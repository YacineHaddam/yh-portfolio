---
title: About page as CV, plus contact links
status: done
blocked-by: [01]
---

# 07: About page as CV, plus contact links

**What to build:** A recruiter can read the author's CV on the About page and optionally download a PDF. They can reach the author from GitHub, LinkedIn and email links that appear site-wide. The default homepage gets a short intro (who, what) pointing to Projects, Blog and About.

See the spec: Content model (About); Homepage.

**Blocked by:** 01 (Site skeleton that builds, with a check command)

- [x] The About page is structured as a CV: summary, experience, skills and education, with placeholder content for the author to fill in.
- [ ] An optional CV PDF link points to a site asset. The page works if the PDF is absent.
- [x] GitHub, LinkedIn and email links appear site-wide (header or footer social links).
- [x] The default homepage has a short intro and links to the three other sections. No custom homepage template is used.
- [x] No phone number or home address appears anywhere. Once ticket 05 is done, its personal-data scan covers this page.
- [x] Built-site check: the About page exists and the social links render.

## Comments

### 2026-10-22

Verified: `make check` steps each run on their own: source check (real and fixture) exit 0, strict build exit 0, pytest 49 passed. The new test `test_contact_links_render_on_every_page` was seen failing (links absent) before the fixture config got the social links, then passing. The real built site's home and About pages contain the GitHub link. The source check from ticket 05 passes over the new About page and reports no phone or address.

Not verified or not met:

- The CV PDF link is left unticked. Linking to a missing file would fail the strict build, so the link is a commented-out line in `content/about.md` with instructions to add `content/assets/cv.pdf` and uncomment it. The page builds without a PDF, but no live link points to an asset yet.
- The real `zensical.toml` uses placeholder handles (`your-github-handle`, `your-linkedin-handle`, `you@example.com`) marked with a TODO. The author must replace them before deploying, because `make check` does not catch them. Tests run against fixtures only, per the testing rules, so nothing asserts on the real config.
- The home page intro and the About page text are placeholders for the author to fill in.
