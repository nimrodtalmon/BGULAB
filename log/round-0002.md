---
round: 2
date: 2026-10-01
title: fewer tabs, folded pages, sign in once
commits: [c5fd20f1916656d39de709885e1b72778fb3fa23]
---
## Public

The site was simplified, as an admin change. Ten links became four tabs:
Research (with projects and publications), People, Lab, and Govern (the
request form, then pending requests, rules, rounds, and how this works).
Every page now shows its sections collapsed, so it fits on one screen
until you open what you care about. Contact details moved to the footer.
Lab members now sign in once and stay signed in for a year. Old addresses
still work and redirect.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| — | Nimrod | admin change: merge into four tabs, collapsed sections, sign in once (name remembered), Lab page lab-only | done | site had too many pages and the members' view was confusing; Nimrod OK'd the edits to protected files (CLAUDE.md, app/gate.py, app/govern.py) | c5fd20f |

Wrong-pass submissions: none.

Notes: the Lab page (onboarding, house style, reading list) is now lab-only;
the style guide and reading list used to be public. Rule 2 still says
"the Log"; the log now lives on the Govern page under Rounds. Rewording
the rule is left to a request.
