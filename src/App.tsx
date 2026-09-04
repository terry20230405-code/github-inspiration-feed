import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react'
import { ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Check, ChevronRight, ExternalLink, Star } from 'lucide-react'
import { ProjectIdentity } from './components/ProjectIdentity'
import { LanguageSwitch } from './components/LanguageSwitch'
import { localizeEditorial, messages, readLanguage, saveLanguage, type Language } from './i18n'
import { formatRelativeDate, formatRepositoryCount, repositoryUrl, type Direction } from './data'
import { loadProject, loadProjectIndex, retainProjectCache, type ProjectIndexEntry, type RuntimeProject as Project } from './data/runtime'
import { clampProjectIndex, progressIndicatorTargets, renderedProjectIndices, retainedProjectIndices } from './feed-window'

function ProjectTitle({ name }: { name: string }) {
  const titleRef = useRef<HTMLHeadingElement>(null)

  useLayoutEffect(() => {
    const title = titleRef.current
    const container = title?.parentElement
    if (!title || !container) return

    let cancelled = false
    const fitOnOneLine = () => {
      if (cancelled) return
      title.style.removeProperty('font-size')

      const availableWidth = title.clientWidth
      const naturalWidth = title.scrollWidth
      if (!availableWidth || naturalWidth <= availableWidth) return

      const styles = window.getComputedStyle(title)
      const baseFontSize = Number.parseFloat(styles.fontSize)
      const minimumFontSize = Number.parseFloat(styles.getPropertyValue('--project-title-min-size')) || 24
      const fittedFontSize = Math.max(minimumFontSize, Math.floor(baseFontSize * availableWidth / naturalWidth))
      title.style.fontSize = `${fittedFontSize}px`
    }

    fitOnOneLine()
    const resizeObserver = new ResizeObserver(fitOnOneLine)
    resizeObserver.observe(container)
    void document.fonts.ready.then(fitOnOneLine)

    return () => {
      cancelled = true
      resizeObserver.disconnect()
    }
  }, [name])

  return <h1 ref={titleRef} className="project-title">{name}</h1>
}

