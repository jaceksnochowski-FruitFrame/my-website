#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "journal"
OUTPUT_DIR = ROOT / "journal"
ASSETS_DIR = OUTPUT_DIR / "assets"


SITE_CSS = """
:root{
  --bg:#0a0a0a;
  --panel:#111111;
  --panel-2:#151515;
  --text:#f2ede5;
  --muted:rgba(242,237,229,0.72);
  --soft:rgba(242,237,229,0.46);
  --line:rgba(242,237,229,0.1);
  --accent:#b8864c;
  --shadow:0 24px 90px rgba(0,0,0,0.35);
  --max:1120px;
  --ease:cubic-bezier(.2,.8,.2,1);
  --headline:"Manrope", sans-serif;
  --body:"Manrope", sans-serif;
}

*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  color:var(--text);
  background:
    radial-gradient(circle at top left, rgba(184,134,76,0.08), transparent 30%),
    radial-gradient(circle at bottom right, rgba(242,237,229,0.04), transparent 28%),
    var(--bg);
  font-family:var(--body);
  -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility;
}

a{color:inherit}
img{display:block;max-width:100%}

.shell{
  min-height:100vh;
}

.topbar{
  position:sticky;
  top:0;
  z-index:20;
  backdrop-filter:blur(16px);
  background:rgba(10,10,10,0.88);
  border-bottom:1px solid var(--line);
}

.topbar-inner{
  width:min(calc(100% - 2rem), var(--max));
  margin:0 auto;
  padding:1rem 0;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
}

.brand{
  text-decoration:none;
  text-transform:uppercase;
  letter-spacing:0.05em;
  font-family:var(--headline);
  font-size:0.96rem;
}

.topnav{
  display:flex;
  flex-wrap:wrap;
  gap:1rem 1.5rem;
}

.topnav a{
  text-decoration:none;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:0.14em;
  font-size:0.72rem;
}

.topnav a:hover,
.topnav a.active{
  color:var(--text);
}

.page{
  width:min(calc(100% - 2rem), var(--max));
  margin:0 auto;
  padding:clamp(2rem, 5vw, 4rem) 0 clamp(4rem, 7vw, 6rem);
}

.hero{
  display:grid;
  gap:1.25rem;
  padding:clamp(2rem, 5vw, 4rem) 0 2rem;
  border-bottom:1px solid var(--line);
}

.eyebrow,
.meta,
.card-meta{
  text-transform:uppercase;
  letter-spacing:0.16em;
  color:var(--soft);
  font-size:0.72rem;
}

.hero h1,
.post-header h1{
  margin:0;
  font-family:var(--headline);
  text-transform:uppercase;
  line-height:0.95;
  letter-spacing:0.01em;
}

.hero h1{
  font-size:clamp(2.7rem, 7vw, 5.6rem);
  max-width:11ch;
}

.hero p,
.post-lead{
  margin:0;
  color:var(--muted);
  font-size:clamp(1.02rem, 1.8vw, 1.28rem);
  line-height:1.7;
  max-width:44rem;
}

.hero-actions{
  display:flex;
  flex-wrap:wrap;
  gap:0.9rem;
}

.btn,
.btn-ghost{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-height:48px;
  padding:0.95rem 1.35rem;
  text-decoration:none;
  text-transform:uppercase;
  letter-spacing:0.14em;
  font-size:0.78rem;
  transition:transform .25s var(--ease), border-color .25s var(--ease), background-color .25s var(--ease), color .25s var(--ease);
}

.btn{
  background:var(--text);
  color:var(--bg);
  border:1px solid var(--text);
}

.btn-ghost{
  background:rgba(242,237,229,0.04);
  border:1px solid rgba(242,237,229,0.22);
  color:var(--text);
}

.btn:hover,
.btn-ghost:hover{
  transform:translateY(-2px);
}

.posts{
  display:grid;
  gap:1.2rem;
  padding-top:2rem;
}

.post-card{
  display:grid;
  gap:0.8rem;
  text-decoration:none;
  background:linear-gradient(180deg, rgba(242,237,229,0.03), rgba(242,237,229,0.01));
  border:1px solid var(--line);
  box-shadow:var(--shadow);
  overflow:hidden;
}

.post-card-image{
  aspect-ratio:16/9;
  background:var(--panel);
}

.post-card-image img{
  width:100%;
  height:100%;
  object-fit:cover;
}

.post-card-body{
  display:grid;
  gap:0.8rem;
  padding:1.35rem;
}

.post-card h2{
  margin:0;
  font-family:var(--headline);
  text-transform:uppercase;
  letter-spacing:0.01em;
  line-height:1;
  font-size:clamp(1.5rem, 3vw, 2.5rem);
}

.post-card p{
  margin:0;
  color:var(--muted);
  line-height:1.7;
}

.tag-row{
  display:flex;
  flex-wrap:wrap;
  gap:0.55rem;
}

.tag{
  display:inline-flex;
  align-items:center;
  min-height:30px;
  padding:0.45rem 0.7rem;
  border:1px solid rgba(242,237,229,0.14);
  background:rgba(242,237,229,0.03);
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:0.14em;
  font-size:0.64rem;
}

.post-header{
  display:grid;
  gap:1rem;
  padding:clamp(2rem, 5vw, 4rem) 0 2rem;
  border-bottom:1px solid var(--line);
}

.post-cover{
  margin-top:1rem;
  border:1px solid var(--line);
  background:var(--panel);
  overflow:hidden;
  box-shadow:var(--shadow);
}

.post-cover img{
  width:100%;
  aspect-ratio:16/9;
  object-fit:cover;
}

.post-meta-row{
  display:flex;
  flex-wrap:wrap;
  gap:0.8rem 1rem;
}

.post-body{
  width:min(100%, 760px);
  padding-top:2rem;
}

.post-body > * + *{
  margin-top:1.15rem;
}

.post-body h2,
.post-body h3{
  margin:2.2rem 0 0.8rem;
  font-family:var(--headline);
  text-transform:uppercase;
  letter-spacing:0.01em;
  line-height:1;
}

.post-body h2{font-size:clamp(1.7rem, 3vw, 2.5rem)}
.post-body h3{font-size:clamp(1.25rem, 2.5vw, 1.7rem)}

.post-body p,
.post-body li,
.post-body blockquote{
  color:var(--muted);
  line-height:1.8;
  font-size:1.02rem;
}

.post-body p,
.post-body ul,
.post-body ol,
.post-body blockquote,
.post-body pre{
  margin:0;
}

.post-body ul,
.post-body ol{
  padding-left:1.3rem;
}

.post-body a{
  color:var(--text);
  text-decoration-color:rgba(184,134,76,0.7);
}

.post-body strong{color:var(--text)}

.post-body blockquote{
  padding:1rem 1.1rem;
  border-left:2px solid var(--accent);
  background:rgba(242,237,229,0.03);
}

.post-body code{
  font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size:0.92em;
  padding:0.15rem 0.35rem;
  background:rgba(242,237,229,0.06);
}

.post-body pre{
  overflow:auto;
  padding:1rem;
  border:1px solid var(--line);
  background:var(--panel);
}

.post-body pre code{
  padding:0;
  background:none;
}

.footer{
  padding-top:2rem;
  margin-top:3rem;
  border-top:1px solid var(--line);
  color:var(--soft);
  font-size:0.9rem;
}

@media (max-width: 760px){
  .topbar-inner,
  .page{
    width:min(calc(100% - 1.5rem), var(--max));
  }

  .topnav{
    gap:0.75rem 1rem;
  }

  .hero h1,
  .post-header h1{
    font-size:clamp(2.1rem, 11vw, 3.5rem);
  }

  .hero-actions{
    flex-direction:column;
    align-items:stretch;
  }
}
"""


