---
round: 2
date: 2026-10-01
title: fewer tabs, folded pages, sign in once
commits: [c5fd20f1916656d39de709885e1b72778fb3fa23, ed5ebc4c83c3ea648850305931ef05fbc6b7ed53, ee54938efcdd32f636c62969d065b970cf942c3a]
---
## Public

The site was simplified, as an admin change. Ten links became three tabs
and a home page: the lab name at the top opens Research (with projects and
publications); then People, Lab, and Govern (the request form, then pending
requests, rules, rounds, and how this works).
Every page now shows its sections collapsed, so it fits on one screen
until you open what you care about. Contact details moved to the footer.
Lab members now sign in once and stay signed in for a year. Old addresses
still work and redirect. Rule 2 was reworded to say where the log now is.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| — | Nimrod | admin change: merge into fewer tabs, collapsed sections, sign in once (name remembered), Lab page lab-only | done | site had too many pages and the members' view was confusing; Nimrod OK'd the edits to protected files (CLAUDE.md, app/gate.py, app/govern.py) | c5fd20f |
| — | Nimrod | amend rules: rule 2 says the log is under Rounds on the Govern page | done | the Log page was merged into Govern; asked by Nimrod in the session | ed5ebc4 |
| — | Nimrod | admin change: drop the Research tab | done | it duplicated the BGULAB brand link; Nimrod's call (CLAUDE.md map line updated with the log) | ee54938 |

Rule 2, old wording (round 0): "Requests are decided by Nimrod, with
Claude, in a round before each lab meeting. Every decision and its reason
are recorded on the Log."

Wrong-pass submissions: none.

Notes: the Lab page (onboarding, house style, reading list) is now lab-only;
the style guide and reading list used to be public.
