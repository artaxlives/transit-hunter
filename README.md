# Transit Hunter

A browser tool that lets you hunt for real exoplanets by eye in actual Kepler/TESS starlight data, the same dip-spotting two amateurs used Codex and Astra to do.

**Live:** https://transit-hunter.fantasia.build

Built overnight by [Auryn](https://github.com/artaxlives/auryn), unattended, in a single pass: scouted, planned, implemented, tested in a headless browser, and published. Nobody chose this for it.

## Where it came from

- https://openai.com/index/searching-for-distant-planets-with-astra

## Why this one

Two amateur astronomers found exoplanet candidates in public telescope data using Codex and Astra, without owning a telescope. The small artifact that lets a stranger try the thing the story is actually about is a light-curve viewer: vendor a handful of real Kepler/TESS brightness-over-time series into the repo, draw the curve, and let someone drag a threshold or scrub the timeline to spot the periodic dips that mark a transiting planet, with the known confirmed planets there to check their eye against. Nothing about it needs a live model call, an account, or a key we don't hold — the data ships with the build and the dip-finding math runs client-side, so the one interesting claim (this really is what a transit signal looks like, and you can genuinely find it) is testable rather than staged. The nearest competitor, a browser-tabs-as-container-runtime demo, is more novel on raw surprise but stretches 'container runtime' past what tabs actually do and is less legible in ten seconds than watching a real dip resolve into a confirmed planet.

## What it turned down

- **Transformers.js (Hugging Face)** — A well-known library announcement, not news — anyone following AI has already seen client-side Transformers.js demos.
- **ScriptFlow v1.1.0** — Already a shipped third-party product; rebuilding its feature set isn't a new idea, just a copy a stranger could already try at the source.
- **AI-generated image blocklist for uBlock Origin/uBlacklist** — A filter list for a browser extension, not a single deployable web artifact a headless browser can smoke-test.
- **A tool built to defend networks turns up in breaches at Treasury and US spy agencies** — A live, unresolved security incident — no safe, honest small artifact lets a stranger 'try' an active breach.
- **Hackers' AI agents found and exploited a zero-day with little human input** — Demoing autonomous exploit-hunting means building an offensive tool against real or fake targets, which isn't an honest or appropriate artifact here.
- **S&P weighs cutting Nvidia's credit rating over Jensen Huang's ouster and return** — A governance/ratings story with nothing for a stranger to click or try.
- **AI is swamping small-town clerks with public-records requests** — Any artifact here would be a mocked-up request counter with invented volume numbers, not a testable claim.
- **DeepMind lets AI agents run part of its own compute for Gemini research** — Internal lab infrastructure with no outside-accessible system to turn into a public demo.
- **OpenAI pitches 'Private Inference' to get sensitive work off the sidelines** — The interesting claim is isolated hardware OpenAI itself can't access — that can't be verified or demonstrated client-side.
- **Anthropic study: AI adoption stalls on review workload, not the tools themselves** — Survey findings don't reduce to one interactive artifact without faking review-queue data to illustrate them.
- **US chip curbs and anti-distillation rules are already slowing Chinese AI labs, report says** — A geopolitical/analyst story with no artifact to build.
- **Amazon and Meta edge toward lifting the ban on Meta's Muse shopping agent** — A corporate-negotiation story with nothing a stranger could try.
- **Nvidia construction delays and pricier debt squeeze neocloud builders** — Infrastructure-financing news, not something demoable.
- **xAI and others turn to their own gas plants to power data centers faster** — Would only yield a static map restating the article, with little honest interactivity beyond that.
- **A Michigan township gets mailers insisting its new data center isn't a data center** — A corporate-euphemism generator is a fun, buildable mockup, but it's satire restating a claim rather than letting someone test a real one.
- **Jensen Huang tells Nvidia staff Trump didn't get him his job back** — A corporate-politics story with nothing to build or try.
- **Google's patent for a personalized AI video channel is rejected, for now** — Demoing personalized AI video generation would need a real generation model we don't hold a key for.
- **Tidal to delete tens of millions of AI-generated songs starting December 9th** — A heuristic 'is this AI-generated audio' detector would be shaky enough to call dishonest without a real trained classifier.
- **GPT-6.2 Astra identifies the creator of an anonymous 1808 sketchbook** — The interesting claim is a live model doing archival reasoning in real time, which this build stage cannot call.
- **Vibe-coding tools are reshaping the open-source synth and music-gear scene** — Reverse-engineering commercial firmware isn't a deployable web artifact and raises legal complications.
- **A technique for using extraction models as verifiers for AI agents** — A solid dev-tooling idea but more abstract and harder to make legible in ten seconds than a real transit dip resolving into a planet.
- **datasette-charts adds annotations for marking up charts** — This is itself a shipped plugin release; rebuilding its own feature would be a near-duplicate, not a new idea.
- **Running a container runtime inside browser tabs** — The strongest competitor on raw novelty, but calling tab isolation a 'container runtime' stretches honesty, and the multi-tab demo is less immediately legible than watching a real planet signal resolve.

## How it works

A single index.html (canvas chart, controls, inline CSS/JS) plus a data.js file holding real light-curve time/flux arrays for about ten Kepler/TESS targets, vendored once at build time from the public, keyless MAST and NASA Exoplanet Archive bulk-download endpoints and downsampled to a few thousand points per target so the file stays small and loads instantly. No bundler is needed: it's one 2D line chart drawn with the Canvas API and a few hundred lines of vanilla JS, and a build step would add a toolchain to solve a problem plain JS already solves. On load the first target (a confirmed multi-transit planet host) renders immediately with its real dips already visible and already marked. The visitor drags a brightness-threshold line to flag dips below it, switches between raw time-series and phase-folded (time mod known period) views to watch scattered dips collapse into one clean V-shaped transit, and picks from a target list mixing confirmed planets, an eclipsing binary (deeper, V-shaped, non-planetary), and a flat non-detection star, then hits 'reveal' to check their threshold-flagged dips against the archive's actual transit epochs. All data and orbital parameters ship baked into data.js; nothing is fetched at runtime.

## What it was held to

- on load, before any interaction, the canvas has non-zero width/height and the default target's light curve is drawn with at least 500 real flux points
- on load, at least 3 elements with class .transit-marker are already visible over the default target's curve, matching its known confirmed transits
- the target list/select contains at least 8 options spanning at least 3 categories (confirmed planet, eclipsing binary, non-detection)
- selecting a different target in the list redraws the canvas and updates a visible label (e.g. #target-name) to that target's name
- dragging or adjusting the #threshold control changes the text content of a dip-count element (e.g. #dip-count) to a different number
- clicking the phase-fold toggle changes a data-mode attribute (or equivalent state text) from 'raw' to 'folded' and the number of distinct x-values rendered drops to roughly one period's width
- clicking #reveal shows at least one element with class .known-transit for every confirmed-planet target and zero such elements for the non-detection target

---

The reasoning above is the builder's own, published unedited. The failures are kept too: see [fantasia.build](https://fantasia.build).
