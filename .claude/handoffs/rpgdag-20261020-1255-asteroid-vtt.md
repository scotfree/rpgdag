# Handoff: rpgdag-20261020-1255-asteroid-vtt

- Repo / branch / HEAD: rpgdag / main / the `wrapup: handoff rpgdag-20261020-1255-asteroid-vtt` commit (pushed)
- Session: 2026-10-10 → 10-20, Asteroid Boys campaign config + hosted-system/VTT exploration

## Where things stand
- **Asteroid Boys** committed: `campaigns/asteroid_boys/game_config.json`, produced by
  `campaigns/asteroid_boys/generate.py` (edit its `LAYERS` table, re-run; it prints a balance report).
  Renders cleanly with `python3 cli.py render --config campaigns/asteroid_boys/game_config.json`.
  - Departure → 5×5 asteroid field (each asteroid → same/adjacent column next layer, no wrap; 259 paths)
    → Fly Base Ship Out (win iff Base Ship ≥ 4) / Stuck in the Belt (loss).
  - Axes: Credits start 3, Base Ship start 0, Force Balance start 5.
  - Each asteroid has 3 session questions (mined? fought? science?); its 2 effects hang on two of the "yes" answers.
  - Goal cards: Jedi Master (FB ≥ 8, 3VP), Force Anomaly (FB == 0, 3VP), Wealthy (Credits > 6, 2VP),
    Big Spender (credits down ≥ 6, 2VP), Miner (≥2 mining, 2VP), Hot Blooded (≥3 fights, 2VP), Brainy (≥2 science, 2VP).
- **Hosted-system / VTT exploration** — discussion only, no code. Findings:
  - Roll20: no external API; Mod scripts are sandboxed (no network) and need Pro. Best possible = one persistent
    game + Mod script + GM pastes a chat command `cli.py` prints.
  - Foundry: ~$50 one-time license (verify), free if self-hosted on the Mac; the Lancer system is maintained
    (v3.1.1, Foundry 13, COMP/CON pilot import). Preferred Foundry route ("option C"): `cli.py` writes
    `current_node.json` into Foundry's data dir; a tiny module/macro builds the scene on one click.
  - Free VTTs: **Owlbear Rodeo** is the best fit for implementing our *own* simple rules system — extensions are
    plain web apps with an SDK (scene items, synced metadata, broadcast, GM/player roles), multiplayer sync for free.
    MapTool is built for rules frameworks but dated/clunky. No confirmed Lancer support on any free VTT.
  - Cross-VTT design issue: rpgdag's Scene GM rotates every node; VTT GM rights are per-user.

## Next step
Answer the open questions below, then verify three Owlbear SDK unknowns against docs.owlbear.rodeo before
picking a POC: (a) can the SDK create/switch scenes or only edit the open one; (b) shared metadata size limits;
(c) can an extension fetch `http://localhost` (rpgdag server) from the https site, in Chrome and Safari.

## Open questions for Scot
1. **Simple host system** — the Axis ruleset (not yet written; `design/axes.md` is only an axis list), or something else (Lancer-lite)?
2. **Lancer's role** — drop it if we build our own, or keep as an optional heavy hosted system?
3. **Automation level** — VTT runs rules (→ Foundry) vs. shared map + COMP/CON (→ Owlbear)?
4. **GM rotation** — everyone gets GM rights / host toggles per scene / shared GM login? (Claude leans: everyone.)
5. **Hosting / remote play** — self-host on the Mac OK? Players remote, in person, or mixed?
6. **Big Spender** — keep ≥ 6 (only reachable on one exact route) or lower to ≥ 4?

## Decisions this session
- Asteroid Boys: Credits start 3 "just to make a point"; FB effects symmetric −3..+3; no wraparound;
  Departure links to all 5 of layer 1; party win via Base Ship threshold on the Fly Out terminal.
- Session type is decided by what players do, not by location → recorded via yes/no session questions,
  which also carry the effects (keeps the 3-question limit; no schema change).
- Base Ship effects deliberately skew positive (+15/−8) so ≥ 4 is reachable — Claude's call, flagged, not objected to.
- Not locked into Roll20; open to Foundry or a free VTT. Exploration first, POC discussion after.
- 4 issue candidates deliberately **not filed** (Scot: don't worry about them now) — listed in Claude memory
  (`rpgdag-project-state`): VTT POC, Big Spender threshold, `total_change` clamping semantics, `design/axes.md` cleanup.

## Issues filed / relevant
- None filed. Relevant existing: #1 validation, #6 scoring (`total_change` semantics), #7 pytest.

## Gotchas
- The session scratchpad was wiped during a ~9-day idle gap; the generator had to be rebuilt (verified
  byte-identical output). Keep-worthy scripts now go straight into the repo.
- `design/axes.md` contains pasted claude.ai UI text at the top.
- No project CLAUDE.md exists in this repo; conventions live in Claude memory.

## Verify state on pickup
```
git log -3 --oneline
python3 campaigns/asteroid_boys/generate.py /tmp/ab.json && cmp /tmp/ab.json campaigns/asteroid_boys/game_config.json
python3 cli.py render --config campaigns/asteroid_boys/game_config.json
```
