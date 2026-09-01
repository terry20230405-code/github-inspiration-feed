import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react'
import { ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Check, ChevronRight, ExternalLink, Star } from 'lucide-react'
import { ProjectIdentity } from './components/ProjectIdentity'
import { formatRelativeDate, formatRepositoryCount, repositoryUrl, type Direction, type Project } from './data'
import { loadProject, loadProjectIndex, retainProjectCache, type ProjectIndexEntry } from './data/runtime'
import { clampProjectIndex, progressIndicatorTargets, renderedProjectIndices, retainedProjectIndices } from './feed-window'

function FeedCard({ project, index, total, active, onOpen }: { project: Project; index: number; total: number; active: boolean; onOpen: () => void }) {
  const { repository, editorial, visual } = project
  return (
    <section className={`feed-card ${active ? 'is-active' : ''}`} data-index={index} style={{ '--project-accent': visual.accent, '--project-foreground': visual.foreground } as CSSProperties}>
      <div className="feed-inner">
        <div className="eyebrow feed-index"><span>{String(index + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}</span></div>
        <div className="project-heading">
          <h1>{repository.name}</h1>
          <p className="project-hook">{editorial.hook}</p>
          <p className="project-summary">{editorial.summary}</p>
        </div>
        <div className="project-actions">
          <div className="meta-row"><span><Star size={15} fill="currentColor"/> {formatRepositoryCount(repository.stars)}</span><span className="lang-dot" style={{background: visual.accent}}/> <span>{repository.language}</span></div>
          <a className="github-editorial github-hover-link" href={repositoryUrl(repository.fullName)} target="_blank" rel="noreferrer"><span>在 GitHub 查看</span><ExternalLink size={14}/></a>
        </div>
        <div className="possibilities">
          <div className="section-label">从这里继续</div>
          {editorial.directions.slice(0, 3).map((item, directionIndex) => <div className="possibility" key={item.id}><span className="possibility-index">0{directionIndex + 1}</span><span className="possibility-copy"><strong>{item.name}</strong><small>{item.tagline}</small></span></div>)}
        </div>
        <button className="remix-link" onClick={onOpen}><span>查看 3 个改造方向</span><ArrowRight size={18}/></button>
      </div>
    </section>
  )
}

function FeedPlaceholder({ entry, index }: { entry: ProjectIndexEntry; index: number }) {
  return <section className="feed-card feed-card--loading" data-index={index} aria-busy="true" style={{ '--project-accent': entry.accent, '--project-foreground': entry.foreground } as CSSProperties}><span>正在准备下一个项目</span></section>
}

function DirectionCard({ direction, selected, revealed, onSelect }: { direction: Direction; selected: boolean; revealed: boolean; onSelect: () => void }) {
  return <button className={`direction-card ${selected ? 'selected' : ''} ${revealed ? 'is-visible' : ''}`} onClick={onSelect}>
    <span className="radio">{selected && <Check size={14}/>}</span>
    <span className="direction-copy"><strong>{direction.name}</strong><small>{direction.tagline}</small></span>
    <ChevronRight size={18}/>
  </button>
}

function Detail({ project, onBack }: { project: Project; onBack: () => void }) {
  const { repository, editorial, visual } = project
  const [selected, setSelected] = useState(editorial.directions[0])
  const [directionsVisible, setDirectionsVisible] = useState(() => !('IntersectionObserver' in window))
  const directionListRef = useRef<HTMLDivElement>(null)
  const detailRef = useRef<HTMLElement>(null)
  useEffect(() => { window.scrollTo(0, 0) }, [project])
  useEffect(() => {
    const detail = detailRef.current
    if (!detail) return
    const revealItems = Array.from(detail.querySelectorAll<HTMLElement>('[data-reveal]'))
    if (!('IntersectionObserver' in window)) {
      revealItems.forEach(item => { item.dataset.inView = 'true' })
      return
    }
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return
        const item = entry.target as HTMLElement
        item.dataset.inView = 'true'
        observer.unobserve(item)
      })
    }, { threshold: .14, rootMargin: '0px 0px -8% 0px' })
    revealItems.forEach(item => observer.observe(item))
    return () => observer.disconnect()
  }, [project])
  useEffect(() => {
    const list = directionListRef.current
    if (!list) return
    if (!('IntersectionObserver' in window)) return
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return
      setDirectionsVisible(true)
      observer.disconnect()
    }, { threshold: .15 })
    observer.observe(list)
    return () => observer.disconnect()
  }, [])
  return <main className="detail" ref={detailRef} style={{ '--project-accent': visual.accent, '--project-foreground': visual.foreground } as CSSProperties}>
    <nav className="detail-nav"><button className="detail-back-link" onClick={onBack}><ArrowLeft size={19}/><span>灵感流</span></button><span>{repository.name}</span><a className="detail-nav-github github-hover-link" href={repositoryUrl(repository.fullName)} target="_blank" rel="noreferrer"><span>GitHub 原项目</span><ExternalLink size={13}/></a></nav>
    <header className="detail-hero"><div className="detail-wrap detail-hero-wrap"><ProjectIdentity visual={visual}/><div className="detail-heading-row"><h1>从 {repository.name}<br/>长出你的项目</h1><a className="github-link detail-github-link github-hover-link" href={repositoryUrl(repository.fullName)} target="_blank" rel="noreferrer"><span>查看 GitHub 原项目</span><ExternalLink size={14}/></a></div><p>{editorial.summary}</p></div></header>
    <div className="detail-wrap detail-content">
      <section data-reveal="section"><div className="section-kicker">01 / 原项目</div><h2>先看懂它的核心</h2><p className="lead">{editorial.meaning}</p>
        <div className="stat-grid" data-reveal="stats"><div><span>STAR</span><strong>{formatRepositoryCount(repository.stars)}</strong></div><div><span>FORK</span><strong>{formatRepositoryCount(repository.forks)}</strong></div><div><span>更新</span><strong>{formatRelativeDate(repository.pushedAt)}</strong></div><div><span>许可</span><strong>{repository.license}</strong></div></div>
        <div className="info-grid"><div><h3>核心功能</h3><ul>{editorial.features.map(x => <li key={x}>{x}</li>)}</ul></div><div className="info-audience"><h3>适合谁</h3><p>{editorial.audience}</p></div><div className="info-stack"><h3>技术基础</h3><div className="tag-list">{editorial.stack.map(x => <span key={x}>{x}</span>)}</div></div></div>
      </section>
      <section className="opportunity" data-reveal="section"><div className="section-kicker">02 / 机会</div><h2>为什么值得继续做？</h2><div className="reason-list" data-reveal="reasons">{editorial.opportunity.map((x, i) => <div key={x}><span>0{i + 1}</span><p>{x}</p></div>)}</div></section>
      <section data-reveal="section"><div className="section-kicker">03 / 选择方向</div><h2>你想把它变成什么？</h2><p className="section-intro">先选一个清晰的小切口。选择后，下方会展示这条路线的具体做法。</p><div className="direction-list" ref={directionListRef}>{editorial.directions.map(d => <DirectionCard key={d.id} direction={d} selected={selected.id === d.id} revealed={directionsVisible} onSelect={() => setSelected(d)}/>)}</div>
        <div className="direction-detail" key={selected.id}><div className="direction-title"><span>当前选择</span><h3>{selected.name}</h3><p>{selected.tagline}</p></div><div className="analysis-grid"><div><span>解决的问题</span><p>{selected.problem}</p></div><div><span>目标用户</span><p>{selected.audience}</p></div><div><span>可以怎么做</span><p>{selected.approach}</p></div><div><span>与原项目的不同</span><p>{selected.difference}</p></div></div><div className="minimum-scope"><span>最小功能范围</span><ul>{selected.scope.map(x => <li key={x}><Check size={15}/>{x}</li>)}</ul></div></div>
      </section>
    </div>
  </main>
}

