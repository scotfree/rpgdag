# rpgdag

# Architecture: 
* A game server runs as a simple python service under gunicorn and FastAPI with very simple deployment and architecture so we can serve the API later using serverless and an API gateway with a minimum of changes.
* A simple single page HTML/JS client will provide an interface to the game. Users should use SSO login with google, then view the game state via the API.
* All game state should be held serverside. For now this will just be a JSON file.

# Game
* A game is a DAG, called the "game graph".
  * Each node represents a single scene of live tabletop RPG play which will happen offline - not in the app or client.
  * A full game will be a path through these nodes.
  * The context and goals for a scene will be set by the game state and player choices.
  * Players will then choose the Scene GM, who will run the scene using some external set of rules.
  * On finishing the scene, the GM will enter the game impacts of the scene that was played.
  * The group of players will then chose which edge to follow out from the scene node, and thus which node will be next.
* Users will have a role as a player character. This character will be specified in some extedrnal set of rules, and stored elsewhere.
* Another key component is the set of "game axes"
  * each axis has two "directions" and a value.
  * The directions represent two opposing aspects of the game world. Examples might include:
    * capitalism / communism
    * evil / good
    * magic / technology
    * north / south
    * hot / cold
    * fire / water
  * the value represents the balance between the two axis directions at a point in time
  * each scene node will define an impact on different axes for outcomes of the scene. Some examples:
    *  fight - party wins, +1 Good; monsters win +1 evil
    *  vote - candidat A wins +1 capitalism, party B wins +1 communism
    *  forest fire - prevented +1 cold, ignited +1 hot
  *  edges may also have axis impacts
* When the game finishes there will be victory conditions for the party and each character
  * the party VC represents the overall narrative success of the party, usually represented by a node on the graph.
  * each characters VC will be defined as a position on an axis (or set of them). Examples:
    * communism > 5
    * technology > 10
  * so at the end of a game, the party will succeed or fail together, but there will be a player winner based on the axes state
* Game configurations will thus include
  * general metadata
    * name
    * description
    * start and destination nodes
    * player VCs
    * background - art or color used for background
    * game meta configuration, such as:
      * narrative fog: players can only see the nodes they have already visited, not "downstream" or "future" nodes
      * traitor mode: player can win even if party has failed
  * nodes, each comprising:
    * name
    * description
    * art (link to image)
    * scene stats
    * list of outcomes:
      * simple boolean questions
      * impact lists for True and False answers
      * impact may be another outcome? Or early exit from list?
    * color
  * edges - representing paths between scene nodes, each desribing
    * name
    * song (link to song or just a name)
    * axis impacts
  
