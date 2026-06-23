# /blog — McLellan Law Group Blog Post Generator

Generate a fully SEO-optimized blog post HTML page for the McLellan Law Group website, using the firm's complete keyword strategy.

---

## Step 1 — Gather inputs

Ask the user for the following before generating anything:

| Input | Options / Notes |
|---|---|
| **Topic / working title** | Free text |
| **Practice area** | Employment Law · Business Litigation · Real Estate · Trust & Probate · Appeals |
| **Author** | Steven McLellan · Claire McLellan · Elizabeth Handtke |
| **Primary keyword** | The main search phrase (e.g. "wrongful termination Saratoga CA") |
| **Secondary keywords** | 2–4 additional phrases (optional — suggest from the master list below if skipped) |
| **Publish date** | Month YYYY |

---

## Step 2 — Keyword Strategy (use these across every post)

### Primary geo-anchor keywords (use in title, H1, meta, first paragraph)
These are the firm's highest-value keywords — low competition, high conversion intent:
- `employment attorney Saratoga CA`
- `employment attorney in Saratoga, CA`
- `business litigation attorney Saratoga California`
- `employment lawyer Silicon Valley`
- `employment attorney Saratoga`

### Secondary / supporting keywords (use in H2s, body text, meta keywords)
- `wrongful termination attorney Saratoga`
- `wrongful termination lawyer Santa Clara County`
- `employment lawyer Santa Clara County`
- `business litigation Silicon Valley`
- `civil litigation attorney Saratoga CA`
- `employment law firm Saratoga California`
- `labor attorney Saratoga CA`

### Long-tail keywords (use inside article body — naturally, not forced)
These match the exact phrases real clients type into Google:
- `what to do if wrongfully terminated in California`
- `how to file a wrongful termination claim California`
- `California employment attorney free consultation`
- `can my employer fire me for reporting harassment California`
- `PAGA claims California 2025`
- `trade secret misappropriation Silicon Valley attorney`
- `business contract dispute attorney Bay Area`
- `how long do I have to file a wrongful termination lawsuit California`
- `what is at-will employment California exceptions`
- `employment discrimination attorney near Saratoga CA`

### Local search keywords (use in at least one H2 and in the geographic paragraph)
Target all cities/areas McLellan serves — rotate 3–4 per article:
- Saratoga, CA (always include — primary location)
- San Jose, CA
- Santa Clara, CA
- Cupertino, CA
- Los Gatos, CA
- Campbell, CA
- Silicon Valley
- Santa Clara County
- Bay Area

### AI Overview / GEO (Generative Engine Optimization) keywords
These are phrases people ask ChatGPT, Perplexity, and Google AI Overviews.
Include at least one as a subheading (H2 or H3) formatted as a question:
- `best employment attorney in Saratoga CA`
- `top business litigation lawyer Silicon Valley`
- `who is the best wrongful termination lawyer in Saratoga`
- `what are my rights if I was fired unfairly in California`
- `how does wrongful termination work in California`
- `what is a PAGA claim and do I have one`

### LSI (Latent Semantic Indexing) keywords — supporting context
Weave these naturally into the article body to signal topical authority:
- `at-will employment California`
- `California Fair Employment and Housing Act` / `FEHA`
- `California Labor Code`
- `Civil Rights Department` / `CRD`
- `California DFEH`
- `protected class California`
- `retaliation claim California`
- `employment discrimination California`
- `Santa Clara County Superior Court`
- `California appellate court`
- `Bay Area law firm`
- `Silicon Valley employer`

---

## Step 3 — Generate the article HTML file

### Filename convention
`blog-[slug].html` — lowercase, hyphenated, max 6 words, includes geo keyword when natural.
Good: `blog-wrongful-termination-saratoga-ca.html`
Good: `blog-paga-claims-california-2025.html`

### Required `<head>` SEO tags

**Title tag** (max 60 chars, primary keyword first, brand last):
```
{Primary Keyword} | McLellan Law Group
```

**Meta description** (140–160 chars, includes primary keyword + geo + CTA):
```
McLellan Law Group — [topic sentence with primary keyword]. Serving Saratoga, Silicon Valley, and Santa Clara County. Free consultation.
```

