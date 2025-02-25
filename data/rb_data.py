import string
import requests
import pandas as pd
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

def main():
    urls = [f"https://www.pro-football-reference.com/players/{letter}/" for letter in string.ascii_uppercase]
    players = pd.DataFrame(columns=['name', 'position', 'years', 'link'])
    for url in urls:
        players = pd.concat([players, get_players(url)], ignore_index=True)
    print(players)



# ------------------------------------------------------------------------------------------------------------------------

# # URL for the player's page
# url = "https://www.pro-football-reference.com/players/B/BadaRi00.htm"
# headers = {"User-Agent": "Mozilla/5.0"}

# # Fetch the page
# response = requests.get(url, headers=headers)
# if response.status_code != 200:
#     raise Exception(f"Failed to fetch page: {response.status_code}")

# # Parse the HTML
# soup = BeautifulSoup(response.text, "html.parser")

# # Find the table with id "rushing_and_receiving"
# table = soup.find("table", id="rushing_and_receiving")
# if table is None:
#     raise Exception("Table with id 'rushing_and_receiving' not found!")

# # Option 1: Use pandas to read the table directly from the HTML snippet.
# # First, convert the table to a string and then read it with pandas.
# table_str = str(table)
# dfs = pd.read_html(table_str)
# if len(dfs) > 0:
#     df = dfs[0]
# else:
#     print("No table could be parsed.")

# ------------------------------------------------------------------------------------------------------------------------

# df_filtered = df[df[( 'Unnamed: 3_level_0',     'Lg')].str.contains("NFL", case=False, na=False)]
# def combine_levels(col_tuple):
#     # Filter out any empty strings that might result from missing values in the MultiIndex
#     return '_'.join(filter(None, [str(x).strip() for x in col_tuple if x and 'Unnamed' not in str(x)]))

# df_filtered.columns = [combine_levels(col) for col in df.columns.values]
# df_filtered


if __name__ == "__main__":
    main()
