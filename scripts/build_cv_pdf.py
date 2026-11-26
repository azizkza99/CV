"""Build the public one-page CV PDFs (English and Arabic) from HTML.

Usage:  python scripts/build_cv_pdf.py
Needs:  npm ci (for the fonts) and Playwright with a Chromium/Chrome install.
Output: public/resumes/Abdelaziz-Abuthuraya-CV-EN.pdf and -AR.pdf
"""
import asyncio
import html
import os
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "node_modules" / "@fontsource"
INTER = ROOT / "node_modules" / "@fontsource-variable" / "inter" / "files" / "inter-latin-wght-normal.woff2"
INTER_EXT = ROOT / "node_modules" / "@fontsource-variable" / "inter" / "files" / "inter-latin-ext-wght-normal.woff2"
PLEX = FONTS / "ibm-plex-sans-arabic" / "files"
OUT = ROOT / "public" / "resumes"

CONTACT = {
    "email": "aziz.kza99@gmail.com",
    "phone": "+966 54 994 9023",
    "linkedin": "linkedin.com/in/abdelazizabuthuraya",
    "portfolio": "cv-ruby-two.vercel.app",
    "github": "github.com/azizkza99",
}

EN = {
    "dir": "ltr",
    "lang": "en",
    "name": "Abdelaziz Abuthuraya",
    "title": "Industrial Engineer · Procurement & Supply Chain · Production Planning · AI Automation",
    "location": "Jeddah, Saudi Arabia",
    "labels": {
        "summary": "Profile", "experience": "Experience", "education": "Education",
        "skills": "Skills", "projects": "Selected projects", "languages": "Languages", "current": "Current",
    },
    "summary": (
        "Industrial Engineering graduate (B.Sc., Üsküdar University, English-taught) currently working as a "
        "Procurement Specialist in Saudi Arabia. Brings hands-on experience from manufacturing in Türkiye and EPC "
        "projects in Saudi Arabia across purchasing, production planning, quality, and process improvement, plus "
        "AI-powered automation and bilingual web tools that cut manual reporting and repetitive work."
    ),
    "experience": [
        {
            "role": "Procurement Specialist", "company": "Al Razzaz Establishment for Cash Transportation",
            "place": "Makkah Region, Saudi Arabia", "date": "Jun 2026 – Present", "current": True,
            "bullets": [
                "Handle purchase requests from internal departments, from specification through supplier selection to delivery.",
                "Request and compare supplier quotations on price, quality, and lead time to support cost-effective decisions.",
                "Follow up purchase orders and deliveries; maintain Excel-based purchasing records and spending reports.",
            ],
        },
        {
            "role": "Web & AI Automation Builder", "company": "Freelance",
            "place": "Jeddah · Remote", "date": "Aug 2026 – Present", "current": True,
            "bullets": [
                "Build AI-assisted workflow automations that reduce manual reporting, data entry, and repetitive tasks.",
                "Develop bilingual Arabic/English web apps (React, TypeScript, Supabase); six live projects shipped.",
            ],
        },
        {
            "role": "Production Planning Intern", "company": "Edaş Yatak",
            "place": "Kayseri, Türkiye", "date": "Aug 2025 – Oct 2025",
            "bullets": [
                "Prepared and monitored daily production schedules to keep workflow priorities aligned with delivery dates.",
                "Analyzed production-performance data to identify bottlenecks and coordinated fixes across departments.",
            ],
        },
        {
            "role": "Operations & Process Improvement Intern", "company": "Murat Şahin Orman Ürünleri",
            "place": "Tokat, Türkiye", "date": "Jan 2025 – Jul 2025",
            "bullets": [
                "Supported plywood/MDF production across cutting, pressing, finishing, and packaging; tracked output and waste.",
                "Performed surface and dimensional quality inspections; used SolidWorks for basic engineering support.",
            ],
        },
        {
            "role": "Project Management Intern", "company": "Delta CJSC",
            "place": "Jeddah, Saudi Arabia", "date": "Jul 2024 – Aug 2024",
            "bullets": [
                "Coordinated daily EPC activities and project documentation; maintained Excel scheduling and logistics reports.",
            ],
        },
        {
            "role": "Engineering Intern", "company": "Delta CJSC",
            "place": "Riyadh, Saudi Arabia", "date": "Jul 2022 – Aug 2022",
            "bullets": [
                "Tracked timelines and KPIs across engineering, procurement, and construction activities to flag schedule deviations.",
            ],
        },
    ],
    "education": [
        {"degree": "B.Sc. Industrial Engineering", "school": "Üsküdar University · Istanbul",
         "date": "2020 – 2024", "detail": "English-taught · Graduated Oct 2024"},
        {"degree": "Master's coursework, Industrial Engineering", "school": "Abdullah Gül University · Kayseri",
         "date": "Jan – May 2026", "detail": "One semester: Supply Chain Mgmt, Mathematical Modeling"},
    ],
    "skills": [
        ("Procurement & SCM", "Purchasing · Supplier quotations · PO follow-up · Cost reduction · Negotiation · Supply chain analysis"),
        ("Industrial Eng.", "Production planning · Process improvement · Lean · 5S · Six Sigma basics · Quality control"),
        ("Tools & analysis", "Advanced Excel · Data analysis · Mathematical modeling · MIP optimization · SolidWorks"),
        ("AI & digital", "AI-assisted workflows · Prompt engineering · Automation · React · TypeScript · Supabase"),
    ],
    "projects": [
        ("Supply chain & revenue analysis", "Procurement, capacity, 85% machine utilization, 0.5–1.5% waste."),
        ("QoS-aware VM placement (MIP)", "Mixed-Integer Programming model with a 0% optimality gap."),
        ("HR planning study", "14-question survey across 8 companies (graduation project)."),
        ("FORM · Kayan · ECLIPSE", "Live 3D configurator, workflow system, and bilingual web app."),
    ],
    "languages": "Arabic (native) · English (C1) · Turkish (B1)",
}

