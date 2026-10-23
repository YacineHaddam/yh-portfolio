---
title: Social cards and Open Graph metadata
status: done
blocked-by: [02, 03]
---

# 08: Social cards and Open Graph metadata

**What to build:** When a post is shared on LinkedIn or X, it shows a generated preview image, title and description.

See the spec: Site features (Social cards).

**Blocked by:** 02 (Deploy to GitHub Pages via CI; provides `site_url`), 03 (Blog with published and hidden posts)

**Status:** done

- [x] Zensical's native social plugin is enabled.
- [x] Built-site check: each published fixture post has a generated card image, plus `og:title`, `og:description`, `og:image` and `twitter:card` meta tags. The `og:image` URL is absolute and based on `site_url`.
- [x] Built-site check: no card image is generated for a hidden fixture post.
- [x] Verified on the live site with a social preview debugger (e.g. LinkedIn Post Inspector) for one post.

## Comments

### 2026-10-22

Implemented with a placeholder `site_url` (`https://your-github-handle.github.io/yh-portfolio/`) in `zensical.toml`, because ticket 02 isn't done. Replace it when 02 lands.

Verified: `make check` passes (source check on real and fixture content, strict build, 54 tests), including `tests/test_social_cards.py`. After review, the tests were tightened and `make check` passed again: every generated card must be referenced by a built page's `og:image` (so a hidden post's card would fail), `og:title` must contain the post title, `twitter:card` must be `summary_large_image`, and meta tags are parsed regardless of attribute order.

Left open from review: the fixture imports in `test_social_cards.py` would sit better in a shared `conftest.py`.

### 2026-10-23

`site_url` is now the real address (`https://YacineHaddam.github.io/yh-portfolio/`, set by the ticket 02 wizard) and the site is deployed.

Verified on the live site: LinkedIn Post Inspector, run by the author on `https://yacinehaddam.github.io/yh-portfolio/blog/2026/10/21/hello-world/`, shows the generated card image, the title "Hello, world - Yacine Haddam" and the site name. Evidence is the author's screenshot. The X preview was not checked.
