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
    print(teams.head() if not teams.empty else "No teams found")

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