AR = {
    "dir": "rtl",
    "lang": "ar",
    "name": "عبد العزيز أبو ثريا",
    "title": "مهندس صناعي · المشتريات وسلاسل الإمداد · تخطيط الإنتاج · الأتمتة بالذكاء الاصطناعي",
    "location": "جدة، المملكة العربية السعودية",
    "labels": {
        "summary": "نبذة", "experience": "الخبرة العملية", "education": "التعليم",
        "skills": "المهارات", "projects": "مشاريع مختارة", "languages": "اللغات", "current": "حالي",
    },
    "summary": (
        "خريج هندسة صناعية (بكالوريوس، جامعة أسكدار، برنامج باللغة الإنجليزية) أعمل حاليًا أخصائي مشتريات في المملكة. "
        "أمتلك خبرة عملية من قطاع التصنيع في تركيا ومشاريع EPC في السعودية في الشراء وتخطيط الإنتاج والجودة وتحسين العمليات، "
        "إلى جانب بناء أتمتة بالذكاء الاصطناعي وأدوات ويب ثنائية اللغة تقلل التقارير اليدوية والأعمال المتكررة."
    ),
    "experience": [
        {
            "role": "أخصائي مشتريات", "company": "مؤسسة الرزاز لنقل الأموال",
            "place": "منطقة مكة المكرمة", "date": "يونيو 2026 – حتى الآن", "current": True,
            "bullets": [
                "أتولى طلبات الشراء من الأقسام الداخلية من تحديد المواصفات واختيار المورد حتى التسليم.",
                "أطلب عروض أسعار الموردين وأقارنها من حيث السعر والجودة ومدة التوريد لدعم قرارات شراء فعّالة التكلفة.",
                "أتابع أوامر الشراء والتوريد وأحدّث سجلات المشتريات وتقارير الإنفاق على Excel.",
            ],
        },
        {
            "role": "مطور ويب وأتمتة بالذكاء الاصطناعي", "company": "عمل حر",
            "place": "جدة · عن بُعد", "date": "أغسطس 2026 – حتى الآن", "current": True,
            "bullets": [
                "أبني أتمتة لسير العمل مدعومة بالذكاء الاصطناعي تقلل التقارير اليدوية وإدخال البيانات والمهام المتكررة.",
                "أطور تطبيقات ويب عربية وإنجليزية (React وTypeScript وSupabase)، وأطلقت ستة مشاريع حية.",
            ],
        },
        {
            "role": "متدرب تخطيط إنتاج", "company": "Edaş Yatak",
            "place": "قيصري، تركيا", "date": "أغسطس – أكتوبر 2025",
            "bullets": [
                "أعددت وتابعت جداول الإنتاج اليومية لربط أولويات العمل بمواعيد التسليم.",
                "حللت بيانات أداء الإنتاج لتحديد الاختناقات ونسّقت الحلول بين الأقسام.",
            ],
        },
        {
            "role": "متدرب عمليات وتحسين إجراءات", "company": "Murat Şahin Orman Ürünleri",
            "place": "توكات، تركيا", "date": "يناير – يوليو 2025",
            "bullets": [
                "دعمت إنتاج ألواح Plywood وMDF في القطع والكبس والتشطيب والتعبئة، وتابعت الإنتاج ونسب الهدر.",
                "أجريت فحوصات الجودة السطحية والبُعدية واستخدمت SolidWorks في الدعم الهندسي.",
            ],
        },
        {
            "role": "متدرب إدارة مشاريع", "company": "Delta CJSC",
            "place": "جدة، السعودية", "date": "يوليو – أغسطس 2024",
            "bullets": ["نسّقت أنشطة ووثائق مشاريع EPC اليومية وأعددت تقارير Excel للجدولة والخدمات اللوجستية."],
        },
        {
            "role": "متدرب هندسي", "company": "Delta CJSC",
            "place": "الرياض، السعودية", "date": "يوليو – أغسطس 2022",
            "bullets": ["تابعت الجداول الزمنية ومؤشرات الأداء عبر أنشطة الهندسة والمشتريات والإنشاءات لرصد الانحرافات."],
        },
    ],
    "education": [
        {"degree": "بكالوريوس الهندسة الصناعية", "school": "جامعة أسكدار · إسطنبول",
         "date": "2020 – 2024", "detail": "برنامج بالإنجليزية · تخرج أكتوبر 2024"},
        {"degree": "مقررات ماجستير في الهندسة الصناعية", "school": "جامعة عبدالله غول · قيصري",
         "date": "يناير – مايو 2026", "detail": "فصل واحد: سلاسل الإمداد والنمذجة الرياضية"},
    ],
    "skills": [
        ("المشتريات وسلاسل الإمداد", "الشراء · عروض الأسعار · متابعة أوامر الشراء · خفض التكاليف · التفاوض · تحليل سلاسل الإمداد"),
        ("الهندسة الصناعية", "تخطيط الإنتاج · تحسين العمليات · Lean · 5S · أساسيات Six Sigma · ضبط الجودة"),
        ("الأدوات والتحليل", "Excel متقدم · تحليل البيانات · النمذجة الرياضية · التحسين (MIP) · SolidWorks"),
        ("الذكاء الاصطناعي والرقمنة", "سير عمل بالذكاء الاصطناعي · هندسة الأوامر · الأتمتة · React · TypeScript · Supabase"),
    ],
    "projects": [
        ("تحليل سلسلة الإمداد والإيرادات", "المشتريات والطاقة الإنتاجية، استغلال آلات 85% وهدر 0.5–1.5%."),
        ("توزيع الآلات الافتراضية (MIP)", "نموذج برمجة صحيحة مختلطة بفجوة أمثلية 0%."),
        ("دراسة تخطيط الموارد البشرية", "استبيان من 14 سؤالًا على 8 شركات (مشروع التخرج)."),
        ("FORM · Kayan · ECLIPSE", "مشاريع حية: أداة ثلاثية الأبعاد ونظام سير عمل وموقع ثنائي اللغة."),
    ],
    "languages": "العربية (اللغة الأم) · الإنجليزية (C1) · التركية (B1)",
}


