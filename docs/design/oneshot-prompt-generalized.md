# One-Shot Prompt (Generalized)

A single instruction for a fresh agent. It keeps the product intent and the hard-won interaction rules, and it does not leak a researched tool list, taxonomy, or measured layout numbers. The agent rediscovers the landscape and chooses visual details.

---

You are building a public GitHub Pages app that helps an engineer assemble an Infrastructure-as-Code and software-delivery stack the way an RPG player builds a character.

## Who this is for

Someone starting an IaC-first project. They already know a couple of tools and have strong tastes about a few others. They just discovered that the ecosystem is larger than those names, and they want a full enough map to choose from without pretending any catalog is complete.

The page should make a competent engineer look at a tool and think: I need this, for that job.

## What to ship

A dedicated public repo with an interactive static page on GitHub Pages.

This is not a blog, not a slide, and not a card dump. It is a talent tree:

- A central tree of tools, grouped into layers and jobs, with visible connections. It should read as a skill tree (nodes and links), not a stacked list with a decorative arrow.
- A way to inspect a tool in a persistent panel (click, not hover-only).
- A way to see the current build as a persistent character sheet of chosen tools (logos, names, remove, jump back to the node).
- On a wide desktop, keep those two panels available instead of hiding them behind toggles. On a narrow screen, overlay or collapse is fine.
- Sticky utilities for reset, paste-in of a saved build, and copy-out of the current build. Do not use a blocking prompt dialog for JSON.
- Named preset builds an engineer can apply, then edit. Each preset should state strengths and weaknesses.
- Export of the current build as JSON and as a graphic (SVG or equivalent).

Do not ask the user to pick among implementation options. Choose sensible defaults and ship.

## Discover the landscape (do not assume a list)

Research the IaC and delivery ecosystem from scratch. Identify the distinct jobs practitioners actually combine, and derive the layers, slots, and tool set from that research. Do not start from a remembered taxonomy.

For each tool you include:

- A short job-shaped description (what it is for), not brochure language.
- A logo that links to official docs or a starter guide.
- License and cost/hosting made obvious (open vs gated license; free/self-host vs vendor-free vs paid). Words plus a small mark beat a tiny color dot.
- Popularity from real public signals (for example repository stars). Show the real magnitude and a comparison within the set. Do not rescale to 100. If a product has no public repo, say so; do not treat missing data as zero, and do not drop important commercial tools only because they lack a star count.
- Sentiment from recent public discussion (forums, video, docs, reviews). Store it as counts and a ratio of outcomes to data points, not a fake 0–100 score.
- Color-coded positive and negative user concerns, paraphrased from sources.

Cite only sources you actually fetched. Flag estimates. Never invent versions, dates, or citations.

Decide which tools compete for the same job (pick one) and which compose (combine). Do not force exclusive picks on things that coexist in real stacks. Tag the constraints your research finds so a "pick one" is scoped honestly.

Where tools compose, show that in the tree and in the inspector (small marks, logos, highlight on hover or focus). Those marks must be recognizable: icon and background have to contrast. Clicking a related mark should take the user to that tool.

Acronyms and jargon should be understandable in place (hover, inline, or equivalent), not only in a separate glossary. Each layer and each inner job should say why it exists and why anyone should put a point there.

Include a curated set, not "every tool." Do not claim completeness. Do not overweight fading tools at the expense of the ones people actually reach for. If a category is famous in the field, it should not be missing without a sourced reason.

## Interaction

Inspect and select are different actions. Clicking a node opens the inspector. Adding or removing from the build is an explicit control (on the node and in the inspector). Keyboard users must be able to do both. After paste or a preset, the tree, the count, and the build sheet must agree.

If a panel can sit empty, give it an empty state rather than a blank hole.

## Visual quality

Take cues from polished product sites (type, color, shape), then make it readable:

- Comfortable type size. Secondary copy still has to be readable.
- Enough width that names and explanations are not cramped. Prefer wrapping at word boundaries over clipping names.
- Alignment that looks intentional (headers line up with lists; controls are not jammed against tags).
- One clear primary action.
- No overflow outside panels.
- No horizontal page scroll as a normal desktop state.
- The tree should not slide under a persistent panel.

You choose the exact palette, type, spacing, and breakpoints. Recheck the real page in a browser; CSS comments are not proof.

## Honesty and review

Stars and similar metrics measure attention, not quality. Community sentiment is biased toward loud sources; do not overclaim.

After the first working version, critique the taxonomy and the UI (including with extra agents or passes if you have them): false rivalries, missing jobs, unclear slots, unreadable chrome, broken selection. Fix what that review finds before you call it done.

## Done when, in a real browser

- A new visitor can read the tree, inspect a tool, add it to a build, apply a preset, paste JSON, copy JSON, and export.
- Desktop shows inspect and build without hunting for them.
- Combine/related marks are visible, not empty squares.
- License and cost are obvious at a glance.
- Names in the build sheet are readable.
- No console errors on the happy path.
- The GitHub Pages URL loads over HTTP.

## Do not

- Stop at a research memo or a static poster.
- Invent sources or numbers.
- Hide the only explanation of a term in a distant glossary.
- Make inspect and select fight for the same click.
- Scale sparse data to look like a percentage out of 100.
- Oversell the set as the entire ecosystem.
