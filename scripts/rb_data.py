import time
import string
import argparse
import requests
import pandas as pd
from tqdm import tqdm
from io import StringIO
from bs4 import BeautifulSoup


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
    
def get_free_agent_data(url, year):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all player names
    players= []
    if (year == "2025"):
        for row in soup.select('table.table tbody tr'):
            player = {}
            columns = row.find_all('td')
            name_cell = row.find('a', {'class': 'link'})
            if name_cell:
                player['Name'] = name_cell.get_text(strip=True)
            players.append(player)
    else:
        for row in soup.select('table.table tbody tr'):
            player = {}
            columns = row.find_all('td')
            name_cell = row.find('a', {'class': 'link'})
            value_cell = row.find_all('td', {'class': 'text-center'})
            status = columns[-2].text.strip()
            if "UFA" not in status and "RFA" not in status and "ERFA" not in status and "UDFA" not in status:
                if name_cell:
                    player['Name'] = name_cell.get_text(strip=True)
                    player['Signed'] = True 
                if value_cell:
                    player['Years'] = value_cell[1].get_text(strip=True)
                    player['Value'] = value_cell[2].get_text(strip=True)
                    player['Total_GTD'] = value_cell[4].get_text(strip=True)
            else:
                if name_cell:
                    player['Name'] = name_cell.get_text(strip=True)
                    player['Years'] = 0
                    player['Signed'] = False
                    player['Years'] = 0
                    player['Value'] = 0
                    player['Total_GTD'] = 0
                
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
    return final_df
        


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
    if(args.players and args.type == "pull"):
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
    if(args.data and args.year and args.type == "sum"):
        player_data = pd.read_csv(args.data)
        url  = f"https://www.spotrac.com/nfl/free-agents/_/year/{args.year}/position/rb"
        free_agents = get_free_agent_data(url, args.year)
        free_agent_df = get_filtered_data(player_data, free_agents, args.year)
        free_agent_df.to_csv(f"./data/freeAgents{args.year}.csv", index=False) 




if __name__ == "__main__":
    main()
