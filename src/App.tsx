import { useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from 'react'
import { ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Check, ChevronRight, ExternalLink, Star } from 'lucide-react'
import { ProjectIdentity } from './components/ProjectIdentity'
import { formatRelativeDate, formatRepositoryCount, projects, repositoryUrl, type Direction, type Project } from './data'

function FeedCard({ project, index, active, onOpen }: { project: Project; index: number; active: boolean; onOpen: () => void }) {
  const { repository, editorial, visual } = project
  return (
    <section className={`feed-card ${active ? 'is-active' : ''}`} data-index={index} style={{ '--project-accent': visual.accent, '--project-foreground': visual.foreground } as CSSProperties}>
      <div className="feed-inner">
        <div className="eyebrow feed-index"><span>{String(index + 1).padStart(2, '0')} / {String(projects.length).padStart(2, '0')}</span></div>
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
  const [active, setActive] = useState(0)
  const [detail, setDetail] = useState<Project | null>(null)
  const feedRef = useRef<HTMLDivElement>(null)
  const restoreFeedPosition = useRef(false)
  const goTo = (next: number) => feedRef.current?.children[Math.max(0, Math.min(projects.length - 1, next))]?.scrollIntoView({ behavior: 'smooth' })

  useLayoutEffect(() => {
    if (detail || !restoreFeedPosition.current) return

    const feed = feedRef.current
    const card = feed?.children[active] as HTMLElement | undefined
    if (feed && card) {
      const scrollBehavior = feed.style.scrollBehavior
      feed.style.scrollBehavior = 'auto'
      feed.scrollTop = card.offsetTop
      feed.style.scrollBehavior = scrollBehavior
    }
    restoreFeedPosition.current = false
  }, [active, detail])

  const closeDetail = () => {
    restoreFeedPosition.current = true
    setDetail(null)
  }

  useEffect(() => {
    if (detail) return
    const el = feedRef.current
    if (!el) return
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) setActive(Number((entry.target as HTMLElement).dataset.index)) }), { root: el, threshold: .65 })
    Array.from(el.children).forEach(child => observer.observe(child))
    const key = (e: KeyboardEvent) => { if (['ArrowDown', 'PageDown'].includes(e.key)) { e.preventDefault(); goTo(active + 1) } if (['ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); goTo(active - 1) } }
    window.addEventListener('keydown', key)
    return () => { observer.disconnect(); window.removeEventListener('keydown', key) }
  }, [active, detail])
  if (detail) return <Detail project={detail} onBack={closeDetail}/>
  return <div className="app-shell" style={{ '--project-accent': projects[active].visual.accent, '--project-foreground': projects[active].visual.foreground } as CSSProperties}>
    <header className="topbar"><a className="brand" href="#">灵感流<span>β</span></a><div className="progress">{projects.map((_, i) => <button key={i} className={i === active ? 'active' : ''} onClick={() => goTo(i)} aria-label={`前往第 ${i + 1} 个项目`}/>)}</div><span className="top-note">为你的下一个项目，找一个起点</span></header>
    <div className="feed" ref={feedRef}>{projects.map((project, index) => <FeedCard key={project.id} project={project} index={index} active={index === active} onOpen={() => { setActive(index); setDetail(project) }}/>)}</div>
    <div className="pager"><button onClick={() => goTo(active - 1)} disabled={active === 0}><ArrowUp size={18}/></button><span>{active + 1} / {projects.length}</span><button onClick={() => goTo(active + 1)} disabled={active === projects.length - 1}><ArrowDown size={18}/></button></div>
  </div>
}
