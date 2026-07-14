
/
RPG DAG
RPG DAG
platform for running tabletop RPG campaigns as a directed acyclic graph (DAG) of scenes. A campaign is a journey through nodes — each node is a scene played out at the table using whatever rules system the group prefers. The platform manages game state, tracks axes (bipolar stats representing world and character state), and generates HTML interfaces for players and the GM.




How can I help you today?



Recents
RPG campaign conflict axes
1 minute ago
Instructions
Add instructions to tailor Claude’s responses

Memory
Only you
Purpose & context Scot is developing a tabletop RPG system called rpgdag — a DAG (directed acyclic graph)-structured campaign framework where players traverse nodes (scenes), each resolved using a lightweight rule system called Axis (or an external system like D&D). The project has prior work stored in a repository with associated design documents. Key design values include minimizing meta-debate at the table and keeping play flowing smoothly. Current state Several major design questions have been resolved: Axes are monopolar (0–10, single adjective); opposition is expressed through explicit paired impacts rather than axis structure Character advancement doesn't occur within a single DAG campaign but can happen between campaigns as a consequence of hidden per-character axis goals End-of-node ritual: GM reads global axis impacts aloud; no per-player tracking needed during play Victory structure: Party victory is binary (campaign goal success/fail); individual victory is scored through personal victory points tied to hidden axis goals Fog of war revelation at end of each node is a core mechanic driving narrative awareness and player decisions about which node to visit next and who GMs it Three documents were generated: a starter axis list (organized by category: moral/ethical, political/ideological, cultural/social, elemental/mythic, faction/conflict, character/personal), a D&D-inspired axis list (mapping ability scores, skills, and class archetypes onto axes), and a GM regulation mechanics catalog (fifteen options, A–O, ranging from token-based vetoes to voting systems to scene pre-commitment). On the horizon Open questions remaining at the end of the last session: Scope of fog-of-war revelation at each node Method for generating the DAG map Degree of player agency in node movement How the DAG map updates after node resolution High-level board game loop formalization Key learnings & principles Monopolar axes are mechanically simpler and sufficient; opposition is better expressed structurally (paired impacts) than through axis polarity GM regulation mechanics should minimize table meta-debate — solutions that keep play flowing are preferred over those requiring negotiation or voting Fog of war revelation is load-bearing for both narrative engagement and strategic decision-making Approach & patterns Scot works through design iteratively in conversation, resolving questions layer by layer (campaign framework → scene resolution → specific implementations) Uses voice mode on mobile at times; artifact/document context is not reliably available in voice mode, so important content should be pasted directly into the chat thread rather than stored only as artifacts Repository and external design documents exist but aren't always accessible mid-session, which creates friction — worth establishing what's available at the start of a session Tools & resources Repository with prior rpgdag design documents (not always accessible mid-session) D&D as a reference system and potential integration target for the Axis rule system

Last updated May 4

Context
1% of project capacity used

scotfree/rpgdag
main

GITHUB



dnd_axes.md
129 lines

md



axes.md
88 lines

md



gm_regulation_mechanics.md
170 lines

md



gm_regulation_mechanics.md


# GM Regulation Mechanics
 
A menu of potential mechanics for encouraging fair and interesting GM behavior in the rotating GM model. The goal is not to prevent GMs from pursuing their hidden axis goals — that tension is the point — but to prevent outright abuse (rooms full of lava) while also discouraging subtle systematic bias (every scene mysteriously advances the Blood Moon).
 
---
 
## Background: What We're Solving For
 
In the rotating GM model, the player running a scene has:
- A hidden set of personal axis goals they may want to advance
- Control over scene design, NPC behavior, and narrative framing
- Incentive to steer outcomes toward their goals
Good GM behavior is **neither fully supportive nor fully adversarial**. The GM is a partial ally with their own agenda baked into the scene design. The party can still succeed — they just may succeed *more easily* if they play into the GM's preferred narrative direction.
 
The mechanics below address: when can the party object, how does that work, and what stops a GM from gaming the system.
 
---
 
## The Options
 
### Option A: Veto with Immediate Vote
- A player spends a token to call a veto
- Table votes immediately on whether it's legitimate
- If vote passes: veto takes effect, player gets token back
- If vote fails: veto doesn't take effect, player loses token
- **Pro:** legitimacy is tied directly to the moment of decision
- **Con:** creates meta-debate at the table during play
---
 
### Option B: Veto Always Works, Vote on Recharge
- Player spends a token, veto takes effect immediately — no discussion
- After the scene (or at a break), table votes on whether it was legitimate
- If yes: player gets token back; if no: token stays spent
- **Pro:** no interruption to play, veto is clean and fast
- **Con:** voting phase still exists, even if softer; delayed vote may be colored by downstream consequences
---
 
### Option C: Limited Tokens, No Recharge
- Players start with X tokens, use them freely, no recharge mechanism
- Simplest mechanically — no voting, no tracking
- **Pro:** simple, no overhead
- **Con:** exploitable — a GM can bait players into spending tokens early, then act freely
---
 
### Option D: Unlimited Vetoes with Escalating Cost
- First veto costs nothing (or very little), each subsequent veto by the same player costs more
- Cost could be an axis hit, a resource, a narrative penalty
- **Pro:** self-regulating without a token economy
- **Con:** requires tracking, and the cost has to actually matter to the player
---
 
