# MAD Lions E.C. LoL Data Solution
Professional teams have the need to manage the data they generate every day and the tools available in the market are too expensive for what they offer, even for top tier teams. With this solution, teams are able to generate datasets of whoever's solo queue games, competitions such as SLO or LCS, and scrims. The datasets are exported in XLSX or CSV format. Both are pretty popular formats and can be imported in visualization softwares such as Tableau and Spotfire to quickly analyse the data.

# Features
## Data bases
The application needs to connect to two data sources in order to work. One is a Mongo DB that will be used to store matches raw data and the other is a Maria DB that is used to store all the information related to players, teams and competitions.

### Mongo DB
Post game and timeline raw data is stored in this DB, as mentioned before. Thanks to that, making queries to get statistics for specific matches is pretty easy and quick, and there is no need of keep making calls to the API which takes much longer because of rate limits.

For every scenario it is needed to create two collections, one for the post game statistics and the other for the timeline statistics. For example:
* LCS EU. 
  * lcs_eu_m: for post game stats.
  * lcs_eu_tl: for timeline stats.
* Solo queue.
  * soloq_m: for post game stats.
  * soloq_tl: for timeline stats.

And so on and so forth.

The DB is also used for storing the static data of the game. This data relates the identifiers of the items, champions, runes, etc. with their names, descriptions and whatever. The raw data we store in the this DB lacks of this information, so we need to merge it before generating any dataset.

### Maria DB
In this case, the SQL DB is used to store all the relevant information of the players, teams and competitions we mess up with. Basically what is needed is a place to have all the relations between players teams and competitions because the Riot API doesn' have that. To have that context helps a lot when analysing data.

## Official competitions
Manage data from competitions such as LCS EU or Superliga Orange and export the statistics. [WIP]


## Scrims
[WIP]

## Solo queue
[WIP]
