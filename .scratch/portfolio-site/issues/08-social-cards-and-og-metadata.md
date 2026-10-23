---
title: Social cards and Open Graph metadata
status: ready-for-agent
blocked-by: [02, 03]
---

# 08: Social cards and Open Graph metadata

**What to build:** When a post is shared on LinkedIn or X, it shows a generated preview image, title and description.

See the spec: Site features (Social cards).

**Blocked by:** 02 (Deploy to GitHub Pages via CI; provides `site_url`), 03 (Blog with published and hidden posts)

**Status:** ready-for-agent

- [x] Zensical's native social plugin is enabled.
- [x] Built-site check: each published fixture post has a generated card image, plus `og:title`, `og:description`, `og:image` and `twitter:card` meta tags. The `og:image` URL is absolute and based on `site_url`.
- [x] Built-site check: no card image is generated for a hidden fixture post.
- [ ] Verified on the live site with a social preview debugger (e.g. LinkedIn Post Inspector) for one post.

## Comments

### 2026-10-22

Implemented with a placeholder `site_url` (`https://your-github-handle.github.io/yh-portfolio/`) in `zensical.toml`, because ticket 02 isn't done. Replace it when 02 lands.

Verified: `make check` passes (source check on real and fixture content, strict build, 54 tests), including `tests/test_social_cards.py`. After review, the tests were tightened and `make check` passed again: every generated card must be referenced by a built page's `og:image` (so a hidden post's card would fail), `og:title` must contain the post title, `twitter:card` must be `summary_large_image`, and meta tags are parsed regardless of attribute order.

Not verified: the live-site preview-debugger criterion, which needs the deployed site (ticket 02). Status stays `ready-for-agent` until then.

Left open from review: the fixture imports in `test_social_cards.py` would sit better in a shared `conftest.py`.
