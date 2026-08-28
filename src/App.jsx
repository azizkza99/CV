import { useEffect, useState } from 'react'
import { content, shared } from './content'

function getInitialLanguage() {
  try {
    return window.localStorage.getItem('cv-language:v1') === 'en' ? 'en' : 'ar'
  } catch {
    return 'ar'
  }
}

function ArrowIcon() {
  return <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M7 17 17 7M8 7h9v9" /></svg>
}

function SectionHeading({ number, children }) {
  return <div className="section-heading"><span>{number}</span><h2>{children}</h2></div>
}

export default function App() {
  const [language, setLanguage] = useState(getInitialLanguage)
  const copy = content[language]
  const isArabic = language === 'ar'

  useEffect(() => {
    document.documentElement.lang = language
    document.documentElement.dir = isArabic ? 'rtl' : 'ltr'
    document.title = copy.meta.title
    document.querySelector('meta[name="description"]')?.setAttribute('content', copy.meta.description)
    try { window.localStorage.setItem('cv-language:v1', language) } catch { /* optional preference */ }
  }, [copy.meta.description, copy.meta.title, isArabic, language])

  return (
    <>
      <a className="skip-link" href="#about">{isArabic ? 'انتقل إلى المحتوى' : 'Skip to content'}</a>
      <header className="site-header">
        <a className="brand" href="#top" aria-label={copy.name}><span>AA</span><strong>{copy.name}</strong></a>
        <nav aria-label={isArabic ? 'التنقل الرئيسي' : 'Main navigation'}>
          {copy.nav.map((item, index) => <a key={item} href={`#${copy.navIds[index]}`}>{item}</a>)}
        </nav>
        <button className="language-button" type="button" aria-label={copy.languageLabel} onClick={() => setLanguage(isArabic ? 'en' : 'ar')}>{copy.language}</button>
      </header>

      <main id="top">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow"><span />{copy.eyebrow}</p>
            <h1 id="hero-title">{copy.name}<small>{copy.role}</small></h1>
            <p className="hero-intro">{copy.intro}</p>
            <div className="hero-actions">
              <a className="button primary" href={`mailto:${shared.email}`}>{copy.contact}<ArrowIcon /></a>
              <a className="button secondary" href={copy.downloadHref} download>{copy.download}</a>
            </div>
            <div className="social-row">
              <a href={shared.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
              <a href={shared.github} target="_blank" rel="noreferrer">GitHub</a>
              <a href={`mailto:${shared.email}`}>{shared.email}</a>
            </div>
          </div>
          <div className="portrait-wrap">
            <div className="portrait-frame" aria-hidden="true">
              <div className="portrait-monogram"><span>AA</span><small>IE × DEV</small></div>
            </div>
            <p>{copy.location}</p>
          </div>
        </section>

        <section className="profile section" id="about">
          <SectionHeading number="01">{copy.sections.about}</SectionHeading>
          <p className="profile-copy">{copy.summary}</p>
          <div className="signal-grid">
            <div><strong>4</strong><span>{isArabic ? 'تجارب ميدانية' : 'Field experiences'}</span></div>
            <div><strong>3</strong><span>{isArabic ? 'لغات' : 'Languages'}</span></div>
            <div><strong>3</strong><span>{isArabic ? 'مشاريع مختارة' : 'Selected projects'}</span></div>
          </div>
        </section>

        <section className="section" id="experience">
          <SectionHeading number="02">{copy.sections.experience}</SectionHeading>
          <div className="timeline">
            {copy.experience.map((item) => (
              <article className="experience-card" key={`${item.company}-${item.date}`}>
                <div className="experience-meta"><time>{item.date}</time><span>{item.place}</span></div>
                <div><h3>{item.role}</h3><p className="company">{item.company}</p><ul>{item.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}</ul></div>
              </article>
            ))}
          </div>
        </section>

        <section className="section" id="projects">
          <SectionHeading number="03">{copy.sections.projects}</SectionHeading>
          <div className="project-grid">
            {shared.projects.map((project, index) => {
              const projectCopy = copy.projectCopy[project.id]
              return (
                <article className="project-card" key={project.id}>
                  <div className="project-number">0{index + 1}</div>
                  <h3>{projectCopy.title}</h3>
                  <p>{projectCopy.description}</p>
                  <div className="tags">{project.stack.map((item) => <span key={item}>{item}</span>)}</div>
                  <div className="project-links">
                    <a href={project.live} target="_blank" rel="noreferrer">{copy.visit}<ArrowIcon /></a>
                    {project.repo && <a href={project.repo} target="_blank" rel="noreferrer">{copy.source}</a>}
                  </div>
                </article>
              )
            })}
          </div>
        </section>

        <section className="section" id="skills">
          <SectionHeading number="04">{copy.sections.skills}</SectionHeading>
          <div className="skills-grid">{copy.skillGroups.map((group) => <article key={group.title}><h3>{group.title}</h3><ul>{group.items.map((item) => <li key={item}>{item}</li>)}</ul></article>)}</div>
        </section>

        <section className="section education" id="education">
          <SectionHeading number="05">{copy.sections.education}</SectionHeading>
          <div className="education-grid">
            <article className="degree-card"><p>{copy.education.date}</p><h3>{copy.education.degree}</h3><strong>{copy.education.school}</strong><span>{copy.education.place}</span><span>{copy.education.grade}</span></article>
            <ul className="academic-list">{copy.academic.map((item, index) => <li key={item}><span>0{index + 1}</span><p>{item}</p></li>)}</ul>
          </div>
        </section>
      </main>

      <footer><p>{copy.footer}</p><a href={`mailto:${shared.email}`}>{shared.email}<ArrowIcon /></a><span>© 2026 {copy.name}</span></footer>
    </>
  )
}
