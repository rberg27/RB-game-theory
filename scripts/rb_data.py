import re
import time
import string
import argparse
import requests
import pandas as pd
from tqdm import tqdm
from io import StringIO
from functools import reduce
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


HEADERS={"User-Agent": "Mozilla/5.0"}

def get_players(url):
    response = requests.get(url, headers=HEADERS)
    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        players_div = soup.find("div", id="div_players")
    
        # Lists to store data for each column
        names = []
        positions = []
        years = []
        links = []
         # Loop through each <p> in the players div
        for p in players_div.find_all("p"):
            # Assume that there is an <a> tag inside the <p> containing the player's name and link.
            a_tag = p.find("a")
            if a_tag:
                name = a_tag.text.strip()
                link = a_tag.get("href", "").strip()
                # Depending on the page structure, position may be in a <span> or as additional text.
                # Here's an example if it's in a <span>:
                span_tag = p.find("span")
                if span_tag:
                    position = span_tag.text.strip()
                else:
                    # Alternatively, if the position is part of the text after the <a> tag,
                    # you might try to extract it from the p.text and remove the name.
                    text = p.get_text(separator=" ", strip=True)
                    text = text.replace(name, "").strip()  # This is a heuristic.
                    pos_yr =text.split(')')
                    position = pos_yr[0][1:]
                    year = pos_yr[1]

            else:
                name = ""
                link = ""
                position = ""
                year = ""
            
            names.append(name)
            positions.append(position)
            links.append(link)
            years.append(year)
        
        # Create the DataFrame
        df = pd.DataFrame({
            "name": names,
            "position": positions,
            "years": years,
            "link": links
        })
    else:
        print(f"Failed to retrieve {url}: {response.status_code}")
    return df[df["position"].str.contains("RB", case=False, na=False)]

def combine_levels(col_tuple):
    # Filter out any empty strings that might result from missing values in the MultiIndex
    return '_'.join(filter(None, [str(x).strip() for x in col_tuple if x and 'Unnamed' not in str(x)]))

def get_player_data(url, name):
        # Fetch the page
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return pd.DataFrame()
    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table with id "rushing_and_receiving"
    table = soup.find("table", id="rushing_and_receiving")
    if table is None:
        return pd.DataFrame()

    # Option 1: Use pandas to read the table directly from the HTML snippet.
    # First, convert the table to a string and then read it with pandas.
    table_str = str(table)
    dfs = pd.read_html(StringIO(table_str))
    if len(dfs) > 0:
        df = dfs[0]
        df_filtered = df[df[( 'Unnamed: 3_level_0',     'Lg')].str.contains("NFL", case=False, na=False)]
        df_filtered.columns = [combine_levels(col) for col in df.columns.values]
        df_filtered['Name'] = name
        return df_filtered
    else:
        return pd.DataFrame()

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0
    
def get_free_agent_data(url, year):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all player names
    players= []
    if (year.strip() == "2025"):
        for row in soup.select('table.table tbody tr'):
            player = {}
            columns = row.find_all('td')
            name_cell = row.find('a', {'class': 'link'})
            if name_cell:
                player['Name'] = name_cell.get_text(strip=True).replace(".", "")
            if player['Name'] == 'Nyheim Miller-Hines':
                player['Name'] = 'Nyheim Hines'
            elif player['Name'] == 'Josh Kelley':
                player['Name'] = 'Joshua Kelley'
            elif player['Name'] == 'D’Ernest Johnson':
                player['Name'] = "D'Ernest Johnson"
            elif player['Name'] == 'JaMycal Hasty':
                player['Name'] = "Jamycal Hasty"
            elif player['Name'] == 'Larry Rountree III':
                player['Name'] = 'Larry Rountree'
            elif player['Name'] == 'Anthony McFarland':
                player['Name'] = 'Anthony McFarland Jr'
            players.append(player)
    else:
        for row in soup.select('table.table tbody tr'):
            player = {}
            columns = row.find_all('td')
            name_cell = row.find('a', {'class': 'link'})
            value_cell = row.find_all('td', {'class': 'text-center'})
            status = columns[-2].text.strip()
            if "UFA" not in status and "RFA" not in status and "ERFA" not in status and "UDFA" not in status and "CLUB" not in status:
                if name_cell:
                    player['Name'] = name_cell.get_text(strip=True).replace(".", "")
                    #player['Signed'] = True 
                if value_cell:
                    #player['Years'] = value_cell[1].get_text(strip=True)
                    #player['Value'] = value_cell[2].get_text(strip=True)
                    #player['Total_GTD'] = value_cell[4].get_text(strip=True)
                    player['Cap'] = safe_divide(int(value_cell[2].get_text(strip=True)[1:].replace(",", "")), int(value_cell[1].get_text(strip=True))) 
            else:
                if name_cell:
                    player['Name'] = name_cell.get_text(strip=True).replace(".", "")
                    # player['Years'] = 0
                    # player['Signed'] = False
                    # player['Value'] = 0
                    # player['Total_GTD'] = 0
                    player['Cap'] = 0
            if player['Name'] == 'Nyheim Miller-Hines':
                player['Name'] = 'Nyheim Hines'
            elif player['Name'] == 'Josh Kelley':
                player['Name'] = 'Joshua Kelley'
            elif player['Name'] == 'D’Ernest Johnson':
                player['Name'] = "D'Ernest Johnson"    
            elif player['Name'] == 'JaMycal Hasty':
                player['Name'] = "Jamycal Hasty"
            elif player['Name'] == 'Larry Rountree III':
                player['Name'] = 'Larry Rountree'
            elif player['Name'] == 'Anthony McFarland':
                player['Name'] = 'Anthony McFarland Jr'
            players.append(player)
    return players