def esc(text):
    return html.escape(text, quote=True)


def render(d):
    L = d["labels"]
    exp = "".join(
        f"""<article class="job{' current' if e.get('current') else ''}">
          <header><div><h3>{esc(e['role'])}</h3><p class="co">{esc(e['company'])}</p></div>
          <div class="when">{'<span class="badge">' + esc(L['current']) + '</span>' if e.get('current') else ''}<time>{esc(e['date'])}</time><span>{esc(e['place'])}</span></div></header>
          <ul>{''.join(f'<li>{esc(b)}</li>' for b in e['bullets'])}</ul></article>"""
        for e in d["experience"]
    )
    edu = "".join(
        f"<div class='edu'><time>{esc(e['date'])}</time><strong>{esc(e['degree'])}</strong><span>{esc(e['school'])}</span><em>{esc(e['detail'])}</em></div>"
        for e in d["education"]
    )
    skills = "".join(f"<div class='sk'><strong>{esc(t)}</strong><span>{esc(v)}</span></div>" for t, v in d["skills"])
    projects = "".join(f"<div class='pr'><strong>{esc(t)}</strong><span>{esc(v)}</span></div>" for t, v in d["projects"])
    c = CONTACT
    return f"""<!doctype html><html lang="{d['lang']}" dir="{d['dir']}"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Inter; src: url('{INTER.as_uri()}') format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: Inter; src: url('{INTER_EXT.as_uri()}') format('woff2'); font-weight: 100 900; unicode-range: U+0100-024F, U+1E00-1EFF; }}
@font-face {{ font-family: Plex; src: url('{(PLEX / 'ibm-plex-sans-arabic-arabic-400-normal.woff2').as_uri()}'); font-weight: 400; }}
@font-face {{ font-family: Plex; src: url('{(PLEX / 'ibm-plex-sans-arabic-arabic-500-normal.woff2').as_uri()}'); font-weight: 500; }}
@font-face {{ font-family: Plex; src: url('{(PLEX / 'ibm-plex-sans-arabic-arabic-600-normal.woff2').as_uri()}'); font-weight: 600; }}
@font-face {{ font-family: Plex; src: url('{(PLEX / 'ibm-plex-sans-arabic-arabic-700-normal.woff2').as_uri()}'); font-weight: 700; }}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{ width: 210mm; height: 297mm; overflow: hidden; font-family: {'Plex, Inter' if d['dir'] == 'rtl' else 'Inter, Plex'}, sans-serif; color: #172434; font-size: 8.55pt; line-height: 1.42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.top {{ padding: 11mm 13mm 7mm; color: #fff; background: linear-gradient(120deg, #071a2e, #0c3456); position: relative; }}
.top::after {{ content: ''; position: absolute; inset-inline: 0; bottom: 0; height: 2.2px; background: linear-gradient(90deg, #1684bd, #d6a05b); }}
h1 {{ margin: 0; font-size: 22pt; letter-spacing: {'0' if d['dir'] == 'rtl' else '-.02em'}; line-height: 1.15; }}
.title {{ margin: 1.6mm 0 3.2mm; color: #8fd1f0; font-weight: 600; font-size: 9.4pt; }}
.contact {{ display: flex; flex-wrap: wrap; gap: 1mm 5mm; color: #c7d6e2; font-size: 7.9pt; }}
.contact span {{ white-space: nowrap; unicode-bidi: isolate; direction: ltr; }}
.contact span.loc {{ direction: {d['dir']}; }}
.grid {{ display: grid; grid-template-columns: 1fr 61mm; gap: 7mm; padding: 6.5mm 13mm 0; }}
h2 {{ display: flex; align-items: center; gap: 2mm; margin: 0 0 2.4mm; color: #075b8f; font-size: 8.4pt; letter-spacing: {'0' if d['dir'] == 'rtl' else '.12em'}; text-transform: uppercase; }}
h2::after {{ content: ''; flex: 1; height: 1px; background: #d9e3ea; }}
section + section {{ margin-top: 4.6mm; }}
.summary {{ margin: 0; color: #2c3e50; font-size: 8.75pt; line-height: 1.55; }}
.job {{ padding-block: 2.1mm; border-bottom: 1px solid #edf1f4; }}
.job:last-child {{ border: 0; }}
.job header {{ display: flex; justify-content: space-between; gap: 3mm; }}
h3 {{ margin: 0; font-size: 9.6pt; line-height: 1.25; }}
.co {{ margin: .4mm 0 0; color: #075b8f; font-weight: 650; font-size: 8.3pt; }}
.when {{ display: flex; flex-direction: column; align-items: flex-end; text-align: end; gap: .3mm; color: #66768a; font-size: 7.5pt; white-space: nowrap; }}
.when time {{ color: #172434; font-weight: 650; }}
.badge {{ padding: .2mm 1.6mm; color: #0f6a46; background: #e3f6ed; border-radius: 9px; font-size: 6.6pt; font-weight: 700; }}
.job.current {{ border-inline-start: 2.2px solid #1684bd; padding-inline-start: 2.6mm; margin-inline-start: -2.8mm; }}
ul {{ margin: 1.2mm 0 0; padding-inline-start: 3.6mm; color: #3c4c5d; }}
li {{ margin-top: .45mm; }}
li::marker {{ color: #1684bd; }}
aside section {{ padding: 3.6mm 3.8mm; background: #f3f7fa; border-radius: 2.2mm; }}
aside section + section {{ margin-top: 3.2mm; }}
.edu + .edu, .sk + .sk, .pr + .pr {{ margin-top: 2.4mm; }}
.edu time {{ display: block; color: #1684bd; font-weight: 700; font-size: 7.2pt; }}
.edu strong, .sk strong, .pr strong {{ display: block; font-size: 8.3pt; line-height: 1.3; }}
.edu span, .sk span, .pr span {{ display: block; color: #4e5f71; font-size: 7.7pt; }}
.edu em {{ display: block; color: #6b7b8d; font-style: normal; font-size: 7.3pt; }}
.langs {{ color: #3c4c5d; font-size: 8pt; }}
</style></head><body>
<div class="top"><h1>{esc(d['name'])}</h1><p class="title">{esc(d['title'])}</p>
<div class="contact"><span class="loc">{esc(d['location'])}</span><span>{c['phone']}</span><span>{c['email']}</span><span>{c['linkedin']}</span><span>{c['portfolio']}</span></div></div>
<div class="grid"><main>
<section><h2>{esc(L['summary'])}</h2><p class="summary">{esc(d['summary'])}</p></section>
<section><h2>{esc(L['experience'])}</h2>{exp}</section>
</main><aside>
<section><h2>{esc(L['education'])}</h2>{edu}</section>
<section><h2>{esc(L['skills'])}</h2>{skills}</section>
<section><h2>{esc(L['projects'])}</h2>{projects}</section>
<section><h2>{esc(L['languages'])}</h2><div class="langs">{esc(d['languages'])}</div></section>
</aside></div></body></html>"""


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chrome = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=chrome if Path(chrome).exists() else None)
        for data, suffix in [(EN, "EN"), (AR, "AR")]:
            page = await browser.new_page()
            src = ROOT / f".cv-{suffix}.html"
            src.write_text(render(data), encoding="utf-8")
            await page.goto(src.as_uri())
            await page.wait_for_timeout(400)
            overflow = await page.evaluate("document.body.scrollHeight > document.body.clientHeight + 2")
            await page.pdf(path=str(OUT / f"Abdelaziz-Abuthuraya-CV-{suffix}.pdf"), format="A4", print_background=True)
            await page.screenshot(path=str(ROOT / f".cv-{suffix}.png"), full_page=True)
            print(suffix, "overflow!" if overflow else "fits on one page")
            src.unlink()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
