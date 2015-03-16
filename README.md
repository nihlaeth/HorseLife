# HorseLife
A simple python game



## Directories

### assets
Here you can find all the graphical and audio assets that belong to the game

### config
.ini files that configure the generation of content. For example, files that 
set the general traits for specific horse breeds, files that deal with the
traits and wages of employees, etc.

### interface
The available interfaces are housed here. I try to keep a strict separation between
code that deals with graphical stuff and anything that deals with the database. This
was it's easier to swap out an interface. But mostly it makes it easier for me not to
worry about anything graphical during the early stages of development.

### lang
Internationalization. For now, this has low priority.

### models
Database structure. Since we use object relational mapping, this is also where you'll find the bulk of the game logic.

### saves
The databases (read: saved games) will go here.

### tests
Well... Tests.