def get_filtered_data(player_data, free_agents, year):
    player_data = player_data[player_data['Name'].isin([agent["Name"] for agent in free_agents])]
    player_data['Awards'] = player_data['Awards'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    player_data = player_data.drop(columns=['Team', 'Lg', 'Pos','Scrimmage_Touch', 'Scrimmage_Y/Tch', 'Scrimmage_YScm', 'Scrimmage_RRTD'])
    player_data = player_data.drop_duplicates(subset=['Name', 'Season'], keep='first')
    last_season_stats = player_data.copy(deep=True)

    player_data = player_data[player_data["Season"] < year]
    player_data = player_data.drop(columns=['Age','Season', 'Receiving_Lng', "Rushing_Lng"])
    player_data = player_data.groupby('Name', as_index=False).agg({'G': 'sum', 'GS': 'sum', 'Rushing_Att': 'sum', "Rushing_Yds": 'sum', "Rushing_TD": 'sum', "Receiving_R/G": "mean", "Receiving_Y/G": "mean",
                                                                   "Fmb": "sum", "AV": "sum", "Awards": "sum", "Rushing_1D": "sum", "Rushing_Succ%": "mean", "Rushing_Y/A": "mean", "Rushing_A/G": "mean",
                                                                   "Receiving_Tgt": "sum", "Receiving_Rec": "sum", "Receiving_Yds": "sum", "Receiving_Y/R": "mean", "Receiving_TD": "sum", "Receiving_1D": "sum",
                                                                   "Receiving_Succ%": "mean", "Receiving_Ctch%": "mean", "Receiving_Y/Tgt": "mean"})


    last_season_stats = last_season_stats.loc[last_season_stats.groupby('Name')['Season'].idxmax()]
    last_season_stats = last_season_stats.groupby('Name').last().reset_index()
    final_df = pd.merge(player_data, last_season_stats, on='Name', suffixes=('', '_last_season'))
    final_df = final_df.drop(columns='Season')
    final_df = pd.merge(final_df, pd.DataFrame(free_agents), on="Name", how="left")
    final_df = final_df.fillna(0).replace('', 0)
    return final_df

def model(train_data, test_data,  columns, model_name, standardize=True):
    d = train_data.copy(deep=True)
    t = test_data.copy(deep=True)
    y = d.iloc[:, -1]
    d = d.iloc[:, 1:-1]
    d = d[columns]
    names = t.iloc[:, 0]
    t = t.iloc[:, 1:]
    t = t[columns]
    if standardize:
        s = StandardScaler()
        d = s.fit_transform(d)
        t = s.fit_transform(t)
    X_train, X_test, y_train, y_test = train_test_split(d, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    predictions = model.predict(t)
    agent_predictions = pd.DataFrame({'Names': names, f'Pred_{model_name}': predictions})
    agent_predictions[f'Pred_{model_name}'] = agent_predictions[f'Pred_{model_name}'].apply(lambda x: max(x, 0)).astype(int)
    return (mse, agent_predictions)

def main():
    #THIS IS MEANT TO BE RUN FROM OUTSIDE OF THE SCRIPTS FOLDER from the base RB-GAME-THEORY folder
    pd.options.mode.chained_assignment = None 
    parser = argparse.ArgumentParser(description="What to do with RB Data")
    parser.add_argument(
        '--type', 
        type=str, 
        help="name: gets all running back names; pull: gets data for each year given running back names; sum: sum data before a given year for free agency purposes", 
        required=True
    )
    parser.add_argument(
        '--players', 
        type=str, 
        help="file location for player names", 
        required=False
    )
    parser.add_argument(
        '--data', 
        type=str, 
        help="file location for player data", 
        required=False
    )
    parser.add_argument(
        '--year', 
        type=str, 
        help="year of free agency", 
        required=False
    )
    args = parser.parse_args()
    if(args.type == "name"):
        urls = [f"https://www.pro-football-reference.com/players/{letter}/" for letter in string.ascii_uppercase]
        players = pd.DataFrame(columns=['name', 'position', 'years', 'link'])
        for url in tqdm(urls):
            time.sleep(30)
            players = pd.concat([players, get_players(url)], ignore_index=True)
        players.to_csv("./data/players.csv", index=False) 
    elif(args.players and args.type == "pull"):
        players = pd.read_csv(args.players)
        player_data = pd.DataFrame(columns = [
                                    "Name", "Season", "Age", "Team", "Lg", "Pos", "G", "GS", "Rushing_Att", 
                                    "Rushing_Yds", "Rushing_TD", "Receiving_Lng", "Receiving_R/G", 
                                    "Receiving_Y/G", "Scrimmage_Touch", "Scrimmage_Y/Tch", 
                                    "Scrimmage_YScm", "Scrimmage_RRTD", "Fmb", "AV", "Awards"
                                    ])
        for _, player in tqdm(players.iterrows()):
            player_data = pd.concat([player_data, get_player_data(f'https://www.pro-football-reference.com{player.link}', player.iloc[0])], ignore_index=True)
            time.sleep(12)
        player_data.to_csv("./data/player_data.csv", index=False)
    elif(args.data and args.year and args.type == "sum"):
        player_data = pd.read_csv(args.data)
        player_data['Name'] = player_data['Name'].str.replace('.', '')
        url  = f"https://www.spotrac.com/nfl/free-agents/_/year/{args.year}/position/rb"
        free_agents = get_free_agent_data(url, args.year)
        free_agent_df = get_filtered_data(player_data, free_agents, args.year)
        free_agent_df.to_csv(f"./data/freeAgents{args.year}.csv", index=False) 

    elif(args.data and args.type == "model"):
        dfs =  [pd.read_csv(f'{args.data}{year}.csv') for year in range(2011,2025)]
        data_2025 = pd.read_csv(f'{args.data}2025.csv')
        combined_df = pd.concat(dfs, ignore_index=True)
        full_columns = [ 'G', 'GS', 'Rushing_Att', 'Rushing_Yds', 'Rushing_TD',
       'Receiving_R/G', 'Receiving_Y/G', 'Fmb', 'AV', 'Awards', 'Rushing_1D',
       'Rushing_Succ%', 'Rushing_Y/A', 'Rushing_A/G', 'Receiving_Tgt',
       'Receiving_Rec', 'Receiving_Yds', 'Receiving_Y/R', 'Receiving_TD',
       'Receiving_1D', 'Receiving_Succ%', 'Receiving_Ctch%', 'Receiving_Y/Tgt',
       'Age', 'G_last_season', 'GS_last_season', 'Rushing_Att_last_season',
       'Rushing_Yds_last_season', 'Rushing_TD_last_season', 'Receiving_Lng',
       'Receiving_R/G_last_season', 'Receiving_Y/G_last_season',
       'Fmb_last_season', 'AV_last_season', 'Awards_last_season',
       'Rushing_1D_last_season', 'Rushing_Succ%_last_season', 'Rushing_Lng',
       'Rushing_Y/A_last_season', 'Rushing_Y/G', 'Rushing_A/G_last_season',
       'Receiving_Tgt_last_season', 'Receiving_Rec_last_season',
       'Receiving_Yds_last_season', 'Receiving_Y/R_last_season',
       'Receiving_TD_last_season', 'Receiving_1D_last_season',
       'Receiving_Succ%_last_season', 'Receiving_Ctch%_last_season',
       'Receiving_Y/Tgt_last_season']
        
        mse = {}
        mse_std_full, pred_std_full = model(combined_df, data_2025, full_columns, 'std_full')
        mse['Pred_std_full'] = mse_std_full
        print(mse_std_full)
        print(pred_std_full.sort_values(by='Pred_std_full', ascending=False))

        mse_full, pred_full = model(combined_df, data_2025, full_columns, 'full', standardize=False)
        mse['Pred_full'] = mse_full
        print(mse_full)
        print(pred_full.sort_values(by='Pred_full', ascending=False))

        career_columns = [ 'G', 'GS', 'Rushing_Att', 'Rushing_Yds', 'Rushing_TD',
       'Receiving_R/G', 'Receiving_Y/G', 'Fmb', 'AV', 'Awards', 'Rushing_1D',
       'Rushing_Succ%', 'Rushing_Y/A', 'Rushing_A/G', 'Receiving_Tgt',
       'Receiving_Rec', 'Receiving_Yds', 'Receiving_Y/R', 'Receiving_TD',
       'Receiving_1D', 'Receiving_Succ%', 'Receiving_Ctch%', 'Receiving_Y/Tgt',
       'Age']

        mse_std_career, pred_std_career = model(combined_df, data_2025, career_columns, 'std_career')
        mse['Pred_std_career'] = mse_std_career
        print(mse_std_career)
        print(pred_std_career.sort_values(by='Pred_std_career', ascending=False))

        mse_career, pred_career = model(combined_df, data_2025, career_columns, 'career', standardize=False)
        mse['Pred_career'] = mse_career
        print(mse_career)
        print(pred_career.sort_values(by='Pred_career', ascending=False))

        last_columns = [
       'Age', 'G_last_season', 'GS_last_season', 'Rushing_Att_last_season',
       'Rushing_Yds_last_season', 'Rushing_TD_last_season', 'Receiving_Lng',
       'Receiving_R/G_last_season', 'Receiving_Y/G_last_season',
       'Fmb_last_season', 'AV_last_season', 'Awards_last_season',
       'Rushing_1D_last_season', 'Rushing_Succ%_last_season', 'Rushing_Lng',
       'Rushing_Y/A_last_season', 'Rushing_Y/G', 'Rushing_A/G_last_season',
       'Receiving_Tgt_last_season', 'Receiving_Rec_last_season',
       'Receiving_Yds_last_season', 'Receiving_Y/R_last_season',
       'Receiving_TD_last_season', 'Receiving_1D_last_season',
       'Receiving_Succ%_last_season', 'Receiving_Ctch%_last_season',
       'Receiving_Y/Tgt_last_season']
        
        mse_std_last, pred_std_last = model(combined_df, data_2025, last_columns, 'std_last')
        mse['Pred_std_last'] = mse_std_last
        print(mse_std_last)
        print(pred_std_last.sort_values(by='Pred_std_last', ascending=False))

        mse_last, pred_last = model(combined_df, data_2025, last_columns, 'last', standardize=False)
        mse['Pred_last'] = mse_last
        print(mse_last)
        print(pred_last.sort_values(by='Pred_last', ascending=False))

        combo_columns = ['Rushing_Att', 'Rushing_Yds', 'Rushing_TD',
       'Receiving_R/G', 'Receiving_Y/G', 'Fmb', 'AV', 'Awards',
       'Age', 'G_last_season', 'GS_last_season', 'Rushing_Att_last_season',
       'Rushing_Yds_last_season', 'Rushing_TD_last_season', 'Receiving_Lng',
       'Receiving_R/G_last_season', 'Receiving_Y/G_last_season',
       'Fmb_last_season']
        
        mse_std_combo, pred_std_combo = model(combined_df, data_2025, combo_columns, 'std_combo')
        mse['Pred_std_combo'] = mse_std_combo
        print(mse_std_combo)
        print(pred_std_combo.sort_values(by='Pred_std_combo', ascending=False))

        mse_combo, pred_combo = model(combined_df, data_2025, combo_columns, 'combo', standardize=False)
        mse['Pred_combo'] = mse_combo
        print(mse_combo)
        print(pred_combo.sort_values(by='Pred_combo', ascending=False))

        smallest_key = min(mse, key=mse.get)
        d_list = [pred_std_full, pred_full, pred_std_career, pred_career, pred_std_last, pred_last, pred_std_combo, pred_combo]
        df_merged = reduce(lambda left, right: pd.merge(left, right, on='Names'), d_list).sort_values(by=smallest_key, ascending=False)
        print(f'Sorted on {smallest_key}')
        print(df_merged)

        df_merged.to_csv(f"./data/predictions.csv", index=False) 
if __name__ == "__main__":
    main()
