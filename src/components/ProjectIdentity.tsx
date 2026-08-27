import type { CSSProperties, ReactNode } from 'react'
import type { ProjectVisual } from '../data/types'

type IdentityStyle = CSSProperties & {
  '--motif-enter-x': string
  '--motif-enter-y': string
}

function createRandom(seed: number) {
  let state = seed >>> 0 || 1
  return () => {
    state ^= state << 13
    state ^= state >>> 17
    state ^= state << 5
    return (state >>> 0) / 0xffffffff
  }
}

function renderOrbit(random: () => number, strokeWidth: number): ReactNode {
  const offset = Math.round((random() - 0.5) * 18)
  return <>
    <circle cx={120 + offset} cy="95" r="72" />
    <circle cx={120 + offset} cy="95" r="43" strokeDasharray={`${12 + Math.round(random() * 16)} 9`} />
    <path d={`M ${48 + offset} 95 A 72 72 0 0 1 ${120 + offset} 23`} strokeWidth={strokeWidth + 1} />
    <circle cx={120 + offset} cy="23" r="7" className="motif-fill" />
    <circle cx={192 + offset} cy="95" r="5" className="motif-fill" />
    <path d={`M ${108 + offset} 73 L ${108 + offset} 117 L ${145 + offset} 95 Z`} className="motif-fill" />
  </>
}

function renderWave(random: () => number, strokeWidth: number): ReactNode {
  const lift = Math.round((random() - 0.5) * 16)
  const amplitude = 24 + Math.round(random() * 20)
  return <>
    {[0, 1, 2].map(index => <path key={index} d={`M 20 ${62 + index * 32 + lift} C 68 ${62 - amplitude + index * 32} 95 ${62 + amplitude + index * 32} 138 ${62 + index * 32} S 198 ${62 - amplitude + index * 32} 224 ${62 + index * 32}`} strokeWidth={strokeWidth + (index === 1 ? 1 : 0)} />)}
    <circle cx="20" cy={94 + lift} r="6" className="motif-fill" />
    <circle cx="138" cy={94 + lift} r="5" className="motif-fill" />
    <circle cx="224" cy={94 + lift} r="7" />
  </>
}

function renderRadial(random: () => number, strokeWidth: number): ReactNode {
  const count = 6 + Math.floor(random() * 4)
  const rotation = Math.round(random() * 40)
  return <>
    {Array.from({ length: count }, (_, index) => <ellipse key={index} cx="120" cy="48" rx={13 + Math.round(random() * 5)} ry={29 + Math.round(random() * 9)} transform={`rotate(${rotation + index * (360 / count)} 120 95)`} strokeWidth={strokeWidth} />)}
    <circle cx="120" cy="95" r="13" className="motif-fill" />
  </>
}

function renderNetwork(random: () => number, strokeWidth: number): ReactNode {
  const points = [
    [28 + Math.round(random() * 22), 34 + Math.round(random() * 18)],
    [113 + Math.round(random() * 18), 26 + Math.round(random() * 20)],
    [190 + Math.round(random() * 20), 53 + Math.round(random() * 20)],
    [66 + Math.round(random() * 26), 132 + Math.round(random() * 25)],
    [163 + Math.round(random() * 28), 126 + Math.round(random() * 28)],
  ]
  const links = [[0, 1], [1, 2], [0, 3], [1, 4], [3, 4]]
  return <>
    {links.map(([from, to], index) => <line key={`line-${index}`} x1={points[from][0]} y1={points[from][1]} x2={points[to][0]} y2={points[to][1]} strokeWidth={strokeWidth} />)}
    {points.map(([x, y], index) => index % 2 === 0
      ? <circle key={`node-${index}`} cx={x} cy={y} r={7 + Math.round(random() * 4)} className={index === 0 ? 'motif-fill' : undefined} />
      : <rect key={`node-${index}`} x={x - 8} y={y - 8} width="16" height="16" rx={random() > 0.5 ? 4 : 0} className={index === 3 ? 'motif-fill' : undefined} />)}
  </>
}

