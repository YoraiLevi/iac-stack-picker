# One-Shot Prompt (Precise)

A single instruction that encodes this project's end state, including hard-won interaction rules and a concrete coverage bar. Use this when the agent should reproduce the known product closely.

---

You are building IaC Stack Picker: a public GitHub Pages app that lets an engineer assemble an Infrastructure-as-Code / delivery stack the way an RPG player builds a character.

## Who this is for

The user is setting up an IaC-first project. They already want Terraform and Ansible. They know Chef and Puppet and do not want them as the default. Terragrunt made them realize they lack the rest of the map (wrappers, TACOS, policy, GitOps, secrets, images, CI). The site must make a competent engineer say of each tool: "ah, I need this, for that."

## What to ship

One self-contained interactive page (prefer a single `index.html` with a JSON data island) on a dedicated public GitHub repo, published to GitHub Pages at the project URL (not behind a broken custom domain).

The page is not a blog, not a static poster, and not a card catalog. It is a talent tree:

- Center: a branching tree of tools grouped into tiers and slots, with visible connectors between tiers. This must look like an RPG skill tree (nodes + lines), not a vertical list with a decorative arrow.
- Left rail: always visible on desktop (≥1100px). Click a tool node to inspect it here. Empty state: "Tool details" placeholder. Close returns to the placeholder; the rail stays.
- Right rail: always visible on desktop. This is the current build (character sheet): logo + name chips. Empty state: "No tools yet." Click a chip to jump/scroll to that node. Click × to remove.
- On a wide desktop, keep those two panels available instead of hiding them behind toggles. Below 1100px, rails may overlay. Do not make the tree jump horizontally when a tool is opened on desktop.
- Sticky top bar: tool count, Paste JSON, Copy JSON, Reset, View build. Do not use `prompt()` or a bottom tray for these.

Also ship: recommended preset builds (named stacks with strengths and weaknesses), SVG and/or JSON export of the current build, and import via Paste JSON.

## Tiers and slots

Use five tiers, each with a short plain-language "what this tier is responsible for" so a slot is never a mystery:

1. Provision — create cloud/cluster resources
2. Orchestrate — workflow, TACOS, policy-as-code
3. Configure — desired state on machines / images / secrets
4. Deliver — CI/CD and GitOps
5. Reconcile — drift, scan, cost, test

Inside each tier, slots are jobs (inner categories). Every slot must answer: what this job is, why you should pick anything here, and whether the slot is **pick one** (true rivals) or **combine** (complements).

Do not force pick-one on tools that coexist in real stacks. Terraform vs OpenTofu can be pick-one. Terraform vs Helm vs Vault vs GitHub Actions are not. CloudFormation/Bicep/Config Connector are single-cloud; tag cloud-specificity. Many orgs run several provisioners; do not teach a false dichotomy.

Where tools combine, show it on the node (small combine mark). Hovering that mark highlights related nodes. In the left inspector, "Combines with" is clickable brand-colored logos that jump to that tool. Combine logos must use the tool's brand background; never white-on-white (the icon renderer emits light fill for dark brands).

## Tool coverage (do not ship a 2022-shaped map)

Start from Terraform and Ansible as first-class. Do not feature Chef/Puppet/Salt as the config story; if present, mark them fading.

The map must actually include, unless you have a sourced reason to drop one:

- Provision: Terraform, OpenTofu, Pulumi, CloudFormation, CDK, Bicep, Crossplane / Config Connector, cluster layer (Cluster API / eksctl / kOps or equivalent)
- Wrappers / DRY: Terragrunt (and peers such as Terramate if warranted)
- TACOS / collaboration: Terraform Cloud/HCP, Spacelift, env0, Atlantis, Digger, etc. SaaS with no public repo is still in the map; do not drop it because stars are n/a
- Policy: OPA/Gatekeeper, Kyverno, Sentinel, Checkov, Trivy, Conftest, and peers
- Configure: Ansible first; Packer / cloud-init; secrets (Vault, SOPS, ESM, etc.)
- K8s package: Helm, Kustomize (cdk8s/KCL only if you have a real slot for them)
- Deliver: GitHub Actions and at least one other CI; GitOps engines Argo CD and Flux (not just the word "GitOps" in a glossary)
- 2024–2026 platform/IDP or app-model tools only if you can source them honestly; do not pretend a round number of names is "the ecosystem"