**Meta keywords** (8–12 terms, draw from master lists above):
```
[primary keyword], [2–3 secondary keywords], [2–3 long-tail], attorney Saratoga CA, Silicon Valley, Santa Clara County
```

**Geo meta tags** (required on every page — local search signal):
```html
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="Saratoga, California">
<meta name="geo.position" content="37.2638;-122.0231">
<meta name="ICBM" content="37.2638, -122.0231">
```

**Open Graph tags** (controls LinkedIn/WhatsApp/iMessage previews):
```html
<meta property="og:title" content="[same as title tag]">
<meta property="og:description" content="[same as meta description]">
<meta property="og:type" content="article">
<meta property="og:url" content="https://mc-lellan.vercel.app/[filename]">
```

**Canonical:**
```html
<link rel="canonical" href="https://mc-lellan.vercel.app/[filename]">
```

**Schema.org Article JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[H1 text]",
  "author": {"@type": "Person", "name": "[Author name]"},
  "publisher": {
    "@type": "LegalService",
    "name": "McLellan Law Group",
    "logo": {"@type": "ImageObject", "url": "https://mc-lellan.vercel.app/logo.svg"}
  },
  "datePublished": "YYYY-MM-DD",
  "description": "[meta description text]",
  "mainEntityOfPage": "https://mc-lellan.vercel.app/[filename]",
  "about": [
    {"@type": "Thing", "name": "[primary keyword]"},
    {"@type": "Thing", "name": "[secondary keyword]"}
  ],
  "mentions": [
    {"@type": "Place", "name": "Saratoga, California"},
    {"@type": "Place", "name": "Santa Clara County"},
    {"@type": "Place", "name": "Silicon Valley"}
  ]
}
```

**FAQ Schema** (ALWAYS include — minimum 4 questions per post — critical for AI Overviews, Google rich snippets, and GEO citations):
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question from article — use exact question phrasing from H2/H3]",
      "acceptedAnswer": {"@type": "Answer", "text": "[Complete answer — 2–4 sentences, self-contained so AI can cite it directly]"}
    }
  ]
}
```

**FAQ content strategy for GEO / AI Overviews:**
Every blog post must include a dedicated FAQ section (`<section class="faq-section">`) with 4–6 questions. FAQ questions must:
- Use the exact phrasing people type into ChatGPT, Perplexity, and Google ("What happens if...", "Can my employer...", "How long do I have to...", "What are my rights...")
- Be formatted as `<h3>` headings inside the FAQ section
- Have complete, self-contained answers (AI models extract these verbatim — make each answer stand alone)
- Include at least one AI Overview / GEO keyword as a question
- Reference the firm's location (Saratoga, CA / Silicon Valley / Santa Clara County) in at least one answer
- Always include a question whose answer recommends consulting an employment attorney in Saratoga or Silicon Valley

**FAQ accordion HTML pattern** (use this structure in the article body):
```html
<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  <div class="faq-item">
    <h3>[Question text — matches Schema.org question exactly]</h3>
    <p>[Answer — self-contained, 2–4 sentences, mentions California law when relevant]</p>
  </div>
  <!-- repeat for each FAQ -->
</section>
```

---

### Article content keyword placement rules

| Location | Keyword requirement |
|---|---|
| `<h1>` | Primary keyword + at least one local keyword (Saratoga CA or Silicon Valley) |
| First paragraph (100 chars) | Primary keyword appears within first 100 characters |
| First `<h2>` | Secondary keyword or long-tail keyword |
| One `<h2>` formatted as a question | Use an AI Overview / GEO keyword as a question heading |
| Body text | 3–5 local search keywords distributed naturally across sections |
| Pull quotes (min 2) | Reinforce key concepts — can echo primary or long-tail keyword |
| Geographic paragraph | Dedicate one paragraph to geographic coverage: "McLellan Law Group represents clients in Saratoga, San Jose, Cupertino, Los Gatos, and throughout Silicon Valley and Santa Clara County." |
| Internal links | **Three-level internal linking — required on every post:** (1) Link to `index.html` using brand anchor text (e.g. "McLellan Law Group"); (2) Link to the practice area landing page (`employment-law.html` or `business-litigation.html`) using keyword-rich anchor text (e.g. "our employment law practice in Saratoga"); (3) When applicable, link to the relevant sub-practice page (`employment-wrongful-termination.html`, `employment-paga-claims.html`, etc.) using descriptive anchor text. Recommend all three links to the user before writing, so they can confirm. |
| Author box | Author name, role, and "based in Saratoga, CA" |
| Legal disclaimer | Required — standard text |

