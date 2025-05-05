import pandas as pd
import os

def get_project_root():
    """Get the absolute path to the project root directory"""
    # Assume this file is in the model directory, get parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return project_root

def get_file_path(relative_path):
    """Convert a relative path to an absolute path from project root"""
    return os.path.join(get_project_root(), relative_path)

def get_free_agents_by_year(year):
    """
    Returns a list of free agent running backs for a given year.
    
    Args:
        year (int): The year to filter free agents for
        
    Returns:
        pandas.DataFrame: DataFrame containing free agents for the specified year
    """
    file_path = get_file_path("./model/nfl_rb_free_agents_madden_2015_2024.csv")
    free_agents_df = pd.read_csv(file_path)
    free_agents_df = free_agents_df[free_agents_df['Season'] == year]
    return free_agents_df
    
def get_teams_by_year(year):
    """
    Returns a list of NFL teams for a given year.
    
    Args:
        year (int): The year to filter teams for
        
    Returns:
        pandas.DataFrame: DataFrame containing teams for the specified year
    """
    file_path = get_file_path("./model/madden_data_processed.xlsx")
    teams_df = pd.read_excel(file_path)
    teams_df = teams_df[teams_df['year'] == year]
    return teams_df

def get_team_cap_for_year(team_name, year):
    """
    Returns the cap space for a specific team in a given year.
    
    Args:
        team_name (str): The name of the team (e.g., "PHI")
        year (int): The year to get cap space for
        
    Returns:
        float: The cap space value for the specified team and year
    """
    # Dictionary to convert full team names to abbreviations
    team_name_to_abbr = {
        "Arizona Cardinals": "ARI",
        "Atlanta Falcons": "ATL",
        "Baltimore Ravens": "BAL",
        "Buffalo Bills": "BUF",
        "Carolina Panthers": "CAR",
        "Chicago Bears": "CHI",
        "Cincinnati Bengals": "CIN",
        "Cleveland Browns": "CLE",
        "Dallas Cowboys": "DAL",
        "Denver Broncos": "DEN",
        "Detroit Lions": "DET",
        "Green Bay Packers": "GB",
        "Houston Texans": "HOU",
        "Indianapolis Colts": "IND",
        "Jacksonville Jaguars": "JAX",
        "Kansas City Chiefs": "KC",
        "Los Angeles Chargers": "LAC",
        "Los Angeles Rams": "LAR",
        "Las Vegas Raiders": "LV",
        "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN",
        "New England Patriots": "NE",
        "New Orleans Saints": "NO",
        "New York Giants": "NYG",
        "New York Jets": "NYJ",
        "Oakland Raiders": "OAK",
        "Philadelphia Eagles": "PHI",
        "Pittsburgh Steelers": "PIT",
        "San Diego Chargers": "SD",
        "Seattle Seahawks": "SEA",
        "San Francisco 49ers": "SF",
        "St. Louis Rams": "STL",
        "Tampa Bay Buccaneers": "TB",
        "Tennessee Titans": "TEN",
        "Washington Commanders": "WAS",
        "Washington Football Team": "WAS",
        "Washington Redskins": "WAS"
    }
    
    # Get team abbreviation
    team_abbr = team_name_to_abbr.get(team_name)
    if not team_abbr:
        return None
    
    file_path = get_file_path("./model/nfl_cap_space_2015_2025.csv")
    cap_space_df = pd.read_csv(file_path)
    
    # Find the row for the specified team
    team_row = cap_space_df[cap_space_df['Team'].str.contains(team_abbr)]
    
    if team_row.empty:
        return None
    
    # Get the cap space for the specified year
    if str(year) in team_row.columns:
        cap_space = team_row[str(year)].values[0]
        # Remove $ and commas, then convert to float
        if isinstance(cap_space, str):
            cap_space = float(cap_space.replace('$', '').replace(',', '').replace('"', ''))
        return cap_space
    else:
        return None

if __name__ == "__main__":
    # Test the free agency functions
    print("Testing free agency module...")
    print(f"Project root: {get_project_root()}")
    
    # Test getting free agents for 2024
    test_year = 2024
    free_agents = get_free_agents_by_year(test_year)
    print(f"\nFree agents for {test_year}:")
    print(free_agents.head() if not free_agents.empty else "No free agents found")

    # Test getting teams for 2024
    teams = get_teams_by_year(test_year)
    print(f"\nTeams for {test_year}:")
    print(teams.head())

    # Check if teams dataframe has the expected columns
    if not teams.empty and 'team_name' in teams.columns and 'HB1' in teams.columns:
        # Print HB for Eagles in 2024
        eagles_2024 = teams[teams['team_name'] == 'Philadelphia Eagles']
        if not eagles_2024.empty:
            print(eagles_2024["HB1"])
        else:
            print("No data for Philadelphia Eagles in 2024")
    else:
        print("Teams dataframe does not have expected columns or is empty")
        
    # Test getting team cap for 2024
    team_cap = get_team_cap_for_year("Philadelphia Eagles", test_year)
    print(f"\nTeam cap for Philadelphia Eagles in {test_year}: {team_cap}")