function renderStack(random: () => number, strokeWidth: number): ReactNode {
  const count = 5 + Math.floor(random() * 3)
  const tilt = Math.round((random() - 0.5) * 18)
  return <>
    {Array.from({ length: count }, (_, index) => {
      const inset = index * 9
      return <rect key={index} x={30 + inset} y={25 + inset} width={180 - inset * 2} height={118 - inset * 2} rx={index % 2 === 0 ? 7 : 1} transform={`rotate(${tilt + index * 2} 120 95)`} strokeWidth={strokeWidth} className={index === count - 1 ? 'motif-fill-soft' : undefined} />
    })}
  </>
}

function renderGrid(random: () => number, strokeWidth: number): ReactNode {
  const squareNodes = random() > 0.5
  return <>
    {Array.from({ length: 12 }, (_, index) => {
      const column = index % 4
      const row = Math.floor(index / 4)
      const x = 48 + column * 48 + Math.round((random() - 0.5) * 8)
      const y = 48 + row * 48 + Math.round((random() - 0.5) * 8)
      const size = 5 + Math.round(random() * 5)
      return squareNodes && (index + row) % 2 === 0
        ? <rect key={index} x={x - size} y={y - size} width={size * 2} height={size * 2} strokeWidth={strokeWidth} className={index % 5 === 0 ? 'motif-fill' : undefined} />
        : <circle key={index} cx={x} cy={y} r={size} strokeWidth={strokeWidth} className={index % 5 === 0 ? 'motif-fill' : undefined} />
    })}
  </>
}

function renderPath(random: () => number, strokeWidth: number): ReactNode {
  const bend = 30 + Math.round(random() * 36)
  const points = [[28, 140], [70, 86], [116, 112], [164, 48], [208, 72]]
  return <>
    <path d={`M 28 140 C 52 ${140 - bend} 58 ${86 + bend} 70 86 S 102 112 116 112 S 144 ${48 + bend} 164 48 S 194 72 208 72`} strokeWidth={strokeWidth + 1} />
    {points.map(([x, y], index) => <circle key={index} cx={x} cy={y} r={index === 4 ? 8 : 5} className={index === 0 || index === 4 ? 'motif-fill' : undefined} />)}
    <path d="M 196 61 L 214 72 L 196 83" strokeWidth={strokeWidth} />
  </>
}

function renderPolyline(random: () => number, strokeWidth: number): ReactNode {
  const points = Array.from({ length: 6 }, (_, index) => [24 + index * 39, 40 + Math.round(random() * 105)])
  return <>
    <polyline points={points.map(point => point.join(',')).join(' ')} strokeWidth={strokeWidth + 1} />
    {points.map(([x, y], index) => index % 2 === 0
      ? <circle key={index} cx={x} cy={y} r="6" className={index === 0 ? 'motif-fill' : undefined} />
      : <rect key={index} x={x - 6} y={y - 6} width="12" height="12" className={index === 5 ? 'motif-fill' : undefined} />)}
  </>
}

export function ProjectIdentity({ visual }: { visual: ProjectVisual }) {
  const random = createRandom(visual.variant)
  const strokeWidth = 2 + Math.floor(random() * 3)
  const angle = Math.floor(random() * 4)
  const enter = [[12, 5], [-12, 5], [8, -10], [-8, -10]][angle]
  const style: IdentityStyle = {
    '--motif-enter-x': `${enter[0]}px`,
    '--motif-enter-y': `${enter[1]}px`,
  }
  const renderers = {
    orbit: renderOrbit,
    network: renderNetwork,
    wave: renderWave,
    radial: renderRadial,
    stack: renderStack,
    grid: renderGrid,
    path: renderPath,
    polyline: renderPolyline,
  }

  return <svg className="project-motif" viewBox="0 0 240 190" aria-hidden="true" focusable="false" strokeWidth={strokeWidth} style={style}>
    {renderers[visual.motif](random, strokeWidth)}
  </svg>
}
