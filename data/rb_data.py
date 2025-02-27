import time
import string
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


def main():
    # urls = [f"https://www.pro-football-reference.com/players/{letter}/" for letter in string.ascii_uppercase]
    # players = pd.DataFrame(columns=['name', 'position', 'years', 'link'])
    # for url in tqdm(urls):
    #     time.sleep(30)
    #     players = pd.concat([players, get_players(url)], ignore_index=True)
    # players.to_csv("players.csv", index=False) 
    pd.options.mode.chained_assignment = None 
    players = pd.read_csv("players.csv")
    player_data = pd.DataFrame(columns = [
                                "Name", "Season", "Age", "Team", "Lg", "Pos", "G", "GS", "Rushing_Att", 
                                "Rushing_Yds", "Rushing_TD", "Receiving_Lng", "Receiving_R/G", 
                                "Receiving_Y/G", "Scrimmage_Touch", "Scrimmage_Y/Tch", 
                                "Scrimmage_YScm", "Scrimmage_RRTD", "Fmb", "AV", "Awards"
                                ])
    for _, player in tqdm(players.iterrows()):
        player_data = pd.concat([player_data, get_player_data(f'https://www.pro-football-reference.com{player.link}', player.iloc[0])], ignore_index=True)
        time.sleep(12)
    player_data.to_csv("player_data.csv", index=False) 





if __name__ == "__main__":
    main()
