# HorseLife
A simple python game

## State
This game is pre-alpha right now. Don't try to run it,
because it won't work. Or it might, but it won't be much
of a game.

## Planned features
* detailed training - training of individual skills instead of just "jumping" or "dressage"
* complicated and realistic competitions
* personell that needs to be planned, and does work in realtime
* lessons where the participants pay, groom their horses and actually get better at riding.
* horse owners pay for facilities, expect there to be training opportunities, and go through their day in realtime
* breeding with detailed trait system and small chance of twins
* horses have (genetic) character traits that influence their behavior and training
* extensive goals and grants system to encourage gameplay
* horses get injured once in a while
* older horses are unable to compete on a high level, don't have as much energy, etc. Option to send them to a retirement home for a fee.
* horses interact and have a social need. Some horses they dislike, others they like. This influence riding lessons and pasture behavior (and injuries)
* features are progressively unlocked to ease the player into them
* different types of food are more suited for rigorous exercise or light workouts
* education system so the player can perform certain jobs themselves (e.g. learn to teach, become a vet, etc.)

## Included features
Right now, none. The game is little more than a single stable
with a horse in it. You can clean the stable and the horse
gets unhappy with time. And to add insult to injury, the
horse doesn't even care if the stable is clean or not.

## TODO
For planned features, see above. This is about stuff that NEEDS to happen
in the codebase as it is right now. More a list for myself than for anyone
else's benefit, but I need to dump it somewhere (where I will see it).

* Add some comments. I know you get what this does right now, in a few weeks, you won't. Trust me on this one. For once.
* Check tests to see what can be isolated better
* Add notification system
* Add story progression
* Have needs check if their last_checked < now - don't do any of the work if it is equal to or greater than now.
* Add random 'events' - not the events already built-in. Happenings - finding something on the ground, a horse injuring itself, that kind of thing.
* Implement money
* Look at performance of TestStableCore, also at that of pass_time (still).
* Do a scan of the entire (reworked) code, see what needs refactoring.
* Add other building types (pastures, tack/feed rooms, headquarters, etc.)
* Implement horsemarket
* Start working on training system

## Directories

### assets
Here you can find all the graphical and audio assets that
belong to the game

### backend
This is what talks databases. It passes models to the core
(read: does sql and stuff).

### config
.cfg files that configure the generation of content. For 
example, files that set the general traits for specific
horse breeds, files that deal with the traits and wages
of employees, etc.

### core
The middle layer between the interface and the backend. This
is where the game logic lives.

### errors
Well, exceptions actually, but I couldn't name a module
exceptions for obvious reasons.

### generators
Content generators. They read the config files and use them to
construct new objects, buildings, animals, people, etc.

### interface
The available interfaces are housed here. This is code that
deals with the pesky graphical stuff.

The interfaces are easily interchangeable, and completely
separated from game logic and database.

### lang
Internationalization. For now, this has low priority.

### models
Database structure. Since we use object relational mapping,
this is also where you'll find the bulk of the game logic.

### saves
The databases (read: saved games) will go here.

### support
Some support classes and tools that don't really fit into 
either interface, core or backend.

### tests
Well... Tests.
