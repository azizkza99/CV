# Abdelaziz Abuthuraya — CV & Engineering Portfolio

A bilingual professional portfolio connecting industrial engineering, production planning, process improvement, and digital-systems development.

**Live portfolio:** [cv-ruby-two.vercel.app](https://cv-ruby-two.vercel.app/)

## Overview

This project presents verified experience, technical case studies, and downloadable Arabic and English resumes in a responsive, print-friendly interface. It also includes a Python document-generation workflow for reproducible resume updates.

## Tech Stack

- React 19 and JavaScript
- Vite 7
- Modern CSS
- Python 3 and python-docx
- ESLint

## Key Features

- Arabic and English content with complete RTL/LTR switching
- Responsive, accessible, and print-friendly presentation
- Industrial engineering experience and quantified academic projects
- Technical case studies covering 3D visualization, secure workflows, and product systems
- Downloadable English and Arabic CV PDFs
- Python-based resume document generator
- Privacy-first design with no analytics, forms, cookies, or tracking

## Project Structure

- `src/content.js` is the shared source for Arabic and English portfolio copy.
- `src/App.jsx` renders the sections, language switch, and CV download links.
- `public/resumes/` contains the downloadable PDFs referenced by the site.
- `scripts/generate_resumes.py` produces editable Word files in `output-docx/`; it does not regenerate the public PDFs automatically.

## Featured Work

- [FORM — Interactive 3D Door Configurator](https://bezi-product-viewer.vercel.app/)
- [Kayan — Workflow Discovery & Inquiry System](https://kayan-app-henna.vercel.app/)
- [ECLIPSE — Specialty Coffee Experience](https://eclipse-luxury-experience.vercel.app/)
- [Aether OS — Browser Desktop Environment](https://aether-os-seven-kappa.vercel.app/)
- [AFOQ — Arabic-First Studio Experience](https://afoq-landing-page-alpha.vercel.app/)
- [Nexus AI — Product Planning Workspace](https://nexus-ai-rho-two.vercel.app/)

## Setup

```bash
git clone https://github.com/azizkza99/CV.git
cd CV
npm ci
npm run dev
```

Run release checks:

```bash
npm run check
npm audit --audit-level=high
```

Optional resume document generation:

```bash
python -m pip install python-docx
python scripts/generate_resumes.py
```

## Privacy

The public portfolio intentionally omits national ID, date of birth, nationality, work-permit details, and the profile photograph. Contact information is limited to professional channels supplied by the owner.
