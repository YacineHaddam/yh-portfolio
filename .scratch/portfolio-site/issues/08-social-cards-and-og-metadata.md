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

Verified: `make check` passes (source check on real and fixture content, strict build, 54 tests), including the new `tests/test_social_cards.py`.

Not verified: the live-site preview-debugger criterion, which needs the deployed site (ticket 02). Status stays `ready-for-agent` until then.

Review follow-ups, not done:

- The hidden-post test only checks that no card filename contains "hidden". Compare the set of cards against the published pages instead.
- `og:title` and `og:description` are only checked for non-emptiness.
- The fixture imports in `test_social_cards.py` would sit better in a `conftest.py`.
- The `_meta` regex depends on attribute order.
