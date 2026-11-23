---
round: 27
date: 2026-11-23
title: Rings no more
commits: [dfec669157f0ce158e3d8d0f625eca640511b6b9, da47bca83c73285ceb50557726e2cdd61aa1b494, c1a20c24b42a1614afe087d94d6f0a6c04b33193, fafc8bfebdae2b73c009f7df19b503cce5cbcfb8, 29b62cb9e96ee99a8f4265744fc3fb1e8cf5ec56, f2d7510a015d36fd9c8bc6a4858b4898ecdd4303, dc5e4467b04f691b03143433e1844de36b33abee, 9fe54c4c047e3f8b9133a6dde97ebed48da14230, 886aa2cf0eab6b5a5e490777b7055fd1fc8ee6cd, 7466ff4b978b9be53fa8a11e6b6b479742b50c2a, 9a9e52465fed184a0fa5ace5092f99ed39235e95, e5d49b9d581130f04286be1d519c9b336a6ed518, 00eb8aa31e8b74429367ef963206707434703739, f693f8f3fea79ba96f4acf183e1b11bdf58a5a43, 3c1747107f4d56658a24ab7f08f874607e3d05d1, f048f11901d983fe5280b29975d92af9d88713e7]
---
## Public

A new logo: three linked agents, no longer five-ring-adjacent. About starts
collapsed and News is one list, with two new items: a talk at ADT 2026 and
a journal acceptance. SimGov now says what it is about. On People, one alum
more, and a bio opens from a "Personal" link.

## Lab

| # | name | request | decision | reason | commits |
|---|------|---------|----------|--------|---------|
| 110 | Nimrod | logo looks a bit like the olympics | applied: three dots joined by links, theme colors | rule 1; design left to Claude by Nimrod | dfec669 |
| 116 | Nimrod | make About collapsed by default | applied | rule 1 | da47bca |
| 112 | Nimrod | merge News and Upcoming | applied: News is one list, no subsections | rule 1 | c1a20c2 |
| 111 | Nimrod | add that Nimrod is speaking at ADT | applied: ADT 2026, Paris, Nov 16, with Ehud Shapiro (past) | rule 1 | fafc8bf |
| 118 | Nimrod | add that Query-Based Committee Selection was accepted | applied: SN Computer Science (Springer Nature), arXiv link | rule 1; venue as Nimrod gave it | 29b62cb |
| 121 | Berihu Michiale Haileselassie | SimGov description | applied to the SimGov box | rule 1; project owner | f2d7510 |
| 113 | Nimrod | remove Nir perhaps | applied: moved to Alumni (MSc) | rule 1; Nimrod chose Alumni over deleting | dc5e446 |
| 114 | Nimrod | Berihu: name without a link, and a "Personal" link | applied: names are plain; a bio opens from a "Personal" link ("Bio" if the person also has a personal site) | rule 1 | 9fe54c4, f693f8f |
| 115 | Nimrod | have the next lab meeting open initially | applied: new `open:` frontmatter; Lab meetings and Next meeting start open | rule 1 | 886aa2c |
| 120 | Nimrod | Berihu is presenting tomorrow | applied: Nov 23 agenda item 1; Nov 16 moved to Past | rule 1 | 7466ff4 |
| 122 | Joel | agenda for Nov 23: AAMAS reviews; LD+S synthetic data | applied: Nov 23 agenda item 2 | rule 1 | 9a9e524 |
| 119 | Nimrod | Inbar to present next week | applied: Upcoming, Nov 30, Inbar Gerera (Nimrod confirmed which Inbar) | rule 1 | e5d49b9 |
| 117 | Nimrod | remind all to update for the next meeting | applied: a standing reminder line under Next meeting | rule 1; rule 4 (Lab page) | 00eb8aa |
| admin | Nimrod | CLAUDE.md: `open:` frontmatter (§3); bios open from a "Personal" link (§8) | applied | admin change: brings CLAUDE.md in line with #114 and #115; Nimrod OK'd the protected file in session | 3c17471 |
| admin | Nimrod | Govern showed "Deployed commit local" on talmonlab | applied: the app reads the commit from its git clone when RENDER_GIT_COMMIT is unset | admin change: Nimrod in session | f048f11 |

Wrong-pass submissions: none.

Notes: CLAUDE.md §3 and §8 updated for #114 and #115, with Nimrod's OK
(admin row). The journal name for #118 was not confirmed online.
