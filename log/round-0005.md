---
round: 5
date: 2026-10-02
title: A sharper Research page
commits: [17cdf77c9fb83d756a00b1bcf8f305951ba70560, 39055ae1de7ab67a7d32760987350e3faaf47ca0, 82c25b716abc9eade61619148fd8883979304294, 9e1667e6b0355356fc459bb56153b5919ea0b6b9, 44851736af6e7dfb49a39d15540284574a409965, 861c563814845298a432920a78fe9ba95ac8e3d8]
---
## Public

The Research intro was rewritten, as an admin change: it now names
cooperative AI among the fields, states the method in one sentence (build,
analyze, and simulate models, towards collective decision-making mechanisms
that are efficient and fair), and no longer singles out blockchain. "Humans
with AI" is now "Humans and their AI agents", and a new theme, "Humans with
code", covers governance executed by protocols, as in DAOs.

Also as an admin change, the People page is now grouped by role (PI,
postdocs, PhD students, MSc students, other), alumni too; within a group,
people are listed by seniority, earliest first. Alumni are now in that
order, one MSc student moved to alumni, RAs have their own group, and
four MSc students were added.

Later the same day, also as an admin change, Research became three boxes,
one per theme: humans with humans, humans with AI (the two AI themes
merged), and humans with code. Each current project opens in a popup with
its owners and, once written, a description; finished work leaves the list,
since published work is on DBLP and Scholar, now linked from the intro. The
whole Research page is public, including the projects and their owners.
The footer is gone; the deployed commit is now shown on the Govern page.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| — | Nimrod | admin change: Research intro rewrite; rename "Humans with AI" to "Humans and their AI agents"; add "Humans with code" (two projects, also in Work in progress) | done | sharper framing of the lab; Nimrod's call, worked out in chat | 17cdf77 |
| — | Nimrod | admin change: People grouped by role, seniority within groups (file order = seniority); Nir Soffer listed as MSc student | done | clearer People page; Nimrod's call, worked out in chat | 39055ae |
| — | Nimrod | admin change: People seniority order (alumni reordered); Avital Finanser moved to alumni (MSc); "Other" group renamed RAs | done | order and status given by Nimrod in chat | 82c25b7 |
| — | Nimrod | admin change: add MSc students Inbar Arbel, Inbar Gerera, Gefen Ben Shoshan | done | current lab members, given by Nimrod in chat | 9e1667e |
| — | Nimrod | admin change: add MSc student Joel Van Der Boo (after Nir Soffer) | done | current lab member, given by Nimrod in chat | 4485173 |
| — | Nimrod | admin change: Research as three theme boxes with project popups (content/projects.yaml); Work in progress table folded into the popups (status, next); Publications section dropped, DBLP/Scholar in the intro; Research fully public; footer removed, commit shown on Govern; CLAUDE.md invariants 1 and 6, map and recipes updated | done | less clutter, current work up front; Nimrod's call in chat, with his explicit OK for the CLAUDE.md edits | 861c563 |

Wrong-pass submissions: none counted (no round run).

Notes: owners still to be set for Grassroots federation formation, Token-based
peer review, and LLM voting. Contact details (content/footer.md) are kept but
not shown; where they go is open.
