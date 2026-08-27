import type { ProjectLayerMap, ProjectVisual } from './types'

export const projectVisuals: ProjectLayerMap<ProjectVisual> = {
  remotion: { generatorVersion: 2, seed: 'remotion-dev/remotion', accent: '#588019', foreground: '#ffffff', motif: 'orbit', variant: 2966549373 },
  excalidraw: { generatorVersion: 2, seed: 'excalidraw/excalidraw', accent: '#2a74cb', foreground: '#ffffff', motif: 'wave', variant: 1109566981 },
  immich: { generatorVersion: 2, seed: 'immich-app/immich', accent: '#c526ae', foreground: '#ffffff', motif: 'radial', variant: 1244886925 },
  n8n: { generatorVersion: 2, seed: 'n8n-io/n8n', accent: '#1b8825', foreground: '#000000', motif: 'network', variant: 2367143650 },
}
