# LIVE MODIFICATION TASKS — CHHENG SOKUNTHEARY (p20240044)

> These were sealed until the invigilator released them. You have **one combined
> time-box** to complete all three. Each one **edits an artefact you already built**
> and uses the value printed below. Record every one in `live_mods.md` with the
> exact command(s) you ran, the live value you acted on, and a `live_<letter>.png`
> screenshot in that part's `images/` folder. An answer that ignores your value
> below, or that could have been written before now, scores zero.

| Part | Live curveball | Your value |
|:---:|----------------|-----------|
| **A** | Edit `thread_demo.c` to spawn this many **extra** workers that start **only after** the originals have joined; show the new LWP(s) appear in the mapping then disappear. | **1 extra worker(s)** |
| **D** | Add a **per-buyer purchase cap** to your purchase script (`buy_…`) — reject any single order above it; re-run `swarm` and show the locked result respects the cap and stays consistent. | **cap = 8** |
| **E** | Make `timed_job` **idempotent** using this marker token — it must refuse to run if the token for today is already in its log; trigger it twice and prove the 2nd was skipped. | **token = `ONCEKEY`** |

_Issued for: final-2026. If any value looks blank or wrong, raise your hand._
