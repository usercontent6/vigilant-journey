"""
crawler/selectors.py

Central location for every CSS selector used by the crawler.

If MovieHDTV changes its HTML,
this should be the ONLY file that needs updating.
"""

# ============================================================
# Homepage
# ============================================================

ARTICLE = "article.post-item.site__col"

ARTICLE_LINK = "h3.entry-title a"

ARTICLE_IMAGE = "img.blog-picture"

ARTICLE_DATE = ".date-time span"

# ============================================================
# Movie Page
# ============================================================

TITLE = "h1"

CONTENT = "article"

DESCRIPTION = 'meta[name="description"]'

KEYWORDS = 'meta[name="news_keywords"]'

OG_IMAGE = 'meta[property="og:image"]'

UPLOAD_DATE = "time.entry-date"

# ============================================================
# Download Section
# ============================================================

DOWNLOAD_BUTTONS = "a.btn"

# ============================================================
# Images
# ============================================================

CONTENT_IMAGES = ".container img"

# ============================================================
# Generic
# ============================================================

META_DESCRIPTION = 'meta[name="description"]'

META_KEYWORDS = 'meta[name="news_keywords"]'

META_OG_IMAGE = 'meta[property="og:image"]'