@dataclass
class Post:
    title: str
    slug: str
    date: datetime
    excerpt: str
    categories: list[str]
    cover_image: str
    body_markdown: str
    body_html: str
    source_path: Path


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    _, rest = text.split("---\n", 1)
    frontmatter_text, body = rest.split("\n---\n", 1)
    metadata: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
      line = raw_line.strip()
      if not line or ":" not in line:
          continue
      key, value = line.split(":", 1)
      metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, body.strip()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value or "post"


def format_date(date_value: datetime) -> str:
    return date_value.strftime("%B %-d, %Y")


def inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    chunks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    quote_lines: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph if part.strip())
            chunks.append(f"<p>{inline_markdown(text)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            items = "".join(f"<li>{inline_markdown(item)}</li>" for item in list_items)
            chunks.append(f"<ul>{items}</ul>")
            list_items = []

    def flush_quote() -> None:
        nonlocal quote_lines
        if quote_lines:
            text = " ".join(part.strip() for part in quote_lines if part.strip())
            chunks.append(f"<blockquote>{inline_markdown(text)}</blockquote>")
            quote_lines = []

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_quote()
            if in_code:
                code_html = html.escape("\n".join(code_lines))
                chunks.append(f"<pre><code>{code_html}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_quote()
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flush_list()
            flush_quote()
            chunks.append(f"<h3>{inline_markdown(stripped[4:])}</h3>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            flush_quote()
            chunks.append(f"<h2>{inline_markdown(stripped[3:])}</h2>")
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_list()
            flush_quote()
            chunks.append(f"<h1>{inline_markdown(stripped[2:])}</h1>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_list()
            quote_lines.append(stripped[2:])
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            flush_quote()
            list_items.append(stripped[2:])
            continue

        flush_list()
        flush_quote()
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_quote()

    return "\n".join(chunks)


def load_posts() -> list[Post]:
    posts: list[Post] = []
    for source_path in sorted(CONTENT_DIR.glob("*.md")):
        raw_text = source_path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(raw_text)
        title = metadata.get("title") or source_path.stem
        slug = metadata.get("slug") or slugify(title)
        date_raw = metadata.get("date") or datetime.now().strftime("%Y-%m-%d")
        date_value = datetime.strptime(date_raw, "%Y-%m-%d")
        excerpt = metadata.get("excerpt") or body.split("\n", 1)[0].strip()
        categories_raw = metadata.get("categories", "")
        categories = [item.strip() for item in categories_raw.split(",") if item.strip()]
        cover_image = metadata.get("cover_image", "").strip()
        posts.append(
            Post(
                title=title,
                slug=slug,
                date=date_value,
                excerpt=excerpt,
                categories=categories,
                cover_image=cover_image,
                body_markdown=body,
                body_html=markdown_to_html(body),
                source_path=source_path,
            )
        )
    posts.sort(key=lambda post: post.date, reverse=True)
    return posts


def render_layout(title: str, description: str, body: str, canonical_path: str, active: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#0a0a0a">
<link rel="canonical" href="https://jaceksnochowski.com{canonical_path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/journal/assets/journal.css">
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="topbar-inner">
        <a class="brand" href="/">Jacek Snochowski</a>
        <nav class="topnav" aria-label="Primary">
          <a href="/">Home</a>
          <a class="{active if active == 'journal' else ''}" href="/journal/">Journal</a>
          <a href="/#work">Work</a>
          <a href="/#about">About</a>
          <a href="/#contact">Contact</a>
        </nav>
      </div>
    </header>
    <main class="page">
      {body}
    </main>
  </div>
</body>
</html>
"""


def build_index(posts: list[Post]) -> str:
    cards = []
    for post in posts:
        cover_html = ""
        if post.cover_image:
            cover_html = f"""
  <div class="post-card-image">
    <img src="{html.escape(post.cover_image)}" alt="{html.escape(post.title)}">
  </div>"""
        category_html = ""
        if post.categories:
            tags = "".join(f'<span class="tag">{html.escape(category)}</span>' for category in post.categories)
            category_html = f'<div class="tag-row">{tags}</div>'
        cards.append(
            f"""
<a class="post-card" href="/journal/{post.slug}/">
  {cover_html}
  <div class="post-card-body">
    <div class="card-meta">{format_date(post.date)}</div>
    <h2>{html.escape(post.title)}</h2>
    <p>{html.escape(post.excerpt)}</p>
    {category_html}
  </div>
</a>
"""
        )

    body = f"""
<section class="hero">
  <div class="eyebrow">Weekly Notes</div>
  <h1>Journal</h1>
  <p>A weekly space for behind-the-scenes thoughts on cinematography, movement, prep, lighting, operating, and how I approach commercial and performance-led work.</p>
  <div class="hero-actions">
    <a class="btn" href="mailto:jaceksnochowski@gmail.com">Get In Touch</a>
    <a class="btn-ghost" href="/#work">View Selected Work</a>
  </div>
</section>
<section class="posts">
  {''.join(cards)}
</section>
<div class="footer">New posts can be written in Markdown and rebuilt locally before pushing to GitHub.</div>
"""

    return render_layout(
        title="Journal | Jacek Snochowski",
        description="Weekly journal entries from Jacek Snochowski on cinematography, movement, prep, lighting, and commercial filmmaking.",
        body=body,
        canonical_path="/journal/",
        active="journal",
    )


def build_post(post: Post) -> str:
    category_html = ""
    if post.categories:
        tags = "".join(f'<span class="tag">{html.escape(category)}</span>' for category in post.categories)
        category_html = f'<div class="tag-row">{tags}</div>'
    cover_html = ""
    if post.cover_image:
        cover_html = f"""
    <div class="post-cover">
      <img src="{html.escape(post.cover_image)}" alt="{html.escape(post.title)}">
    </div>"""
    body = f"""
<article>
  <header class="post-header">
    <div class="eyebrow">Journal</div>
    <h1>{html.escape(post.title)}</h1>
    <div class="post-meta-row">
      <div class="meta">{format_date(post.date)}</div>
      <div class="meta">Jacek Snochowski</div>
    </div>
    {category_html}
    <p class="post-lead">{html.escape(post.excerpt)}</p>
    {cover_html}
  </header>
  <div class="post-body">
    {post.body_html}
  </div>
</article>
<div class="footer"><a href="/journal/">Back to the Journal</a></div>
"""

    return render_layout(
        title=f"{post.title} | Journal | Jacek Snochowski",
        description=post.excerpt,
        body=body,
        canonical_path=f"/journal/{post.slug}/",
        active="journal",
    )


def write_site(posts: list[Post]) -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "journal.css").write_text(SITE_CSS.strip() + "\n", encoding="utf-8")

    (OUTPUT_DIR / "index.html").write_text(build_index(posts), encoding="utf-8")
    valid_slugs = {post.slug for post in posts}

    for path in OUTPUT_DIR.iterdir():
        if not path.is_dir():
            continue
        if path.name == "assets":
            continue
        if path.name not in valid_slugs:
            shutil.rmtree(path)

    for post in posts:
        post_dir = OUTPUT_DIR / post.slug
        if post_dir.exists():
            shutil.rmtree(post_dir)
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.html").write_text(build_post(post), encoding="utf-8")


def main() -> None:
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    posts = load_posts()
    write_site(posts)
    print(f"Built {len(posts)} journal post(s) into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
