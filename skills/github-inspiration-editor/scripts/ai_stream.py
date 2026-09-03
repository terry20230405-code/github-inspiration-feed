"""Bounded Chat Completions SSE reader; never accept an unfinished response."""

from __future__ import annotations

import http.client
import json
import time
from typing import Callable


MAX_LINE_BYTES = 1_048_576
MAX_RESPONSE_BYTES = 32 * 1_048_576
READ_BUDGET_SECONDS = 600


class StreamInterrupted(http.client.HTTPException):
    """A response ended before the provider's completion marker arrived."""


class StreamProtocolError(ValueError):
    """An incompatible or rejected response; retrying the same request won't help."""


def read_chat_stream(response, *, started_at: float, on_first_event: Callable[[], None]) -> dict[str, object]:
    """Assemble only assistant content, then expose the usual non-stream JSON shape.

    urllib enforces a socket idle timeout separately. The elapsed-time and byte
    budgets are checked around each read, so heartbeat-only streams cannot keep
    a worker alive forever. A blocked read is still bounded by the socket timeout.
    """
    content: list[str] = []
    event_lines: list[str] = []
    total_bytes = 0
    saw_event = False
    finish_reason = None
    usage = None

    def dispatch(data: str) -> bool:
        nonlocal saw_event, finish_reason, usage
        if not saw_event:
            saw_event = True
            on_first_event()
        if data == "[DONE]":
            if finish_reason != "stop":
                raise StreamInterrupted("Stream ended without a successful finish_reason")
            return True
        chunk = json.loads(data)
        if not isinstance(chunk, dict):
            raise StreamProtocolError("Stream event is not an object")
        if chunk.get("error"):
            # Do not log upstream content, which may contain credentials or prompts.
            raise StreamProtocolError("AI provider returned an error inside the stream")
        if chunk.get("usage") is not None:
            if not isinstance(chunk["usage"], dict):
                raise StreamProtocolError("Stream usage is not an object")
            usage = chunk["usage"]
        choices = chunk.get("choices")
        if not isinstance(choices, list):
            raise StreamProtocolError("Stream event did not contain choices")
        if not choices:  # include_usage emits a final chunk with no choices.
            return False
        if len(choices) != 1 or not isinstance(choices[0], dict) or choices[0].get("index") != 0:
            raise StreamProtocolError("Stream must contain exactly one choice with index 0")
        choice = choices[0]
        delta = choice.get("delta")
        if not isinstance(delta, dict):
            raise StreamProtocolError("Stream choice did not contain a delta")
        if delta.get("refusal"):
            raise StreamProtocolError("AI provider refused the structured request")
        if delta.get("tool_calls") or delta.get("function_call"):
            raise StreamProtocolError("AI returned a tool call instead of structured text")
        text = delta.get("content")
        if text is not None:
            if not isinstance(text, str):
                raise StreamProtocolError("Stream content delta is not text")
            if text and finish_reason is not None:
                raise StreamProtocolError("Stream contained content after completion")
            content.append(text)
        reason = choice.get("finish_reason")
        if reason is not None:
            if reason == "length":
                raise StreamProtocolError("AI output reached the token limit before completion")
            if reason != "stop":
                raise StreamProtocolError("AI stream did not finish normally")
            if finish_reason is not None:
                raise StreamProtocolError("Stream contained duplicate completion markers")
            finish_reason = reason
        return False

    while True:
        if time.monotonic() - started_at > READ_BUDGET_SECONDS:
            raise StreamInterrupted("Stream exceeded the total read budget")
        raw = response.readline(MAX_LINE_BYTES + 1)
        if time.monotonic() - started_at > READ_BUDGET_SECONDS:
            raise StreamInterrupted("Stream exceeded the total read budget")
        if not raw:
            raise StreamInterrupted("Stream closed before data: [DONE]; partial content discarded")
        total_bytes += len(raw)
        if len(raw) > MAX_LINE_BYTES or total_bytes > MAX_RESPONSE_BYTES:
            raise StreamProtocolError("Stream exceeded the response size budget")
        line = raw.decode("utf-8").rstrip("\r\n")
        if total_bytes == len(raw):
            line = line.removeprefix("\ufeff")
        if not line:
            if event_lines:
                done = dispatch("\n".join(event_lines))
                event_lines.clear()
                if done:
                    return {"choices": [{"finish_reason": "stop", "message": {"content": "".join(content)}}], "usage": usage}
        elif line.startswith("data:"):
            event_lines.append(line[5:].removeprefix(" "))
        # SSE comments, event names and IDs carry no assistant text.