function FeedCard({ project, index, total, active, onOpen, language }: { project: Project; index: number; total: number; active: boolean; onOpen: () => void; language: Language }) {
  const { repository, visual } = project
  const editorial = localizeEditorial(project, language)
  const t = messages[language]
  const contentLanguage = language === 'en' ? 'en' : 'zh-CN'
  return (
    <section className={`feed-card ${active ? 'is-active' : ''}`} data-index={index} style={{ '--project-accent': visual.accent, '--project-foreground': visual.foreground } as CSSProperties}>
      <div className="feed-inner">
        <div className="eyebrow feed-index"><span>{String(index + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}</span></div>
        <div className="project-heading" lang={contentLanguage}>
          <ProjectTitle name={repository.name}/>
          <p className="project-hook">{editorial.hook}</p>
          <p className="project-summary">{editorial.summary}</p>
        </div>
        <div className="project-actions">
          <div className="meta-row"><span><Star size={15} fill="currentColor"/> {formatRepositoryCount(repository.stars)}</span><span className="lang-dot" style={{background: visual.accent}}/> <span>{repository.language}</span></div>
          <a className="github-editorial github-hover-link" href={repositoryUrl(repository.fullName)} target="_blank" rel="noreferrer"><span>{t.github}</span><ExternalLink size={14}/></a>
        </div>
        <div className="possibilities">
          <div className="section-label">{t.continueFrom}</div>
          {editorial.directions.slice(0, 3).map((item, directionIndex) => <div className="possibility" lang={contentLanguage} key={item.id}><span className="possibility-index">0{directionIndex + 1}</span><span className="possibility-copy"><strong>{item.name}</strong><small>{item.tagline}</small></span></div>)}
        </div>
        <button className="remix-link" onClick={onOpen}><span>{t.explore}</span><ArrowRight size={18}/></button>
      </div>
    </section>
  )
}

function FeedPlaceholder({ entry, index, language }: { entry: ProjectIndexEntry; index: number; language: Language }) {
  return <section className="feed-card feed-card--loading" data-index={index} aria-busy="true" style={{ '--project-accent': entry.accent, '--project-foreground': entry.foreground } as CSSProperties}><span>{messages[language].loadingNext}</span></section>
}

function DirectionCard({ direction, selected, revealed, onSelect }: { direction: Direction; selected: boolean; revealed: boolean; onSelect: () => void }) {
  return <button className={`direction-card ${selected ? 'selected' : ''} ${revealed ? 'is-visible' : ''}`} onClick={onSelect}>
    <span className="radio">{selected && <Check size={14}/>}</span>
    <span className="direction-copy"><strong>{direction.name}</strong><small>{direction.tagline}</small></span>
    <ChevronRight size={18}/>
  </button>
}

function Detail({ project, onBack, language, onLanguageChange }: { project: Project; onBack: () => void; language: Language; onLanguageChange: (language: Language) => void }) {
  const { repository, visual } = project
  const editorial = localizeEditorial(project, language)
  const t = messages[language]
  const contentLanguage = language === 'en' ? 'en' : 'zh-CN'
  const [selectedId, setSelectedId] = useState(editorial.directions[0].id)
  const [viewedAt] = useState(() => Date.now())
  const selected = editorial.directions.find(direction => direction.id === selectedId) ?? editorial.directions[0]
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
    <nav className="detail-nav"><button className="detail-back-link" onClick={onBack}><ArrowLeft size={19}/><span>{t.back}</span></button><span className="detail-project-name">{repository.name}</span><div className="top-actions"><a className="detail-nav-github github-hover-link" href={repositoryUrl(repository.fullName)} target="_blank" rel="noreferrer"><span>{t.originalLink}</span><ExternalLink size={13}/></a><LanguageSwitch language={language} onChange={onLanguageChange}/></div></nav>
    <header className="detail-hero"><div className="detail-wrap detail-hero-wrap"><ProjectIdentity visual={visual}/><div className="detail-heading-row"><h1>{t.heroFrom(repository.name)}<br/>{t.heroGrow}</h1><a className="github-link detail-github-link github-hover-link" href={repositoryUrl(repository.fullName)} target="_blank" rel="noreferrer"><span>{t.viewOriginal}</span><ExternalLink size={14}/></a></div><p lang={contentLanguage}>{editorial.summary}</p></div></header>
    <div className="detail-wrap detail-content">
      <section data-reveal="section"><div className="section-kicker">{t.original}</div><h2>{t.core}</h2><p className="lead" lang={contentLanguage}>{editorial.meaning}</p>
        <div className="stat-grid" data-reveal="stats"><div><span>STAR</span><strong>{formatRepositoryCount(repository.stars)}</strong></div><div><span>FORK</span><strong>{formatRepositoryCount(repository.forks)}</strong></div><div><span>{t.updated}</span><strong>{formatRelativeDate(repository.pushedAt, viewedAt, language)}</strong></div><div><span>{t.license}</span><strong>{repository.license === '未知' ? t.unknown : repository.license}</strong></div></div>
        <div className="info-grid"><div><h3>{t.features}</h3><ul lang={contentLanguage}>{editorial.features.map(x => <li key={x}>{x}</li>)}</ul></div><div className="info-audience"><h3>{t.audience}</h3><p lang={contentLanguage}>{editorial.audience}</p></div><div className="info-stack"><h3>{t.stack}</h3><div className="tag-list">{editorial.stack.map(x => <span key={x}>{x}</span>)}</div></div></div>
      </section>
      <section className="opportunity" data-reveal="section"><div className="section-kicker">{t.opportunity}</div><h2>{t.why}</h2><div className="reason-list" data-reveal="reasons" lang={contentLanguage}>{editorial.opportunity.map((x, i) => <div key={x}><span>0{i + 1}</span><p>{x}</p></div>)}</div></section>
      <section data-reveal="section"><div className="section-kicker">{t.directions}</div><h2>{t.what}</h2><p className="section-intro">{t.intro}</p><div className="direction-list" ref={directionListRef} lang={contentLanguage}>{editorial.directions.map(d => <DirectionCard key={d.id} direction={d} selected={selected.id === d.id} revealed={directionsVisible} onSelect={() => setSelectedId(d.id)}/>)}</div>
        <div className="direction-detail" key={selected.id}><div className="direction-title"><span>{t.selected}</span><h3 lang={contentLanguage}>{selected.name}</h3><p lang={contentLanguage}>{selected.tagline}</p></div><div className="analysis-grid"><div><span>{t.problem}</span><p lang={contentLanguage}>{selected.problem}</p></div><div><span>{t.target}</span><p lang={contentLanguage}>{selected.audience}</p></div><div><span>{t.approach}</span><p lang={contentLanguage}>{selected.approach}</p></div><div><span>{t.difference}</span><p lang={contentLanguage}>{selected.difference}</p></div></div><div className="minimum-scope"><span>{t.scope}</span><ul lang={contentLanguage}>{selected.scope.map(x => <li key={x}><Check size={15}/>{x}</li>)}</ul></div></div>
      </section>
    </div>
  </main>
}

export default function App() {
  const [language, setLanguage] = useState<Language>(readLanguage)
  const t = messages[language]
  useEffect(() => {
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en'
    document.title = messages[language].title
    saveLanguage(language)
  }, [language])
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

  if (!projectIndex.length) return <main className="app-loading"><div className="loading-language"><LanguageSwitch language={language} onChange={setLanguage}/></div><span role="status">{loadError ? t.loadError : t.loading}</span></main>
  if (detail) return <Detail project={detail} onBack={closeDetail} language={language} onLanguageChange={setLanguage}/>
  const theme = currentProject?.visual ?? currentEntry
  const firstRendered = renderIndices[0] ?? 0
  const lastRendered = renderIndices.at(-1) ?? -1
  return <div className="app-shell" style={{ '--project-accent': theme.accent, '--project-foreground': theme.foreground } as CSSProperties}>
    <header className="topbar"><a className="brand" href="#">{t.brand}<span>β</span></a><div className="progress">{indicatorTargets.map((target, slot) => <button key={slot} disabled={target === null} className={target === active ? 'active' : ''} onClick={() => target !== null && goTo(target)} aria-label={target === null ? t.noProject : t.goTo(target + 1)}/>)}</div><div className="top-actions"><span className="top-note">{t.note}</span><LanguageSwitch language={language} onChange={setLanguage}/></div></header>
    <div className="feed" ref={feedRef} onScroll={handleFeedScroll}>
      {firstRendered > 0 && <div className="feed-spacer" style={{ height: `${firstRendered * 100}dvh` }} aria-hidden="true"/>}
      {renderIndices.map(index => {
        const entry = projectIndex[index]
        const project = loadedProjects.get(entry.id)
        return project
          ? <FeedCard key={entry.id} project={project} index={index} total={total} active={index === active} onOpen={() => { setActive(index); setDetail(project) }} language={language}/>
          : <FeedPlaceholder key={entry.id} entry={entry} index={index} language={language}/>
      })}
      {lastRendered < total - 1 && <div className="feed-spacer" style={{ height: `${(total - lastRendered - 1) * 100}dvh` }} aria-hidden="true"/>}
    </div>
    <div className="pager"><button aria-label={t.previous} onClick={() => goTo(active - 1)} disabled={active === 0}><ArrowUp size={18}/></button><span>{active + 1} / {total}</span><button aria-label={t.next} onClick={() => goTo(active + 1)} disabled={active === total - 1}><ArrowDown size={18}/></button></div>
    {loadError && <div className="feed-error" role="status">{t.loadError}</div>}
  </div>
}
