
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



axes.md


# rpgdag — Starter Axis List
 
A reference list of axes for use in campaigns. Each axis is bipolar — the two poles represent opposing forces, and the score tracks which way the world (or a character) is leaning.
 
---
 
## Moral / Ethical
 
| Axis | Pole A | Pole B |
|---|---|---|
| Good / Evil | Good | Evil |
| Order / Chaos | Order | Chaos |
| Justice / Vengeance | Justice | Vengeance |
| Truth / Deception | Truth | Deception |
| Compassion / Cruelty | Compassion | Cruelty |
 
---
 
## Political / Ideological
 
| Axis | Pole A | Pole B |
|---|---|---|
| Democracy / Tyranny | Democracy | Tyranny |
| Democrats / Republicans | Democrats | Republicans |
| Capitalism / Communism | Capitalism | Communism |
| Rich / Poor | Rich | Poor |
| Empire / Revolution | Empire | Revolution |
| Isolationism / Expansionism | Isolationism | Expansionism |
 
---
 
## Cultural / Social
 
| Axis | Pole A | Pole B |
|---|---|---|
| Old / New | Old | New |
| East / West | East | West |
| Tradition / Progress | Tradition | Progress |
| Urban / Rural | Urban | Rural |
| Individual / Collective | Individual | Collective |
 
---
 
## Elemental / Mythic
 
| Axis | Pole A | Pole B |
|---|---|---|
| Magic / Technology | Magic | Technology |
| Fire / Water | Fire | Water |
| Life / Death | Life | Death |
| Light / Shadow | Light | Shadow |
| Nature / Civilization | Nature | Civilization |
| Divine / Infernal | Divine | Infernal |
 
---
 
## Faction / Conflict
 
| Axis | Pole A | Pole B |
|---|---|---|
| Ninjas / Pirates | Ninjas | Pirates |
| Orcs / Elves | Orcs | Elves |
| Army / Navy | Army | Navy |
| Government / Revolutionaries | Government | Revolutionaries |
| Humans / Monsters | Humans | Monsters |
 
---
 
## Character / Personal
 
| Axis | Pole A | Pole B |
|---|---|---|
| Success / Failure | Success | Failure |
| Fame / Infamy | Fame | Infamy |
| Wealth / Poverty | Wealth | Poverty |
| Loyalty / Betrayal | Loyalty | Betrayal |
| Hope / Despair | Hope | Despair |
| Sanity / Madness | Sanity | Madness |
 
---
 
## Notes
 
- Any axis can be used at the global (world/party) level or the per-character level.
- Per-character axes with `axes_visible: false` enable hidden-objective and traitor mechanics.
- Victory conditions are typically defined as an axis threshold, e.g. `magic > 8` or `loyalty < -3`.
- Axes can be combined — a character might need both `wealth > 5` AND `fame > 3` to win.
 
