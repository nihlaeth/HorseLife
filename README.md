# HorseLife
A simple python game



## Directories

### assets
Here you can find all the graphical and audio assets that belong to the game

### backend
This is what talks databases. It passes models to the core (read: does sql and stuff).

### config
.ini files that configure the generation of content. For example, files that 
set the general traits for specific horse breeds, files that deal with the
traits and wages of employees, etc.

### core
The middle layer between the interface and the backend. Here is where the game logic
lives.

### interface
The available interfaces are housed here. This is code that deals with the pesky graphical stuff.

The interfaces are easily interchangeable, and completely separated from game logic and database.

### lang
Internationalization. For now, this has low priority.

### models
Database structure. Since we use object relational mapping, this is also where you'll find the bulk of the game logic.

### saves
The databases (read: saved games) will go here.

### tests
Well... Tests.