A few dozen tools is a curated teaching map. Do not claim completeness. Do not omit Ansible while listing Chef.

## Research and honesty

Before you write scores, gather per tool:

- GitHub popularity as raw stars (and similar). Display as the real number and a bar vs the set, not a fake /100. SaaS without a repo is `n/a`, not zero. Stars measure attention, not adoption; do not treat them as quality.
- Sentiment from recent HN, Reddit, YouTube, docs, and reviews. Store as favorable/unfavorable counts and a ratio of outcomes/data-points (X/Y), never rescaled to 100.
- Catalog concrete user concerns. In the inspector, show positive concerns and negative concerns, color-coded (green / red), in the user's words as paraphrased from sources.
- Every version, date, acquisition, and numeric claim needs a real fetched source. If a date is estimated, flag it. Never fabricate citations.

Punchy one-liners: what the tool does in a job-shaped sentence, not "a comprehensive platform for…"

Each logo links to that tool's official docs or starter guide.

## Visual language and accessibility

Inspire color, type, and shape from a clean modern marketing site (rounded pills, warm off-white, one accent green, one accent purple for the primary action). Then meet this bar:

- Body and description text must be readable at arm's length. No tiny gray captions as the main explanation.
- License and cost are first-class, not a 6px dot: open source vs source-available vs proprietary; free/self-host vs free-vendor vs paid. Use a small lock/pill plus words.
- Popularity and sentiment are visible on the inspector (stars count + bar; sentiment count + bar). Do not claim they appear on every node if they do not.
- Glossary terms (IaC, HCL, TACOS, GitOps, CRD, KMS, BSL, …) are explained in place: hover or inline, where the word is used. A glossary section may exist; it is not a substitute.
- Right-rail chips: names wrap at word boundaries, never ellipsis-truncate, never mid-word breaks. Rail wide enough (~200–250px) that single words fit. Header gutter aligns with the chip column. Logo, name, and × are vertically centered in the chip.
- Left inspector: breathing room between the license pill and the sticky "Add to build" button (~12px). Text must not overflow the pane.
- One accent for the primary action ("Add to build"). Do not autoplay comparisons.

## Selection model (this was a real bug)

Clicking a node opens the left inspector. It does not toggle selection.

Selection is a separate control on the node (＋ / ✓) that `stopPropagation`s, plus the inspector's "Add to build" / "In your build · tap to remove". Keyboard must work. After paste-JSON or a preset, the tree, count, and right rail all match.

Paste JSON: a modal, not `prompt()`. Copy JSON: clipboard, with a brief "Copied" confirmation. Preset builds fill the tree and the right rail.

Recommended builds: named stacks (for example AWS-native, multi-cloud GitOps, air-gapped) with strengths and weaknesses. Picking one is a starting character build the user can then edit.

## Engineering constraints

- Dedicated public repo; GitHub Pages from `index.html`. Verify over HTTP, never `file://` as the only check.
- Do not pollute a parent monorepo; keep this project self-contained.
- Prefer boring: one page, in-page JSON island for tools, in-page objects for compares/builds/edges.
- Combine graph: "Combines with" is real symmetric edges, not "same slot."
- Desktop always-visible rails reserve real gutters so the tree never slides under a rail. The tree lives in a clipping/scrolling stage if needed.

## Definition of done (verify in a real browser at a wide desktop width and spot-check a ~1000px window)

- Both rails visible on desktop with empty states on load.
- Click a tool with a dark-brand combine partner: combine logo is a colored square with a visible icon, not an empty white box.
- Add via ＋ and via the inspector button; right rail updates; names fully readable.
- Paste a valid build and an invalid payload; copy JSON works.
- A preset applies a full example stack and the right rail shows all of them untruncated at desktop width.
- No horizontal page scroll; tree does not sit under the right rail.
- 0 console errors.
- Pages deploy is reachable at the github.io project URL.

## Do not

- Do not stop at a research memo or a PNG infographic.
- Do not use hover-only detail as the inspector.
- Do not put the current build only in a bottom bar.
- Do not scale scores to 100.
- Do not hide license in a tiny circle.
- Do not leave Chef/Puppet as the config default.
- Do not invent sources, versions, or dates.
- Do not ask the user to choose among implementation options. Pick the conservative default that matches this spec and ship.
