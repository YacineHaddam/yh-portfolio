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

- [ ] Zensical's native social plugin is enabled.
- [ ] Built-site check: each published fixture post has a generated card image, plus `og:title`, `og:description`, `og:image` and `twitter:card` meta tags. The `og:image` URL is absolute and based on `site_url`.
- [ ] Built-site check: no card image is generated for a hidden fixture post.
- [ ] Verified on the live site with a social preview debugger (e.g. LinkedIn Post Inspector) for one post.
