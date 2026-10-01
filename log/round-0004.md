---
round: 4
date: 2026-10-01
title: Govern as a popup, key terms, work in progress
commits: [992787b08c70a2a5ac97d596f7fe4a4b11cf4230, 1fcced354f93417568daea3e70f3f506a002ce88, eb884708b1afb9254a29d96319f4cd1493a56ac6, 5f31b4e379dc4f4787a63ff3b2244c0e83732214]
---
## Public

Research is now a tab of its own, also in the phone menu. The Govern button
opens a small window on any page instead of leaving it, and a request
records which page (and which section) it was sent from. A double click no
longer files a request twice. The Research page gained a Key terms section
for newcomers: plain explanations of the words used here, each with a first
paper or system to read. Lab members also got a place to keep each
project's status.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| 7 | Nimrod | add "Research" inside the hamburger | merged into #8 | duplicate submission, 3 seconds apart | — |
| 8 | Nimrod | same as #7 | applied (rule 2) | Research added as a tab everywhere, not only in the phone menu; the one-line tab list in CLAUDE.md updated with Nimrod's OK | 992787b |
| 9 | Nimrod | Govern must be easy: popup, and keep the page's context | merged into #10 | duplicate submission, 1 second apart | — |
| 10 | Nimrod | same as #9 | applied (rule 2) | popup on every page; issue records the page and last-opened section; same text from the same name within 5 minutes is filed once (cause of #4/5, #7/8, #9/10). Touches `app/govern.py`, a protected path, with Nimrod's OK | 1fcced3 |
| 11 | Briman | explain the terms used; cite and link foundational papers and systems (e.g., LiquidFeedback) | applied (rule 2) | Key terms section on Research (public, for future students), every link checked; Lab reading list linked | eb88470 |
| 12 | Briman | "work in progress" section: what we do and where it stands, incl. submitted/accepted papers | applied (rule 2), lab only | unpublished work stays off the public site; a table with one line per project, filled in by each project's members via Govern | 5f31b4e |

Wrong-pass submissions: none.

Notes: the project bullets on Research (e.g., token-based peer review)
still have no descriptions; their members can request them. Every Work in
progress line is empty until someone fills it in. Worth asking at the lab
meeting.
