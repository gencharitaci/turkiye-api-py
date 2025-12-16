import json
import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from app.i18n import get_translations


def get_scalar_html(app: FastAPI, lang: Literal["en", "tr"] = "en") -> str:
    """Generate Scalar API documentation HTML with language support"""
    openapi_url = f"/openapi-{lang}.json"

    # Load translations
    translations = get_translations(lang)
    page_title = f"{app.title} - {translations['docs']['title']}"

    # Load Scalar configuration
    config_path = os.path.join("app", "scalar.config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            scalar_config = json.load(f)
    else:
        scalar_config = {"theme": "purple", "layout": "modern", "darkMode": True}

    # Convert config to JSON string for inline embedding
    config_json = json.dumps(scalar_config)

    return f"""
    <!doctype html>
    <html lang="{lang}">
      <head>
        <title>{page_title}</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <script
          id="api-reference"
          data-url="{openapi_url}"
          data-configuration='{config_json}'
        ></script>

        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """


def setup_scalar_docs(app: FastAPI):
    """Add Scalar documentation endpoints with multi-language support to FastAPI app"""
    from pathlib import Path

    from fastapi.staticfiles import StaticFiles

    # Mount static assets for guides
    guides_path = Path("guides")
    if guides_path.exists():
        app.mount("/guides/assets", StaticFiles(directory="guides/assets"), name="guide-assets")

    @app.get("/docs", include_in_schema=False)
    async def scalar_html_default():
        """API Documentation - Defaults to English"""
        return HTMLResponse(get_scalar_html(app, lang="en"))

    @app.get("/docs/en", include_in_schema=False)
    async def scalar_html_en():
        """English API Documentation"""
        return HTMLResponse(get_scalar_html(app, lang="en"))

    @app.get("/docs/tr", include_in_schema=False)
    async def scalar_html_tr():
        """Turkish API Documentation"""
        return HTMLResponse(get_scalar_html(app, lang="tr"))

    @app.get("/scalar-config", include_in_schema=False)
    async def scalar_config():
        """Serve Scalar configuration from app/scalar.config.json"""
        config_path = os.path.join("app", "scalar.config.json")

        # Load and return the configuration
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            return config_data
        else:
            # Return minimal config if file doesn't exist
            return {"theme": "purple", "layout": "modern", "darkMode": True}

    @app.get("/guides/en", include_in_schema=False)
    @app.get("/guides/en/", include_in_schema=False)
    async def guides_en_index():
        """English Guides Index"""
        return await serve_guide_page("en", "index.md")

    @app.get("/guides/tr", include_in_schema=False)
    @app.get("/guides/tr/", include_in_schema=False)
    async def guides_tr_index():
        """Turkish Guides Index"""
        return await serve_guide_page("tr", "index.md")

    @app.get("/guides/en/{guide_path:path}", include_in_schema=False)
    async def guides_en_page(guide_path: str):
        """English Guide Pages"""
        return await serve_guide_page("en", guide_path)

    @app.get("/guides/tr/{guide_path:path}", include_in_schema=False)
    async def guides_tr_page(guide_path: str):
        """Turkish Guide Pages"""
        return await serve_guide_page("tr", guide_path)

    @app.get("/api/guides/en/list", include_in_schema=False)
    async def list_guides_en():
        """List all English guides"""
        return await list_guides("en")

    @app.get("/api/guides/tr/list", include_in_schema=False)
    async def list_guides_tr():
        """List all Turkish guides"""
        return await list_guides("tr")


async def serve_guide_page(lang: str, guide_path: str):
    """Serve a guide page with professional markdown rendering"""
    import re
    from pathlib import Path

    import frontmatter
    from markdown import markdown
    from pygments.formatters import HtmlFormatter

    # Ensure .md extension
    if not guide_path.endswith(".md"):
        guide_path = f"{guide_path}.md"

    # Construct full path
    full_path = Path("guides") / lang / guide_path

    if not full_path.exists():
        return HTMLResponse(content="<h1>Guide not found</h1>", status_code=404)

    # Parse frontmatter and content
    with open(full_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    # Extract metadata
    title = post.get("title", "Guide")
    description = post.get("description", "")

    # Generate TOC from content
    toc_html = ""
    headings = []
    for line in post.content.split("\n"):
        match = re.match(r"^(#{2,3})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            slug = text.lower().replace(" ", "-").replace("?", "").replace("!", "")
            headings.append({"level": level, "text": text, "slug": slug})

    if headings:
        toc_html = '<div class="on-this-page"><div class="otp-title">On This Page</div><ul class="otp-list">'
        # Add page title as first item
        toc_html += f'<li class="otp-item level-1"><a href="#" class="otp-link">{title}</a></li>'
        for h in headings:
            toc_html += (
                f'<li class="otp-item level-{h["level"]}"><a href="#{h["slug"]}" class="otp-link">{h["text"]}</a></li>'
            )
        toc_html += "</ul></div>"

    # Convert markdown to HTML with extensions
    html_content = markdown(
        post.content,
        extensions=["extra", "codehilite", "toc", "fenced_code", "tables", "attr_list", "def_list"],
        extension_configs={"codehilite": {"css_class": "highlight", "linenums": False}},
    )

    # Get Pygments CSS for syntax highlighting
    formatter = HtmlFormatter(style="monokai")
    pygments_css = formatter.get_style_defs(".highlight")

    # Build sidebar navigation
    guides_dir = Path("guides") / lang
    sidebar_html = build_sidebar(guides_dir, lang, guide_path)

    # Professional documentation template
    page_html = f"""
    <!doctype html>
    <html lang="{lang}">
      <head>
        <title>{title} | Türkiye API</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="{description}" />
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        >
        <style>
          /* Scalar's exact design system */
          * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }}

          :root {{
            --scalar-purple: #8b5cf6;
            --scalar-purple-light: #a78bfa;

            /* Light mode */
            --bg-1: #ffffff;
            --bg-2: #fafafa;
            --bg-3: #f5f5f5;
            --text-1: #171717;
            --text-2: #525252;
            --text-3: #737373;
            --border: #e5e5e5;

            /* Sidebar */
            --sidebar-bg: #ffffff;
            --sidebar-text: #171717;
            --sidebar-text-muted: #737373;
            --sidebar-hover: #fafafa;
            --sidebar-active-bg: #fafafa;
            --sidebar-active-text: #171717;
            --sidebar-border: #e5e5e5;
          }}

          @media (prefers-color-scheme: dark) {{
            :root {{
              --bg-1: #0a0a0a;
              --bg-2: #171717;
              --bg-3: #262626;
              --text-1: #fafafa;
              --text-2: #a3a3a3;
              --text-3: #737373;
              --border: #262626;

              --sidebar-bg: #0a0a0a;
              --sidebar-text: #fafafa;
              --sidebar-text-muted: #737373;
              --sidebar-hover: #171717;
              --sidebar-active-bg: #171717;
              --sidebar-active-text: #fafafa;
              --sidebar-border: #262626;
            }}
          }}

          body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-1);
            color: var(--text-1);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
          }}

          .page-container {{
            display: flex;
            min-height: 100vh;
          }}

          /* Left Sidebar */
          .sidebar {{
            width: 280px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--sidebar-border);
            position: fixed;
            height: 100vh;
            display: flex;
            flex-direction: column;
            left: 0;
            top: 0;
            z-index: 100;
          }}

          .sidebar-header {{
            padding: 16px;
          }}

          .search-box {{
            background: var(--bg-1);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-3);
            font-size: 13px;
            cursor: text;
          }}

          .search-icon {{
            width: 14px;
            height: 14px;
            opacity: 0.7;
          }}

          .sidebar-nav {{
            flex: 1;
            overflow-y: auto;
            padding: 0 12px 16px;
          }}

          .nav-section {{
            margin-bottom: 24px;
          }}

          .nav-section-title {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--sidebar-text-muted);
            padding: 8px 12px 4px;
            margin-bottom: 4px;
          }}

          .nav-list {{
            list-style: none;
          }}

          .nav-item {{
            margin-bottom: 1px;
          }}

          .nav-link {{
            display: block;
            padding: 6px 12px;
            color: var(--sidebar-text);
            text-decoration: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.15s ease;
          }}

          .nav-link:hover {{
            background: var(--sidebar-hover);
          }}

          .nav-link.active {{
            background: var(--sidebar-active-bg);
            color: var(--sidebar-active-text);
            font-weight: 600;
          }}

          .sidebar-footer {{
            padding: 16px;
            border-top: 1px solid var(--sidebar-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
          }}

          .theme-toggle {{
            background: none;
            border: none;
            cursor: pointer;
            color: var(--text-3);
            padding: 4px;
            border-radius: 4px;
          }}

          .theme-toggle:hover {{
            background: var(--bg-2);
            color: var(--text-1);
          }}

          /* Main content wrapper */
          .main-wrapper {{
            flex: 1;
            margin-left: 280px;
            display: flex;
            flex-direction: column;
          }}

          .top-bar {{
            height: 60px;
            background: var(--bg-1);
            border-bottom: 1px solid var(--border);
            padding: 0 32px;
            position: sticky;
            top: 0;
            z-index: 50;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }}

          .breadcrumb {{
            display: flex;
            gap: 8px;
            align-items: center;
            font-size: 14px;
            font-weight: 500;
          }}

          .breadcrumb a {{
            color: var(--text-1);
            text-decoration: none;
          }}

          .breadcrumb-separator {{
            color: var(--text-3);
          }}

          .content-container {{
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
          }}

          /* Content area */
          .content {{
            flex: 1;
            padding: 48px 64px 96px 32px;
            max-width: 900px;
          }}

          .content h1 {{
            font-size: 32px;
            font-weight: 700;
            color: var(--text-1);
            margin-bottom: 16px;
            line-height: 1.2;
            letter-spacing: -0.02em;
          }}

          .content h2 {{
            font-size: 24px;
            font-weight: 600;
            color: var(--text-1);
            margin-top: 40px;
            margin-bottom: 16px;
            letter-spacing: -0.01em;
          }}

          .content h3 {{
            font-size: 20px;
            font-weight: 600;
            color: var(--text-1);
            margin-top: 32px;
            margin-bottom: 12px;
          }}

          .content p {{
            margin-bottom: 16px;
            color: var(--text-2);
            line-height: 1.7;
            font-size: 15px;
          }}

          .content a {{
            color: var(--text-1);
            text-decoration: underline;
            text-decoration-color: var(--border);
            text-underline-offset: 4px;
            transition: all 0.15s;
          }}

          .content a:hover {{
            text-decoration-color: var(--text-1);
          }}

          .content code {{
            background: var(--bg-2);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
            font-size: 13px;
            color: var(--text-1);
            border: 1px solid var(--border);
          }}

          .content pre {{
            background: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 24px 0;
            border: 1px solid #333;
          }}

          .content pre code {{
            background: none;
            padding: 0;
            border: none;
            color: #e2e8f0;
            font-size: 13px;
            line-height: 1.6;
          }}

          /* Right Sidebar (TOC) */
          .right-sidebar {{
            width: 240px;
            padding: 48px 32px 0 0;
            position: sticky;
            top: 60px;
            height: calc(100vh - 60px);
            overflow-y: auto;
          }}

          .otp-title {{
            font-size: 12px;
            font-weight: 600;
            color: var(--text-3);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }}

          .otp-list {{
            list-style: none;
            border-left: 1px solid var(--border);
          }}

          .otp-item {{
            margin-bottom: 0;
          }}

          .otp-link {{
            display: block;
            padding: 4px 0 4px 16px;
            color: var(--text-3);
            text-decoration: none;
            font-size: 13px;
            border-left: 1px solid transparent;
            margin-left: -1px;
            transition: all 0.15s;
          }}

          .otp-link:hover {{
            color: var(--text-1);
            border-left-color: var(--text-3);
          }}

          .otp-item.level-1 .otp-link {{
            font-weight: 600;
            color: var(--text-1);
            border-left-color: var(--text-1);
          }}

          .otp-item.level-3 .otp-link {{
            padding-left: 28px;
          }}

          {pygments_css}

          @media (max-width: 1024px) {{
            .right-sidebar {{
              display: none;
            }}
            .content {{
              padding-right: 32px;
            }}
          }}

          @media (max-width: 768px) {{
            .sidebar {{
              transform: translateX(-100%);
            }}
            .main-wrapper {{
              margin-left: 0;
            }}
            .content {{
              padding: 24px 16px;
            }}
          }}
        </style>
      </head>
      <body>
        <div class="page-container">
          <aside class="sidebar">
            <div class="sidebar-header">
              <div class="search-box">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <span>Find Anything</span>
              </div>
            </div>
            <nav class="sidebar-nav">
              {sidebar_html}
            </nav>
            <div class="sidebar-footer">
              <button class="theme-toggle" onclick="toggleTheme()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="5"></circle>
                  <line x1="12" y1="1" x2="12" y2="3"></line>
                  <line x1="12" y1="21" x2="12" y2="23"></line>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                  <line x1="1" y1="12" x2="3" y2="12"></line>
                  <line x1="21" y1="12" x2="23" y2="12"></line>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
              </button>
            </div>
          </aside>

          <div class="main-wrapper">
            <div class="top-bar">
              <div class="breadcrumb">
                <a href="/guides/{lang}">Introduction</a>
              </div>
              <div class="lang-switcher">
                <a href="/guides/{'tr' if lang == 'en' else 'en'}/{guide_path}" class="nav-link">
                  {'🇹🇷 Türkçe' if lang == 'en' else '🇬🇧 English'}
                </a>
              </div>
            </div>

            <div class="content-container">
              <article class="content">
                {html_content}
              </article>
              <aside class="right-sidebar">
                {toc_html}
              </aside>
            </div>
          </div>
        </div>
        <script>
          function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('class');
            if (current === 'dark') {{
              html.removeAttribute('class');
              localStorage.setItem('theme', 'light');
            }} else {{
              html.setAttribute('class', 'dark');
              localStorage.setItem('theme', 'dark');
            }}
          }}

          // Init theme
          if (localStorage.getItem('theme') === 'dark' ||
              (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.setAttribute('class', 'dark');
          }}
        </script>
      </body>
    </html>
    """

    return HTMLResponse(content=page_html)


def build_sidebar(guides_dir: Path, lang: str, current_path: str) -> str:
    """Build sidebar navigation with specific structure"""
    import re

    import frontmatter

    # Define sidebar structure
    structure = {
        "introduction": {
            "en": "Introduction",
            "tr": "Giriş",
            "items": ["v1/guide/welcome.md", "v1/guide/getting-started.md"],
        },
        "general": {
            "en": "General Information",
            "tr": "Genel Bilgiler",
            "items": ["v1/guide/api-structure.md", "v1/guide/administrative-structure.md", "v1/guide/key-concepts.md"],
        },
        "usage": {
            "en": "API Usage",
            "tr": "API Kullanımı",
            "items": [
                "v1/guide/provinces.md",
                "v1/guide/districts.md",
                "v1/guide/neighborhoods.md",
                "v1/guide/villages.md",
                "v1/guide/towns.md",
                "v1/guide/examples.md",
            ],
        },
        "support": {
            "en": "FAQ & Support",
            "tr": "SSS & Destek",
            "items": ["v1/guide/faq.md", "v1/guide/contact.md", "v1/guide/donate.md"],
        },
    }

    sidebar_html = ""

    for section_key, section_data in structure.items():
        # Add section header
        section_title = section_data.get(lang, section_data["en"])
        sidebar_html += (
            f'<div class="nav-section"><div class="nav-section-title">{section_title}</div><ul class="nav-list">'
        )

        for item_path in section_data["items"]:
            full_path = guides_dir / item_path

            # Skip if file doesn't exist
            if not full_path.exists():
                continue

            # Normalize paths for comparison
            item_path_normalized = item_path.replace("\\", "/")
            current_path_normalized = current_path.replace("\\", "/")

            # Read file to get title
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)

                # Try to get title from frontmatter
                title = post.get("title")

                # If no frontmatter title, try to find first H1
                if not title:
                    content = post.content
                    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                    if h1_match:
                        title = h1_match.group(1).strip()

                # Fallback to filename
                if not title:
                    title = full_path.stem.replace("-", " ").replace("_", " ").title()

            except Exception:
                title = full_path.stem.replace("-", " ").replace("_", " ").title()

            # Check if this is the current page
            is_active = current_path_normalized.endswith(item_path_normalized)

            sidebar_html += f'<li class="nav-item"><a href="/guides/{lang}/{item_path_normalized}" class="nav-link{
                " active" if is_active else ""}">{title}</a></li>'

        sidebar_html += "</ul></div>"

    return sidebar_html


async def list_guides(lang: str):
    """List all available guides for a language"""
    from pathlib import Path

    guides_dir = Path("guides") / lang
    if not guides_dir.exists():
        return JSONResponse(content={"guides": []})

    guides = []
    for md_file in guides_dir.rglob("*.md"):
        relative_path = md_file.relative_to(guides_dir)
        guides.append({"path": str(relative_path), "url": f"/guides/{lang}/{relative_path}".replace("\\", "/")})

    return JSONResponse(content={"guides": guides})
