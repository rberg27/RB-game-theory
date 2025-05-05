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