export default function App() {
  const [projectIndex, setProjectIndex] = useState<readonly ProjectIndexEntry[]>([])
  const [loadedProjects, setLoadedProjects] = useState<Map<string, Project>>(() => new Map())
  const [loadError, setLoadError] = useState('')
  const [active, setActive] = useState(0)
  const [detail, setDetail] = useState<Project | null>(null)
  const feedRef = useRef<HTMLDivElement>(null)
  const scrollFrame = useRef<number | null>(null)
  const restoreFeedPosition = useRef(false)
  const total = projectIndex.length
  const renderIndices = useMemo(() => renderedProjectIndices(active, total), [active, total])
  const indicatorTargets = useMemo(() => progressIndicatorTargets(active, total), [active, total])
  const currentEntry = projectIndex[active]
  const currentProject = currentEntry ? loadedProjects.get(currentEntry.id) : undefined
  const goTo = useCallback((next: number) => {
    const feed = feedRef.current
    if (!feed || total === 0) return
    feed.scrollTo({ top: clampProjectIndex(next, total) * feed.clientHeight, behavior: 'smooth' })
  }, [total])

  useEffect(() => {
    let cancelled = false
    loadProjectIndex()
      .then(index => {
        if (cancelled) return
        setProjectIndex(index)
        setLoadError('')
      })
      .catch(error => {
        if (!cancelled) setLoadError(error instanceof Error ? error.message : '项目索引读取失败')
      })
    return () => { cancelled = true }
  }, [])

  useEffect(() => {
    if (!total) return
    let cancelled = false
    const retainedIndices = retainedProjectIndices(active, total)
    const retainedIds = new Set(retainedIndices.map(index => projectIndex[index].id))
    retainProjectCache(retainedIds)
    queueMicrotask(() => {
      if (!cancelled) setLoadedProjects(previous => new Map([...previous].filter(([id]) => retainedIds.has(id))))
    })

    for (const index of retainedIndices) {
      const id = projectIndex[index].id
      loadProject(id)
        .then(project => {
          if (cancelled) return
          setLoadedProjects(previous => {
            const next = new Map([...previous].filter(([projectId]) => retainedIds.has(projectId)))
            next.set(id, project)
            return next
          })
          if (index === active) setLoadError('')
        })
        .catch(error => {
          if (!cancelled && index === active && error instanceof Error && error.name !== 'AbortError') setLoadError(error.message)
        })
    }
    return () => { cancelled = true }
  }, [active, projectIndex, total])

  useLayoutEffect(() => {
    if (detail || !restoreFeedPosition.current || !total) return

    const feed = feedRef.current
    if (feed) {
      const scrollBehavior = feed.style.scrollBehavior
      feed.style.scrollBehavior = 'auto'
      feed.scrollTop = active * feed.clientHeight
      feed.style.scrollBehavior = scrollBehavior
    }
    restoreFeedPosition.current = false
  }, [active, detail, total])

  const closeDetail = () => {
    restoreFeedPosition.current = true
    setDetail(null)
  }

  useEffect(() => {
    if (detail || !total) return
    const key = (e: KeyboardEvent) => { if (['ArrowDown', 'PageDown'].includes(e.key)) { e.preventDefault(); goTo(active + 1) } if (['ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); goTo(active - 1) } }
    window.addEventListener('keydown', key)
    return () => window.removeEventListener('keydown', key)
  }, [active, detail, goTo, total])

  useEffect(() => {
    if (detail || !total) return
    const resize = () => {
      const feed = feedRef.current
      if (feed) feed.scrollTop = active * feed.clientHeight
    }
    window.addEventListener('resize', resize)
    return () => window.removeEventListener('resize', resize)
  }, [active, detail, total])

  const handleFeedScroll = () => {
    if (scrollFrame.current !== null) return
    scrollFrame.current = window.requestAnimationFrame(() => {
      scrollFrame.current = null
      const feed = feedRef.current
      if (!feed || !feed.clientHeight) return
      const next = clampProjectIndex(Math.round(feed.scrollTop / feed.clientHeight), total)
      setActive(previous => previous === next ? previous : next)
    })
  }

  if (!projectIndex.length) return <main className="app-loading"><span>{loadError || '正在准备灵感流'}</span></main>
  if (detail) return <Detail project={detail} onBack={closeDetail}/>
  const theme = currentProject?.visual ?? currentEntry
  const firstRendered = renderIndices[0] ?? 0
  const lastRendered = renderIndices.at(-1) ?? -1
  return <div className="app-shell" style={{ '--project-accent': theme.accent, '--project-foreground': theme.foreground } as CSSProperties}>
    <header className="topbar"><a className="brand" href="#">灵感流<span>β</span></a><div className="progress">{indicatorTargets.map((target, slot) => <button key={slot} disabled={target === null} className={target === active ? 'active' : ''} onClick={() => target !== null && goTo(target)} aria-label={target === null ? '暂无项目' : `前往第 ${target + 1} 个项目`}/>)}</div><span className="top-note">为你的下一个项目，找一个起点</span></header>
    <div className="feed" ref={feedRef} onScroll={handleFeedScroll}>
      {firstRendered > 0 && <div className="feed-spacer" style={{ height: `${firstRendered * 100}dvh` }} aria-hidden="true"/>}
      {renderIndices.map(index => {
        const entry = projectIndex[index]
        const project = loadedProjects.get(entry.id)
        return project
          ? <FeedCard key={entry.id} project={project} index={index} total={total} active={index === active} onOpen={() => { setActive(index); setDetail(project) }}/>
          : <FeedPlaceholder key={entry.id} entry={entry} index={index}/>
      })}
      {lastRendered < total - 1 && <div className="feed-spacer" style={{ height: `${(total - lastRendered - 1) * 100}dvh` }} aria-hidden="true"/>}
    </div>
    <div className="pager"><button onClick={() => goTo(active - 1)} disabled={active === 0}><ArrowUp size={18}/></button><span>{active + 1} / {total}</span><button onClick={() => goTo(active + 1)} disabled={active === total - 1}><ArrowDown size={18}/></button></div>
    {loadError && <div className="feed-error" role="status">{loadError}</div>}
  </div>
}