### Option E: GM Moves Are Explicit and Voted
- Inspired by *Apocalypse World* — GM narrates a "move" as an explicit decision point
- Table votes thumbs up/down immediately, no tokens
- Variation: votes only triggered if someone calls for one
- **Pro:** transparent, stateless, no meta-tracking, every significant decision gets scrutiny
- **Con:** could slow play significantly; players could weaponize voting against moves they just dislike
---
 
### Option F: Interrupt Voting, No Tokens
- GM makes moves normally; any player can call for an immediate vote at any time
- Vote determines if the move stands or gets rewound
- No tokens — cost of spamming votes is purely social friction and slowing the table down
- **Pro:** simple, stateless, no economy to track or exploit
- **Con:** relies on table culture; a jerk player just makes everyone miserable
---
 
### Option G: GM Score / Reputation System
- Each GM accumulates a score based on table votes or axis shift patterns over the campaign
- Low score means reduced GM privileges (demoted, smaller scenes, skipped turns)
- **Pro:** incentivizes good behavior over time without in-the-moment friction
- **Con:** feels bureaucratic, hard to tune fairly, punishes players for honest mistakes
---
 
### Option H: Narrative Consequences for GM Overreach
- If a GM's move is vetoed or voted down, their *character* takes an axis hit next time they play
- Heavy-handed GMing affects your character's standing in the world
- **Pro:** ties GM behavior back into the fiction, makes fairness roleplayable
- **Con:** can feel punitive; hard to calibrate; may discourage creative risk-taking
---
 
### Option I: Rotating Veto Authority
- One designated player per session holds "final say" veto power — no token cost, just works
- That role rotates so everyone gets a turn as the check
- **Pro:** spreads power, creates an explicit referee role
- **Con:** adds a new role layer; that player becomes a target if too strict or too lenient
---
 
### Option J: Collaborative Scene Design
- GM proposes a scene outline before play; party gets to edit it
- Players can suggest complications, NPCs, stakes — a design negotiation, not a mid-game veto
- **Pro:** prevents surprises, builds buy-in, no mid-play friction
- **Con:** time-intensive, changes the nature of GM authority, reduces spontaneity
---
 
### Option K: Consequence Escalation
- First veto by a player in a session: costs nothing, just works
- Second veto: costs something (axis point, narrative resource, future GM turn)
- Third and beyond: steeper cost
- **Pro:** punishes spam without limiting legitimate vetoes
- **Con:** requires tracking; cost must feel meaningful to actually deter abuse
---
 
### Option L: GM Abstinence Rule
- GMs are simply prohibited from "gotcha" moves — all complications must be telegraphed or earned
- Rule: no surprises that offer zero counterplay
- **Pro:** simplest, most implicit, no overhead
- **Con:** hardest to enforce; relies entirely on table culture and good faith
---
 
### Option M: Balance Auditing at Scene End
- At the end of every scene, the GM reads out all axis impacts that occurred
- Table can immediately see if certain axes were systematically favored
- Not a veto — purely transparency
- **Pro:** immediate visibility, lets the table calibrate over time, creates a ritual moment
- **Con:** doesn't prevent unfair play, just exposes it after the fact
---
 
### Option N: Explicit Balanced Scene Design
- GM pre-commits to axis impacts before the scene runs
- "The Blood Moon axis goes up one or down one depending on what the party does"
- Lays out the decision tree in advance; party knows what's at stake
- **Pro:** forces fairness into scene prep, party has full information about stakes
- **Con:** requires more prep time; less flexibility mid-scene; can feel railroaded
---
 
### Option O: GM Reward for Balance
- GM earns a meta-reward (recharge token, bonus axis point, campaign currency) if the scene ends balanced
- Balance defined as: equal positive and negative impacts across axes, or zero-sum outcomes
- **Pro:** incentivizes fairness without punishment; aspirational rather than adversarial
- **Con:** could encourage trivially "safe" scenes that cancel out; needs tuning to prevent gaming the metric
---
 
## Key Design Dimensions
 
When choosing or combining mechanics, consider where you land on each of these axes:
 
| Dimension | Option A |
|---|---|
| **When does enforcement happen?** | Before the move / During / After |
| **Who decides legitimacy?** | One player / Majority vote / Unanimous / No one |
| **What's the cost of objecting?** | Tokens / Social friction / Nothing |
| **What's the cost of GM overreach?** | Narrative / Mechanical / Reputational / Nothing |
| **Is it stateless or tracked?** | Stateless (vote and move on) / Tracked (tokens, scores, history) |
| **Does it interrupt play?** | Yes / No |
 
---
 
## Deferred Ideas (Worth Revisiting)
 
- **Card-based implementation:** Axes with low cardinality (binary or 3-state) could be represented physically with cards on a tabletop. Token economy maps naturally to physical tokens.
- **Axis history tracking:** Statistically analyzing a GM's axis shifts across all their scenes to detect systematic bias. Interesting but gameable and potentially wonky.
- **Delayed legitimacy votes:** Voting on veto validity after play has moved on. Generally felt problematic because downstream consequences color the judgment.
 
