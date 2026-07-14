
/
RPG DAG
RPG DAG
platform for running tabletop RPG campaigns as a directed acyclic graph (DAG) of scenes. A campaign is a journey through nodes — each node is a scene played out at the table using whatever rules system the group prefers. The platform manages game state, tracks axes (bipolar stats representing world and character state), and generates HTML interfaces for players and the GM.




Type / for skills



Recents
RPG campaign conflict axes
just now
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



dnd_axes.md


# rpgdag — D&D-Inspired Axis List
 
Axes derived from Dungeons & Dragons mechanics — ability scores, skills, class archetypes, and alignment — reframed as bipolar axes suitable for narrative goals, scene outcomes, and lightweight character definition.
 
---
 
## Alignment (Classic D&D)
 
These map directly from D&D's alignment system and work as both world-level and character-level axes.
 
| Axis | Pole A | Pole B |
|---|---|---|
| Good / Evil | Good | Evil |
| Lawful / Chaotic | Lawful | Chaotic |
 
*Note: These two axes together recreate the full D&D alignment grid. A character at high Lawful + high Good is a Paladin archetype; high Chaotic + high Evil is the classic villain.*
 
---
 
## Combat Style
 
Derived from the tension between different martial archetypes — Fighter, Barbarian, Rogue, Ranger, Monk.
 
| Axis | Pole A | Pole B | D&D Roots |
|---|---|---|---|
| Brawn / Finesse | Brawn | Finesse | STR vs DEX; Fighter vs Rogue |
| Rage / Discipline | Rage | Discipline | Barbarian vs Monk |
| Melee / Ranged | Melee | Ranged | Fighter vs Ranger |
| Offense / Defense | Offense | Defense | Damage vs AC/HP focus |
| Solo / Tactical | Solo | Tactical | Single combat vs battlefield coordination |
 
*Characters at high Brawn/Rage/Melee are classic berserkers. High Finesse/Discipline/Ranged are assassins or monks. High Tactical/Defense suggests a battlefield commander or paladin tank.*
 
---
 
## Magic & Knowledge
 
Derived from spellcasting classes — Wizard, Sorcerer, Warlock, Cleric, Druid, Bard — and INT/WIS/CHA as spellcasting stats.
 
| Axis | Pole A | Pole B | D&D Roots |
|---|---|---|---|
| Arcane / Divine | Arcane | Divine | Wizard/Sorcerer vs Cleric/Paladin |
| Studied / Innate | Studied | Innate | Wizard (spellbook) vs Sorcerer (bloodline) |
| Magic / Martial | Magic | Martial | Full caster vs non-caster |
| Knowledge / Instinct | Knowledge | Instinct | INT vs WIS; Wizard vs Druid |
| Control / Destruction | Control | Destruction | Crowd control spells vs damage spells |
 
*A high Arcane/Studied/Control character is a classic Wizard. High Divine/Innate/Destruction suggests a Warlock or wild Sorcerer. High Martial sits at the non-magic end.*
 
---
 
## Social & Subterfuge
 
Derived from CHA-based skills (Persuasion, Deception, Intimidation, Performance) and DEX-based subterfuge skills (Stealth, Sleight of Hand).
 
| Axis | Pole A | Pole B | D&D Roots |
|---|---|---|---|
| Persuasion / Intimidation | Persuasion | Intimidation | CHA: charm vs fear |
| Truth / Deception | Truth | Deception | Insight vs Deception skill |
| Open / Stealthy | Open | Stealthy | Presence vs Stealth skill |
| Diplomacy / Manipulation | Diplomacy | Manipulation | Honest negotiation vs cunning |
| Fame / Infamy | Fame | Infamy | Positive vs negative reputation |
 
*A high Persuasion/Truth/Diplomacy character is the classic Paladin or noble. High Deception/Stealthy/Manipulation is the Rogue or Warlock. A Bard might sit interestingly in the middle of several of these.*
 
---
 
## Exploration & Survival
 
Derived from WIS and INT skills — Perception, Survival, Nature, Investigation, Medicine — and the classic adventuring loop.
 
| Axis | Pole A | Pole B | D&D Roots |
|---|---|---|---|
| Caution / Boldness | Caution | Boldness | Careful scouting vs charging in |
| Nature / Civilization | Nature | Civilization | Druid/Ranger vs Urban Rogue/Wizard |
| Perception / Concealment | Perception | Concealment | Passive Perception vs Stealth |
| Preparation / Improvisation | Preparation | Improvisation | Long rest planning vs short rest scrapping |
| Healing / Harm | Healing | Harm | Medicine/Cleric support vs damage dealing |
 
---
 
## Character & Fate
 
Derived from classic RPG character arcs, backstory tropes, and the D&D class fantasy of transformation and destiny.
 
| Axis | Pole A | Pole B | D&D Roots |
|---|---|---|---|
| Honor / Pragmatism | Honor | Pragmatism | Paladin code vs Rogue flexibility |
| Loyalty / Independence | Loyalty | Independence | Party cohesion vs lone wolf |
| Courage / Cunning | Courage | Cunning | Barbarian/Paladin vs Rogue/Wizard |
| Hope / Despair | Hope | Despair | Classic hero arc |
| Sanity / Madness | Sanity | Madness | Lovecraftian / Warlock patron pressure |
| Mortal / Transcendent | Mortal | Transcendent | Human limits vs divine/arcane ascension |
 
---
 
## Health & Resources
 
These are the axes most directly useful as *mechanical stats* in a simplified ruleset — they have clear numeric ranges and obvious scene impacts.
 
| Axis | Pole A | Pole B | D&D Roots |
|---|---|---|---|
| Healthy / Wounded | Healthy | Wounded | Hit points |
| Rested / Exhausted | Rested | Exhausted | Exhaustion levels |
| Resourced / Spent | Resourced | Spent | Spell slots, abilities, items |
| Composed / Shaken | Composed | Shaken | Morale, fear, concentration |
 
*These are the most natural per-character axes for scene resolution. A character reduced to high Wounded + high Exhausted is in serious trouble mechanically. A Paladin with a martyr goal might specifically want to end scenes at high Wounded.*
 
---
 
## Notes on Usage
 
### As character stats
Pick 3–5 axes per character and assign starting positions. High Brawn + high Rage + high Offense = a Barbarian. High Studied + high Arcane + high Knowledge = a Wizard. The position on each axis replaces the D&D ability score for that domain.
 
### As scene goals
A character with a hidden goal of "advance Deception" will try to solve scenes through manipulation regardless of outcome. A character chasing "advance Healing" wants to keep allies alive. These pull against each other naturally.
 
### Decoupling capability from incentive
A character can be *mechanically* high Brawn but have a *narrative goal* of advancing Diplomacy — the cursed warrior trying to leave violence behind. Capability and incentive don't have to match, and that tension is interesting.
 
### Mapping D&D outcomes to axis shifts
- Win a combat encounter → Offense shifts up, or Healing shifts up (if lives were saved)
- Negotiate past a guard → Persuasion/Diplomacy shifts up
- Sneak through a dungeon → Stealthy shifts up, Open shifts down
- Lose a fight badly → Wounded shifts up, Courage may shift toward Cunning
- Use dark magic to win → Arcane shifts up, potentially Evil shifts up
 
