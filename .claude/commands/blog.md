# /blog — McLellan Law Group Blog Post Generator

Generate a fully SEO-optimized blog post HTML page for the McLellan Law Group website.

## Instructions

The user will provide a topic, practice area, and optionally an author and target keywords. Use those inputs to generate a complete, publish-ready HTML file that:

1. Matches the existing site design exactly (see Design System below)
2. Is fully SEO-optimized (see SEO Checklist below)
3. Adds the new post as a card to `blog.html`

---

## Step 1 — Gather inputs

If the user hasn't provided all of the following, ask before proceeding:

| Input | Options |
|---|---|
| **Topic / working title** | Free text |
| **Practice area** | Employment Law · Business Litigation · Real Estate · Trust & Probate · Appeals |
| **Author** | Steven McLellan · Claire McLellan · Elizabeth Handtke |
| **Primary keyword** | The main search phrase to rank for (e.g. "wrongful termination California") |
| **Secondary keywords** | 2–4 related phrases (optional, but ask) |

---

## Step 2 — Generate the article HTML file

### Filename convention
`blog-[slug].html` where slug is lowercase, hyphenated, max 6 words.
Example: `blog-paga-claims-california-2025.html`

### SEO Checklist — every post MUST include all of these:

**`<head>` meta tags:**
- `<title>` — Primary keyword near the front, brand at the end, max 60 chars. Pattern: `{Topic} | McLellan Law Group`
- `<meta name="description">` — 140–160 chars, includes primary keyword, includes a call to action or benefit, no keyword stuffing
- `<meta name="keywords">` — 5–8 terms: primary keyword, secondary keywords, "attorney Saratoga", "Silicon Valley", practice area
- `<meta property="og:title">` and `<meta property="og:description">` — for social sharing
- `<link rel="canonical">` — `https://mc-lellan.vercel.app/[filename]`

**Schema.org structured data (`<script type="application/ld+json">`):**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "author": {"@type": "Person", "name": "..."},
  "publisher": {
    "@type": "LegalService",
    "name": "McLellan Law Group",
    "logo": {"@type": "ImageObject", "url": "https://mc-lellan.vercel.app/logo.svg"}
  },
  "datePublished": "YYYY-MM-DD",
  "description": "...",
  "mainEntityOfPage": "https://mc-lellan.vercel.app/[filename]"
}
```

**Article content SEO rules:**
- `<h1>` — Contains primary keyword, written as a question or clear statement of value, max 70 chars
- First `<p>` — Leads with primary keyword within the first 100 characters
- `<h2>` headings — Each covers a subtopic that matches likely search queries; use secondary keywords naturally
- Internal links — Link to the relevant practice area page (`employment-law.html` or `business-litigation.html`) at least once
- Pull quotes — At least 2 pull quotes that reinforce key points
- Article length — Minimum 600 words of substantive legal content (not filler)
- Author attribution — Author box at the bottom with name, role, and 1–2 sentence bio
- Legal disclaimer — Required at bottom of every article

---

## Step 3 — Design System (copy exactly from existing pages)

**Colors:**
- Dark navy: `#1b2a35`
- Gold accent: `#b9986a`
- Cream background: `#f7f5f0`
- Border: `#e5e0d8`

**Fonts:**
- Headings: `'Cormorant Garamond', serif` (font-weight 700–900)
- Body: `'Montserrat', Arial, sans-serif`

**Structure:** Copy the full nav, mobile menu, breadcrumb, article header, article layout, sidebar, and CTA banner from `blog-wrongful-termination.html`. Only change the content.

**Sidebar widgets (always include all three):**
1. Free Consultation CTA → links to `https://www.mclellanlawgroup.com/contact`
2. Practice Area link → relevant page
3. Related Articles → 3 links to other posts in `blog.html`

---

## Step 4 — Add a card to `blog.html`

After creating the article file, open `blog.html` and add a new `<a class="blog-card">` entry inside `#blogGrid`. Follow the existing card pattern:

```html
<a href="blog-[slug].html" class="blog-card" data-category="[employment|business|real-estate|appeals]">
  <div class="blog-card-img-placeholder"><span>§</span></div>
  <div class="blog-card-body">
    <div class="blog-card-meta">
      <span class="blog-tag">[Practice Area]</span>
      <span class="blog-date">[Month YYYY]</span>
    </div>
    <h2>[Article title]</h2>
    <p>[2–3 sentence excerpt that uses the primary keyword naturally]</p>
    <div class="blog-card-footer">
      <span class="blog-author">[Author name]</span>
      <span class="blog-read-more">Read Article →</span>
    </div>
  </div>
</a>
```

---

## Step 5 — Commit and push

```
git add blog-[slug].html blog.html
git commit -m "Add blog post: [title]"
git push -u origin claude/confident-heisenberg-bu4bra
```

---

## Quality gate — before finishing, verify:

- [ ] `<title>` is under 60 characters
- [ ] `<meta name="description">` is 140–160 characters
- [ ] Primary keyword appears in `<h1>`, first paragraph, at least 2 `<h2>`s, and meta description
- [ ] Schema.org Article JSON-LD is present and valid
- [ ] `<link rel="canonical">` matches the actual filename
- [ ] Internal link to practice area page is present
- [ ] Author box with correct photo (`steven.jpg`, `claire.jpg`, or `elizabeth.webp`)
- [ ] Legal disclaimer is present
- [ ] Card added to `blog.html` with correct `data-category`
- [ ] Files committed and pushed
