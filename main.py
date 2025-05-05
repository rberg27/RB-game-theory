import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from model.team_model import TeamModel, calculate_team_needs


import model.free_agency as free_agency
# Choose a year to evaluate
year = 2024
# Load free agent data
free_agents = free_agency.get_free_agents_by_year(year)
print(free_agents)

# Load team data from that year
teams = free_agency.get_teams_by_year(year)

# Calculate team need for each free agent
need_matrix = calculate_team_needs(free_agents, teams)

# Get team cap for each team
team_caps = {}
for team in teams['team_name']:
    team_cap = free_agency.get_team_cap_for_year(team, year)
    team_caps[team] = team_cap
print(team_caps)

# Visualize the results
print(need_matrix)

# Visualize the need matrix as a heatmap
if not need_matrix.empty:
    plt.figure(figsize=(16, 12))
    sns.heatmap(need_matrix, cmap='RdYlGn', annot=True, fmt='.2f')
    plt.title(f'Team Need Matrix for {year} Free Agents')
    plt.ylabel('Free Agent')
    plt.xlabel('Team')
    plt.tight_layout()
    
    # Save the heatmap
    output_dir = os.path.join('.', 'output')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'need_matrix_heatmap_{year}.png'))
    
    print(f"\nHeatmap saved to {output_dir}/need_matrix_heatmap_{year}.png")
else:
    print("Need matrix is empty, cannot create heatmap.")

# Run simulation 

def get_max_bid(team_name, player_name, team_caps, need_matrix, scaling_factor=1.0):
    """
    Returns the maximum amount a team can bid for a player based on need and available cap.
    Need score is scaled to reflect aggressiveness.
    """
    cap = team_caps.get(team_name, 0)
    need_score = need_matrix.at[player_name, team_name]
    
    # Normalize: turn need score into a % of cap to bid
    bid = min(cap, need_score * scaling_factor)
    return round(bid, 2)

def run_auction_for_player(player_name, need_matrix, team_caps):
    """
    Runs an auction for a player between the top 2 bidding teams.
    Returns the winning team and final bid amount.
    """
    # Get all bids
    bids = {
        team: get_max_bid(team, player_name, team_caps, need_matrix)
        for team in need_matrix.columns
    }

    # Sort by bid descending
    top_bidders = sorted(bids.items(), key=lambda x: x[1], reverse=True)[:2]

    if len(top_bidders) < 2:
        return top_bidders[0][0], top_bidders[0][1]  # Only one bidder

    team1, bid1 = top_bidders[0]
    team2, bid2 = top_bidders[1]

    # Simulate a small bidding war 
    winning_bid = max(bid1, bid2) + 0.1 * min(bid1, bid2)
    winning_bid = min(winning_bid, team_caps[team1])  # Cannot bid more than cap

    return team1, round(winning_bid, 2)




# GAME
draft_picks = {}
contract_amounts = {}

# While there are still players and teams to pick
remaining_free_agents = need_matrix.index.tolist()
remaining_teams = need_matrix.columns.tolist()

while remaining_free_agents and remaining_teams:
    for team in remaining_teams[:]:  # Use a copy so we can modify the list inside the loop
        if team not in need_matrix.columns:
            continue  # Skip if team already drafted
        
        # Get the team's highest need free agent still available
        team_needs = need_matrix[team].loc[remaining_free_agents]
        
        if team_needs.empty:
            continue  # No players left for this team to pick
        
        # Choose the top priority player
        top_pick = team_needs.idxmax()
        
        # Run auction
        winner, final_bid = run_auction_for_player(top_pick, need_matrix, team_caps)

        # Update results
        draft_picks[winner] = top_pick
        team_caps[winner] -= final_bid  # Deduct bid from cap
        print(f"{winner} wins the auction for {top_pick} with a bid of ${final_bid}M")
        contract_amounts[winner] = final_bid

        # Remove drafted player
        remaining_free_agents.remove(top_pick)
        need_matrix = need_matrix.drop(index=top_pick)
        need_matrix = need_matrix.drop(columns=winner)
        
        # print(f"Remaining free agents: {remaining_free_agents}")
        # print(f"Remaining teams: {remaining_teams}")
        # print(f"Winner: {winner}")
        remaining_teams.remove(winner)

# Show final draft picks
print("\nFinal Free Agent Signings:")
for team, player in draft_picks.items():
    print(f"{team}: {player} for ${contract_amounts[team]}M")
