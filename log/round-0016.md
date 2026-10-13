---
round: 16
date: 2026-10-13
title: Fewer boxes, shortcuts
commits: [8bdb3d467fbb1fef333c5fd5b8d6fb01c0f60b84, afab6526587fca6f4734852ee118b06e00508a8c, f9c4f0407057ca4f74470dd1a50cbdeb64f57654]
---
## Public

Boxes are back to a few: only sections a page asks for are boxed, one per
row; the rest are plain folds without indentation. The second paragraph of
the Research intro now folds under "More". Each section has a letter
shortcut (underlined in its title); "g" still opens Govern.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| 65 | Nimrod | News on Research should not be a box | applied, merged with 68, 69 | rule 1; News is a plain fold | 8bdb3d4 |
| 68 | Nimrod | opening a box should not widen it; one box per row | applied, merged with 65, 69 | rule 1 | 8bdb3d4 |
| 69 | Nimrod | box only Onboarding and Mantras; Ideas and Lab meetings plain | applied, merged with 65, 68 | rule 1; pages list boxed sections in their frontmatter; Govern and People plain | 8bdb3d4 |
| 66 | Nimrod | fold "We study…" and "Our current work…" on Research | applied in part | rule 1; "We study…" stays visible on the public page, the rest folds under More | afab652 |
| 67 | Nimrod | letter shortcuts for sections, on all pages | applied | rule 1; first free letter of each title, underlined; off while typing | f9c4f04 |

Wrong-pass submissions: none.

Notes: none.
