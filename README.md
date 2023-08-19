# Tools
A collection of independent tools for various purposes.

# Contents
- [Requirements](#requirements)
- [Money Lost](#money-lost)
- [League of Legends Matches](#league-of-legends-matches)

# Requirements
- `config.env`: Copy `example_config.env` and fill in the values.
- `requirements.txt`: Install the required packages with `pip install -r requirements.txt`.

# Money Lost
A tool to calculate how much money you lost in the exchange rate when you bought something in a foreign currency.

Requires Open Exchange Rates API key. You can get one for free [here](https://openexchangerates.org/signup/free).

## Usage
You can use the tool by running the `main.py` file with the `money_lost` command.
It will print the help message if you don't provide any arguments.
```commandline
> py .\main.py money_lost -f RON -t EUR -s 4200 -b 845.05
Success: Environment variables loaded successfully.
 Your rate:      4.970 RON / per EUR
 Real rate:      4.939 RON / per EUR

Your value:    845.050 EUR
Real value:    850.460 EUR
------------------------------
Difference:      5.410 EUR
```

# League of Legends Matches
A tool to get the matches of a League of Legends player.

Requires Riot Games API key. You can get one [here](https://developer.riotgames.com/).

## Usage
You can use the tool by running the `main.py` file with the `lol` command.
It will print the help message if you don't provide any arguments.
```commandline
> py .\main.py lol -n extremq -r EUN1 -s 2023-08-19 -o output.csv
Success: Environment variables loaded successfully.
Info: Found summoner 'extremq' with puuid 'lcnPkpKslAEs9y1DnocGbNmu6zeCt_vrrDLOgr5jhBRny_UA_bkBgcbHxlvHTfiKbonKgAdsMaUpiA'.
Info: Got 9 more matches.
Info: Got 0 more matches.
Info: Finished getting 9 matches.
Info: Got match data for EUN1_3437910600
Info: Got match data for EUN1_3437873539
Info: Got match data for EUN1_3437868277
Info: Got match data for EUN1_3437858543
Info: Got match data for EUN1_3437847970
Info: Got match data for EUN1_3437841882
Info: Got match data for EUN1_3437843644
Info: Got match data for EUN1_3437837683
Info: Got match data for EUN1_3437840463
Info: Turned data into dataframe.
Info: First 5 rows of dataframe:
   allInPings  assistMePings  assists  baitPings  baronKills  basicPings  bountyLevel  champExperience  ...                      gameName  gameStartTimestamp      gameType     gameVersion  mapId  platformId  queueId  tournamentCode
0           0              0       31          0           0           0            0            16856  ...  teambuilder-match-3437910600       1692439821909  MATCHED_GAME  13.16.525.6443     12        EUN1      450               
 
1           0              0       28          0           0           0            0            20106  ...  teambuilder-match-3437873539       1692433683289  MATCHED_GAME  13.16.525.6443     12        EUN1      450               
 
2           0              0       32          0           0           0            1            20396  ...  teambuilder-match-3437868277       1692432283412  MATCHED_GAME  13.16.525.6443     12        EUN1      450               
 
3           0              0        4          0           0           0            7            13383  ...  teambuilder-match-3437858543       1692430294637  MATCHED_GAME  13.16.525.6443     11        EUN1      400               
 
4           1              2       14          0           0           0            0            14320  ...  teambuilder-match-3437847970       1692427895863  MATCHED_GAME  13.16.525.6443     11        EUN1      400               
 

[5 rows x 141 columns]
Success: Successfully saved 9 matches to 'output.csv'.
```