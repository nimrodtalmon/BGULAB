---
round: 6
date: 2026-10-06
title: Fluent Govern, livelier look
commits: [07bd6f02491decdb01db45645d53d1f375760b2c, 075e3f47a40320795e323892e7242bae73c42b53, ca97582174d54df5eeea04995041fe399431fae1, facba8f9d88603ee7a39db6284f90d75a66ba0f4, a5ab09309f16dfe433d17766a460aa7f263b4de5, 3cc529e093107f982ed27b14dbb547c8375b4b30, 8a3d8be61e1f596cc9ef2aa37710a63b27209acb]
---
## Public

Govern is now fluent: Enter sends a request (Shift+Enter for a new line),
the window closes at once, and a short note confirms. Signed-in members are
no longer limited in how many requests they send, and a request sent twice
at the same moment is filed once. The site looks a little livelier: one
color per research theme, new fonts, and initials until members add photos.
The People page takes a photo and links per member, sent by each member
with Govern. The BGULAB brand was dropped, since the Research tab does the
same. One alumnus's current affiliation was updated.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| 13 | Briman | update current people; photos and Scholar/DBLP/LinkedIn links | applied (rule 2), partly done earlier | Avital moved and current students added in round 5; Nir stays current (Nimrod listed him as a current MSc student); People now shows a photo and links per member, each member sends theirs with Govern (e.g. "photo: https://…") | 075e3f4 |
| 14 | Nimrod | K. Sornat moved to AGH Krakow | applied (rule 2) | alumni affiliation updated | 07bd6f0 |
| 15 | Nimrod | drop the BGULAB brand | applied (rule 2) | duplicated the Research tab; on phones the menu button moved to the left; one descriptive line of CLAUDE.md updated, with Nimrod's approval of the round | ca97582 |
| 16 | Nimrod | same as #15 | merged into #15 | filed in the same second (duplicate-filing bug, fixed below) | — |
| 17 | Nimrod | Enter sends; no Send click, no waiting | applied (rule 2) | Enter sends, Shift+Enter new line; popup closes at once and sends in the background; failures show a note with "Edit and resend" (text kept) | facba8f |
| 18 | Nimrod | no "it will be decided…" message; fluent governing | merged into #17 | same change: a short "Sent ✓" note only | — |
| 19 | Nimrod | a bit more lively style, not flashy | applied (rule 2) | theme colors on boxes and avatars, Inter + Source Serif fonts, soft header wash, gradient title mark | a5ab093 |
| — | Nimrod | admin change: file a request once even when sent twice at the same moment | done | cause of #4/5, #7/8, #9/10, #15/16; touches app/govern.py (protected) with Nimrod's OK | 3cc529e |
| — | Nimrod | admin change: no Govern rate limit for signed-in members (others: 5 per 10 minutes) | done | Nimrod hit the limit and one request was refused unsaved; app/govern.py (protected) with Nimrod's OK | 8a3d8be |

Wrong-pass submissions: none.

Notes: one of Nimrod's requests on 2026-10-06 was refused by the rate limit
and not saved; to be resent. Lab members can now send their photos and links.
