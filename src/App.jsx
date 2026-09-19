import { useEffect, useState } from 'react'
import { content, shared } from './content'

function getInitialLanguage() {
  try {
    return window.localStorage.getItem('portfolio-language:v3') === 'ar' ? 'ar' : 'en'
  } catch {
    return 'en'
  }
}

function updateMeta(selector, value) {
  document.querySelector(selector)?.setAttribute('content', value)
}

function ArrowIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="M7 17 17 7M8 7h9v9" />
    </svg>
  )
}

function DownloadIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="M12 3v12m0 0 5-5m-5 5-5-5M5 21h14" />
    </svg>
  )
}

function SectionHeading({ number, eyebrow, children }) {
  return (
    <div className="section-heading">
      <div><span>{number}</span><p>{eyebrow}</p></div>
      <h2>{children}</h2>
    </div>
  )
}

function ProjectVisual({ kind }) {
  return (
    <div className={`project-visual visual-${kind}`} aria-hidden="true">
      <span className="visual-label">{kind.toUpperCase()}</span>
      <div className="visual-canvas"><i /><i /><i /><i /></div>
    </div>
  )
}

export default function App() {
  const [language, setLanguage] = useState(getInitialLanguage)
  const copy = content[language]
  const isArabic = language === 'ar'

  useEffect(() => {
    document.documentElement.lang = language
    document.documentElement.dir = isArabic ? 'rtl' : 'ltr'
    document.title = copy.meta.title
    updateMeta('meta[name="description"]', copy.meta.description)
    updateMeta('meta[property="og:title"]', copy.meta.title)
    updateMeta('meta[property="og:description"]', copy.meta.description)
    updateMeta('meta[name="twitter:title"]', copy.meta.title)
    updateMeta('meta[name="twitter:description"]', copy.meta.description)
    try {
      window.localStorage.setItem('portfolio-language:v3', language)
    } catch {
      // Language persistence is optional.
    }
  }, [copy.meta.description, copy.meta.title, isArabic, language])

  return (
    <>
      <a className="skip-link" href="#about">{copy.skip}</a>

      <header className="site-header">
        <a className="brand" href="#top" aria-label={copy.name}>
          <span className="brand-mark">AA</span>
          <span className="brand-copy"><strong>{copy.name}</strong><small>{copy.brandRole}</small></span>
        </a>
        <nav aria-label={copy.navigationLabel}>
          {copy.nav.map((item, index) => <a key={item} href={`#${copy.navIds[index]}`}>{item}</a>)}
        </nav>
        <div className="header-actions">
          <a className="header-cv" href={copy.downloadHref} download>{copy.cvShort}<DownloadIcon /></a>
          <button className="language-button" type="button" aria-label={copy.languageLabel} onClick={() => setLanguage(isArabic ? 'en' : 'ar')}>
            {copy.language}
          </button>
        </div>
      </header>

      <main id="top">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="availability"><span />{copy.availability}</p>
            <p className="eyebrow">{copy.eyebrow}</p>
            <h1 id="hero-title"><span>{copy.name}</span>{copy.role}</h1>
            <p className="hero-intro">{copy.intro}</p>
            <div className="hero-actions">
              <a className="button primary" href={`mailto:${shared.email}`}>{copy.contact}<ArrowIcon /></a>
              <a className="button secondary" href={copy.downloadHref} download>{copy.download}<DownloadIcon /></a>
            </div>
            <div className="social-row">
              <a href={shared.linkedin} target="_blank" rel="me noreferrer">LinkedIn<ArrowIcon /></a>
              <a href={shared.github} target="_blank" rel="me noreferrer">GitHub<ArrowIcon /></a>
              <a href={`mailto:${shared.email}`}>{shared.email}</a>
              <a href={shared.phoneHref}>{shared.phone}</a>
            </div>
          </div>

          <aside className="hero-dashboard" aria-label={copy.dashboardLabel}>
            <div className="dashboard-top"><span>IE / DIGITAL</span><span className="status"><i />{copy.status}</span></div>
            <div className="dashboard-core">
              <div className="core-ring"><strong>IE</strong><span>×</span><strong>DEV</strong></div>
              <p>{copy.dashboardText}</p>
            </div>
            <div className="dashboard-grid">
              {copy.dashboardItems.map((item, index) => <div key={item}><span>0{index + 1}</span><strong>{item}</strong></div>)}
            </div>
            <div className="dashboard-location">{copy.location}</div>
          </aside>
        </section>

        <section className="section section-shell" id="about">
          <SectionHeading number="01" eyebrow={copy.sectionEyebrows.about}>{copy.sections.about}</SectionHeading>
          <div className="about-layout">
            <p className="profile-copy">{copy.summary}</p>
            <div className="focus-grid">
              {copy.focus.map((item, index) => (
                <article key={item.title}><span>0{index + 1}</span><h3>{item.title}</h3><p>{item.text}</p></article>
              ))}
            </div>
          </div>
          <div className="signal-grid">
            {copy.signals.map((item) => <div key={item.label}><strong>{item.value}</strong><span>{item.label}</span></div>)}
          </div>
        </section>

        <section className="section experience-section" id="experience">
          <div className="section-shell">
            <SectionHeading number="02" eyebrow={copy.sectionEyebrows.experience}>{copy.sections.experience}</SectionHeading>
            <div className="timeline">
              {copy.experience.map((item, index) => (
                <article className="experience-card" key={`${item.company}-${item.date}`}>
                  <div className="experience-index">0{index + 1}</div>
                  <div className="experience-meta"><time>{item.date}</time><span>{item.place}</span></div>
                  <div className="experience-content">
                    <h3>{item.role}</h3><p className="company">{item.company}</p>
                    <ul>{item.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}</ul>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section projects-section" id="projects">
          <div className="section-shell">
            <SectionHeading number="03" eyebrow={copy.sectionEyebrows.projects}>{copy.sections.projects}</SectionHeading>
            <p className="section-intro">{copy.projectsIntro}</p>
            <div className="project-grid">
              {shared.projects.map((project, index) => {
                const projectCopy = copy.projectCopy[project.id]
                return (
                  <article className="project-card" key={project.id}>
                    <ProjectVisual kind={project.id} />
                    <div className="project-body">
                      <div className="project-kicker"><span>0{index + 1}</span>{projectCopy.type}</div>
                      <h3>{projectCopy.title}</h3><p>{projectCopy.description}</p>
                      <div className="tags">{project.stack.map((item) => <span key={item}>{item}</span>)}</div>
                      <div className="project-links">
                        <a href={project.live} target="_blank" rel="noreferrer" aria-label={`${copy.visit}: ${projectCopy.title}`}>{copy.visit}<ArrowIcon /></a>
                        {project.repo && <a href={project.repo} target="_blank" rel="noreferrer" aria-label={`${copy.source}: ${projectCopy.title}`}>{copy.source}<ArrowIcon /></a>}
                      </div>
                    </div>
                  </article>
                )
              })}
            </div>
          </div>
        </section>

        <section className="section section-shell" id="skills">
          <SectionHeading number="04" eyebrow={copy.sectionEyebrows.skills}>{copy.sections.skills}</SectionHeading>
          <div className="skills-grid">
            {copy.skillGroups.map((group) => (
              <article key={group.title}><h3>{group.title}</h3><ul>{group.items.map((item) => <li key={item}>{item}</li>)}</ul></article>
            ))}
          </div>
        </section>

        <section className="section education-section" id="education">
          <div className="section-shell">
            <SectionHeading number="05" eyebrow={copy.sectionEyebrows.education}>{copy.sections.education}</SectionHeading>
            <div className="education-grid">
              <div className="education-list">
                {copy.education.map((item, index) => (
                  <article className={`degree-card${index ? ' degree-card-secondary' : ''}`} key={`${item.school}-${item.date}`}>
                    <span className="degree-date">{item.date}</span><h3>{item.degree}</h3>
                    <strong>{item.school}</strong><span>{item.place}</span><p>{item.detail}</p>
                  </article>
                ))}
              </div>
              <div className="academic-grid">
                {copy.academic.map((item, index) => (
                  <article key={item.title}><span>0{index + 1}</span><div><h3>{item.title}</h3><p>{item.description}</p></div></article>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <div><p className="footer-kicker">{copy.footerKicker}</p><h2>{copy.footer}</h2></div>
        <div className="footer-actions">
          <a className="button light" href={`mailto:${shared.email}`}>{copy.contact}<ArrowIcon /></a>
          <a href={shared.phoneHref}>{shared.phone}</a>
          <a href={shared.linkedin} target="_blank" rel="me noreferrer">LinkedIn</a>
          <a href={shared.github} target="_blank" rel="me noreferrer">GitHub</a>
        </div>
        <span className="copyright">© 2026 {copy.name}</span>
      </footer>
    </>
  )
}
