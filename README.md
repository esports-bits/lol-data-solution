# MAD Lions E.C. LoL Data Solution
Professional teams have the need to manage the data they generate every time their players practice in LoL, and the tools available in the market are either non existent or too expensive for what they offer, even for top tier teams. With this solution, teams are able to generate datasets of whoever's solo queue games, official competitions (SLO, LCS, LCK, etc.) and scrims. The datasets are exported in XLSX or CSV format. Both are pretty popular formats and can be imported in visualization softwares such as Tableau and Spotfire to quickly analyse the data and make graphs like the following ones.


# Needs
## Data bases
The application needs to connect to two data sources in order to work. One is a Mongo DB that will be used to store matches raw data and the other is a Maria DB that is used to store all the information related to players, teams and competitions.

### Mongo DB
Post game and timeline raw data is stored in this DB, as mentioned before. Thanks to that, making queries to get statistics for specific matches is pretty easy and quick, and there is no need of keep making calls to the API which takes much longer because of rate limits.

For every scenario it is needed to create two collections, one for the post game statistics and the other for the timeline statistics. For example:
- LCS EU. 
	- **lcs_eu_m**: for post game stats.
	- **lcs_eu_tl**: for timeline stats.
- Solo queue.
	- **soloq_m**: for post game stats.
	- **soloq_tl**: for timeline stats.

And so on and so forth.

The DB is also used for storing the static data of the game. This data relates the identifiers of the items, champions, runes, etc. with their names, descriptions and whatever. The raw data we store in the this DB lacks of this information, so we need to merge it before generating any dataset.

### Maria DB
In this case, the **SQL** database is used to store all the relevant information of the **players**, **teams** and **competitions** we mess up with. Basically, what I wanted is a place to have all the relations between players teams and competitions due to the lack of this information in **Riot's API**, and it's needed because having that context is what let us export the data needed and analyze it properly at the end.

# Features

## Download
Thanks to all the information that is stored in the data bases, this tool can download game data from every summoners rift game played in any kind of context. LDS will let you select which teams or competitions you want to download data from and which kind of data: Solo Queue or Official Matches. It will automatically select the members of the team or the competition based on the data stored in **MariaDB** and start downloading the most recent matches of every player or competition (matches already downloaded are skipped).

## Export
The export result is a **XLSX** file with all the **post-game** and some of the **timeline** aggregated **stats**. When exporting it is possible to select teams and competitions to export data as well, but it is also possible to select begin and end time, patch, splits, seasons and almost whatever thanks to the endless possibilities of the **MongoDB** queries. TLDR of export options:

 - **Teams**. Select one or more teams to export their data (Solo Queue environment only for now). E.g.: MAD, FNC, SKT, etc.
 - **Competition**. Select one competition and export all the data (Solo Queue environment only for now). E.g.: SLO, EULCS, LCK, etc.
 - **Patch**. Select the patch or patches that you want data from. E.g.: 
	 - "8" will select all patches within version 8.
	 - "8.1" will select all patches within that specific version like: 8.11, 8.12, etc.
 - **Begin time** and **end time**. Both operate as different parameters. Select the begin time of the games, the end time of the games or both at the same time having then a time interval.
 - Split.
 - Season.

## Official competitions
Manage data from competitions such as LCS EU or Superliga Orange and export the statistics. [WIP]


## Scrims
[WIP]

## Solo queue
[WIP]
