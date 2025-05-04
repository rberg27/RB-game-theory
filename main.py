import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from model.market.team_need import calculate_team_need, get_free_agent_rating
from model.team.team_model import TeamModel

def evaluate_free_agents():
    """
    Evaluates free agents against all teams to determine projected win improvements.
    Creates and visualizes a heatmap of the results.
    """
    # Load free agents data
    free_agents_path = os.path.join('.', 'data', 'freeAgents2016.csv')
    free_agents_df = pd.read_csv(free_agents_path)
    
    # Load all players data from Excel file
    all_players_path = os.path.join('.', 'all_players_15_23.xlsx')
    all_players_df = pd.read_excel(all_players_path)
    
    # Load teams data from Excel file
    teams_path = os.path.join('.', 'madden_data_processed.xlsx')
    all_teams_df = pd.read_excel(teams_path)
    
    # Filter teams data for 2015
    all_teams_df_2015 = all_teams_df[all_teams_df['year'] == 2015]
    
    # Get unique team names
    team_names = all_teams_df_2015['team_name'].unique()
    
    # Create empty list to store results
    results = []
    
    print("Free Agents Available:")
    for _, player_row in free_agents_df.iterrows():
        try:
            player_name = player_row['Name']
            print(f"\nEvaluating free agent: {player_name}")
            
            # Get player's overall rating
            player_rating = get_free_agent_rating(player_name, all_players_df)
            if player_rating is None:
                print(f"Could not find rating for {player_name}, skipping...")
                continue
                
            print(f"{player_name} - Overall Rating: {player_rating}")
            
            # Evaluate player for each team
            for team_name in team_names:
                try:
                    # Calculate team need for this player
                    need_result = calculate_team_need(
                        player_name=player_name,
                        team_name=team_name,
                        year=2015,  # Using 2015 team data
                        all_players_df=all_players_df,
                        all_teams_df=all_teams_df
                    )
                    
                    if need_result:
                        win_improvement = need_result['win_improvement']
                        print(f"  {team_name}: Expected win improvement: {win_improvement:.2f}")
                        
                        results.append({
                            'player_name': player_name,
                            'player_rating': player_rating,
                            'team_name': team_name,
                            'current_wins': need_result['current_win_prediction'],
                            'projected_wins': need_result['win_prediction_with_player'],
                            'win_improvement': win_improvement
                        })
                except Exception as e:
                    print(f"Error evaluating {player_name} for {team_name}: {str(e)}")
        except KeyError as e:
            print(f"Error processing free agent: {str(e)}")
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    if results_df.empty:
        print("No results to visualize. Check for errors above.")
        return results_df
    
    # Sort results by win improvement to find best matches
    best_matches = results_df.sort_values('win_improvement', ascending=False).head(10)
    print("\nTop 10 Player-Team Matches:")
    for _, match in best_matches.iterrows():
        print(f"{match['player_name']} to {match['team_name']}: +{match['win_improvement']:.2f} wins")
    
    # Create a pivot table for heatmap visualization
    try:
        heatmap_data = results_df.pivot_table(
            index='player_name', 
            columns='team_name', 
            values='win_improvement'
        )
        
        # Visualize with heatmap
        plt.figure(figsize=(16, 12))
        sns.heatmap(heatmap_data, cmap='RdYlGn', center=0, annot=True, fmt='.2f')
        plt.title('Projected Win Improvement by Free Agent and Team')
        plt.ylabel('Free Agent')
        plt.xlabel('Team')
        plt.tight_layout()
        
        # Save the figure
        output_dir = os.path.join('..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'free_agent_team_heatmap.png'))
        
        # Also save the data
        results_df.to_csv(os.path.join(output_dir, 'free_agent_projections.csv'), index=False)
        
        print(f"\nAnalysis complete. Results saved to {output_dir}")
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
    
    return results_df

if __name__ == "__main__":
    evaluate_free_agents()
