How to run this project:

1. Edit main.py with the year that you want to analyze
2. Run main.py

The output will share the forecast for which player will go for which amount. The output folder will include a heatmap of team needs for certain players.




Folders
- data
  - this folder holds data generated from scripts run for this project
  - data files
      - freeAgents...csv
          - data for free agent running back contracts since 2011
      - nfl_cap_space_2015_2025.csv
          - data for cap space of each team since 2015
      - player_data.csv
          - season statistics for running backs since ~1940
      - players.csv
          - list of players and links to their data pages since ~1940
      - predictions.csv
          - output of the running back value regression model. There are multiple columns but it is sorted by pred_std_combo column to rank which running backs have the highest value contracts

- scripts
  - this folder holds the scripts used to generate data files and end results
  - script files
      - rb_data.py
        - File used to create free agent data files as well as run the regression model to predict running back values
        - meant to be run in top level dir for pathing reason, especially when sum is present
        - Run options:
          - type: command specifying what action the script will take
            - name: gets all running back names -> players.csv,
            - pull: get data for each year given running back names -> player_data.csv
            - sum: get free agent data for a specific year
            - model: run the model to predict free agent running back contract values for 2025
          - players: file location for player names
          - data: file location for player data
          - year: year of free agency
        - some example of runs would be python scripts\rb_data.py --type name || python scripts\rb_data.py --type model --data data\player_data.csv
      - season_outcomes.py
        - Initial attempt for a independant variable in our models, no longer useful as wins were not indicative of running back performance