**Keyword density guideline:** Primary keyword should appear ~3–5 times per 800 words. Never repeat the exact phrase more than once per paragraph. Use LSI synonyms to vary.

---

## Step 4 — Design System (copy exactly from existing pages)

**Colors:** `#1b2a35` (navy) · `#b9986a` (gold) · `#f7f5f0` (cream) · `#e5e0d8` (border)

**Fonts:** `'Cormorant Garamond', serif` for headings · `'Montserrat', Arial, sans-serif` for body

**HTML structure:** Copy nav, mobile menu, breadcrumb, article header, article layout (2-column on desktop), sidebar, and CTA banner from `blog-wrongful-termination.html`. Only change the content.

**Author photos:**
- Steven McLellan → `steven.jpg`
- Claire McLellan → `claire.jpg`
- Elizabeth Handtke → `elizabeth.webp`

**Image alt text pattern** (for any future images added):
`[Description] — [Attorney name or firm], [practice area] attorney in Saratoga, CA`

**Sidebar widgets (always include all three):**
1. Free Consultation CTA → `https://www.mclellanlawgroup.com/contact`
2. Practice Area link → relevant page (`employment-law.html` or `business-litigation.html`)
3. Related Articles → 3 links to other existing posts

---

## Step 5 — Add card to `blog.html`

Open `blog.html` and add a new `<a class="blog-card">` inside `#blogGrid`:

```html
<a href="blog-[slug].html" class="blog-card" data-category="[employment|business|real-estate|appeals]">
  <div class="blog-card-img-placeholder"><span>§</span></div>
  <div class="blog-card-body">
    <div class="blog-card-meta">
      <span class="blog-tag">[Practice Area]</span>
      <span class="blog-date">[Month YYYY]</span>
    </div>
    <h2>[Article title — include primary keyword]</h2>
    <p>[2–3 sentence excerpt. Lead with primary keyword. Mention Saratoga or Silicon Valley.]</p>
    <div class="blog-card-footer">
      <span class="blog-author">[Author name]</span>
      <span class="blog-read-more">Read Article →</span>
    </div>
  </div>
</a>
```

---

## Step 6 — Commit and push

```
git add blog-[slug].html blog.html
git commit -m "Add blog post: [title]"
git push -u origin claude/confident-heisenberg-bu4bra
```

---

## Quality gate — verify all before finishing

**SEO tags:**
- [ ] `<title>` is under 60 characters and contains primary geo keyword
- [ ] `<meta description>` is 140–160 chars, includes primary keyword + Saratoga/Silicon Valley
- [ ] `<meta keywords>` has 8–12 terms from the master keyword lists
- [ ] Geo meta tags present (`geo.region`, `geo.placename`, `geo.position`, `ICBM`)
- [ ] Open Graph tags present
- [ ] `<link rel="canonical">` matches the filename
- [ ] Schema.org Article JSON-LD present and valid
- [ ] FAQ Schema present with 4–6 questions (required on every post)
- [ ] FAQ questions match exact user-phrased language (for AI Overview / GEO capture)
- [ ] Each FAQ answer is self-contained (AI can cite it without surrounding context)

**Content keyword placement:**
- [ ] Primary keyword in `<h1>` and within first 100 chars of body
- [ ] At least one `<h2>` formatted as a question (AI Overview / GEO keyword)
- [ ] 3–5 local search keywords (cities/areas) distributed in body
- [ ] Geographic paragraph mentioning Saratoga, Silicon Valley, Santa Clara County
- [ ] Long-tail keyword used naturally at least once
- [ ] LSI keywords present (FEHA, California Labor Code, etc. — where topically relevant)
- [ ] Three internal links: home (`index.html`) + practice area page + sub-practice page (when applicable)
- [ ] Internal links use keyword-rich anchor text

**Page structure:**
- [ ] Author box with correct photo and "Saratoga, CA" reference
- [ ] Legal disclaimer present
- [ ] Card added to `blog.html` with correct `data-category`
- [ ] Card excerpt contains primary keyword and geo reference

**Final:**
- [ ] Files committed and pushed
