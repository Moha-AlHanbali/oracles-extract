# Oracle's Extract

## Purpose

- Oracle's Extract uses League of Legends filtered Match data to elect the statistically superior build path for a champion, based on the player's team and enemy team compositions,and most commonly bought items in similar situations.

- This program is based off [league-advisor ranked items feature](https://github.com/League-Advisor/league-advisor).

- [league-advisor match_data_scraper](https://github.com/League-Advisor/league-advisor) module can be used to collect and filter data for this program.

- Included data is viable up to patch 11.24 (Pre-Season 12) and uses matches from NA server only.

## To Do

- [x] Gather enough Data samples
- [x] Clean Data (if needed)
- [x] Convert Data format
- [x] Read Data
- [x] Filter Matches with the selected Champion is present
- [x] Filter Winning Cases
- [x] Most commonly bought in winning cases
- [x] Filter relevant compositions
- [x] Return Most commonly bought items in similar cases
- [x] Return the 'most winning' item builds
- [x] Add tolerance threshold
- [x] Create a program to input 'request' Data
- [x] Replace sample Data with new, sufficient Dataset
- [x] Convert Item Keys to Item Names
