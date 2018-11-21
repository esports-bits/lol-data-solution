# LoL Data Solution

# Dependencies
* [RiotWatcher](https://riot-watcher.readthedocs.io/en/latest/).
* [MongoDB](https://www.mongodb.com).

# Features
It generates datasets of stats of the matches from:
* Official Riot Games competitions such as SLO, LEC, LCK, and so on.
* Solo queue.
* Scrims.

To create those datasets it needs some indications. The MongoDB has the structure to store information about competitions, teams and players. With that information the application just needs to know what team, competition or region you want the dataset from and within what dates or versions (patches) of the game.
