import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import os
import pickle

class NeuralNetworkRegressor(nn.Module):
    def __init__(self, input_size):
        super(NeuralNetworkRegressor, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.dropout1 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(128, 64)
        self.dropout2 = nn.Dropout(0.2)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 16)
        self.fc5 = nn.Linear(16, 1)
        self.leaky_relu = nn.LeakyReLU(0.1)

    def forward(self, x):
        x = self.leaky_relu(self.fc1(x))
        x = self.dropout1(x)
        x = self.leaky_relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.leaky_relu(self.fc3(x))
        x = self.leaky_relu(self.fc4(x))
        x = self.fc5(x)
        return x

class TeamModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def preprocess_data(self, data):
        """
        Preprocess the Madden team data by removing non-predictive columns
        and scaling the features.
        """
        # Remove columns that should not be used for prediction
        columns_to_drop = ['team_name', 'year', 'regular_season_wins', 
                          'playoff_wins', 'total_wins']
        
        # Create X (features) and y (target)
        X = data.drop(columns_to_drop, axis=1, errors='ignore')
        y = data['total_wins'] if 'total_wins' in data.columns else None
        
        return X, y
    
    def save_model(self, model_dir=None):
        """
        Save the trained model and scaler to disk.
        
        Args:
            model_dir (str, optional): Directory to save the model. If None, uses default location.
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
            
        if model_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, "saved_models")
            
        os.makedirs(model_dir, exist_ok=True)
        
        # Save the PyTorch model
        model_path = os.path.join(model_dir, "team_model.pt")
        torch.save(self.model.state_dict(), model_path)
        
        # Save the scaler
        scaler_path = os.path.join(model_dir, "team_scaler.pkl")
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
            
        print(f"Model saved to {model_dir}")
        
    def load_model(self, model_dir=None, input_size=None):
        """
        Load a trained model and scaler from disk.
        
        Args:
            model_dir (str, optional): Directory where the model is saved. If None, uses default location.
            input_size (int, optional): Input size for the model if creating a new one. Required if model file doesn't exist.
            
        Returns:
            bool: True if model was loaded successfully, False otherwise
        """
        if model_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, "saved_models")
            
        model_path = os.path.join(model_dir, "team_model.pt")
        scaler_path = os.path.join(model_dir, "team_scaler.pkl")
        
        # Check if model files exist
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            print("No saved model found.")
            return False
            
        try:
            # Load the scaler
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
                
            # Create model instance if needed
            if self.model is None:
                if input_size is None:
                    raise ValueError("input_size must be provided when loading a model for the first time")
                self.model = NeuralNetworkRegressor(input_size).to(self.device)
                
            # Load the model weights
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()  # Set to evaluation mode
            
            print(f"Model loaded from {model_dir}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def train(self, data=None, force_train=False):
        """
        Train the model on Madden team data to predict total wins.
        If a saved model exists, it will be loaded unless force_train is True.
        
        Args:
            data (DataFrame, optional): DataFrame containing team stats and win data.
                                       If None, loads the default madden_data_processed.xlsx file.
            force_train (bool): If True, train a new model even if saved weights exist.
                               If False, load saved weights if they exist.
        """
        # If no data is provided, load the default dataset
        if data is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            data_path = os.path.join(project_root, "rb-game-theory", "data", "madden_data_processed.xlsx")
            print(f"Loading default data from: {data_path}")
            data = load_madden_data(data_path)
        
        # Preprocess data to get input size
        X, y = self.preprocess_data(data)
        input_size = X.shape[1]
        
        # Try to load the model if not forcing training
        if not force_train and self.load_model(input_size=input_size):
            return None, None  # Model loaded successfully, no metrics to return
        
        # If we get here, either force_train is True or no saved model exists
        print("Training new model...")
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert to PyTorch tensors
        X_train_tensor = torch.FloatTensor(X_train_scaled).to(self.device)
        y_train_tensor = torch.FloatTensor(y_train.values).reshape(-1, 1).to(self.device)
        X_test_tensor = torch.FloatTensor(X_test_scaled).to(self.device)
        y_test_tensor = torch.FloatTensor(y_test.values).reshape(-1, 1).to(self.device)
        
        # Create DataLoader
        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
        
        # Initialize the model
        input_size = X_train_scaled.shape[1]
        self.model = NeuralNetworkRegressor(input_size).to(self.device)
        
        # Define loss function and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
        # Training loop
        epochs = 500
        for epoch in range(epochs):
            self.model.train()
            running_loss = 0.0
            
            for inputs, targets in train_loader:
                # Zero the parameter gradients
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(inputs)
                loss = criterion(outputs, targets)
                
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item()
            
            # Print statistics every 10 epochs
            if (epoch + 1) % 10 == 0:
                print(f'Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}')
        
        # Evaluate the model
        self.model.eval()
        with torch.no_grad():
            y_pred_tensor = self.model(X_test_tensor)
            y_pred = y_pred_tensor.cpu().numpy().flatten()
            y_test_np = y_test.values
            
            mse = mean_squared_error(y_test_np, y_pred)
            r2 = r2_score(y_test_np, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        # Save the trained model
        self.save_model()
        
        return mse, r2
    
    def predict(self, team_data):
        """
        Predict the total wins for a team based on their Madden ratings.
        
        Args:
            team_data (DataFrame): DataFrame containing team stats without win data
            
        Returns:
            float: Predicted total wins for the team
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet. Call train() first.")
        
        # Preprocess the input data
        X, _ = self.preprocess_data(team_data)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Convert to PyTorch tensor
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)
        
        # Make prediction
        self.model.eval()
        with torch.no_grad():
            predicted_wins_tensor = self.model(X_tensor)
            predicted_wins = predicted_wins_tensor.cpu().numpy().flatten()
        
        return predicted_wins

def load_madden_data(file_path):
    """
    Load Madden team data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file containing Madden team data
        
    Returns:
        DataFrame: DataFrame containing the Madden team data
    """
    return pd.read_excel(file_path)

def main():
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    data_path = os.path.join(project_root, "rb-game-theory","data", "madden_data_processed.xlsx")
    
    try:
        # Load data
        print(f"Loading data from: {data_path}")
        team_data = load_madden_data(data_path)
        
        # Initialize and train model
        model = TeamModel()
        model.train(force_train=False)  # Will load saved model if it exists
        
        # Example prediction for a new team
        new_team = team_data.iloc[0:1].copy()  # Just for demonstration
        new_team = new_team.drop(['total_wins', 'regular_season_wins', 'playoff_wins'], axis=1, errors='ignore')
        
        predicted_wins = model.predict(new_team)
        team_name = new_team.iloc[0]['team'] if 'team' in new_team.columns else "Unknown Team"
        print(f"\nPredicted wins for {team_name}: {predicted_wins[0]:.1f}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def calculate_team_needs(free_agents, teams):
    """
    Calculate the need matrix for each free agent and team combination.
    
    Args:
        free_agents (DataFrame): DataFrame containing free agent data
        teams (DataFrame): DataFrame containing team data
        
    Returns:
        DataFrame: A matrix where rows are free agents, columns are teams,
                  and values represent the projected win improvement
    """
    if free_agents.empty or teams.empty:
        print("Error: Free agents or teams data is empty")
        return pd.DataFrame()
    
    # Initialize team model
    model = TeamModel()
    model_loaded = model.load_model(input_size=len(teams.columns) - 5)  # Adjust for non-feature columns
    
    if not model_loaded:
        print("Warning: Could not load team model. Training new model...")
        model.train(data=teams, force_train=True)
    
    # Get unique team names
    team_names = teams['team_name'].unique()
    
    # Create empty DataFrame to store results
    results = []
    
    # For each free agent
    for _, player in free_agents.iterrows():
        player_name = player['Player Name'] 
        player_rating = player['Madden OVR'] 
        player_position = "HB"

        print(f"Evaluating free agent: {player_name}")
        
        # For each team
        for team_name in team_names:
            team_data = teams[teams['team_name'] == team_name].copy()
            
            if team_data.empty:
                continue
                
            need_result = calculate_team_need(player_rating, player_name, team_name, player_position, team_data, model)
                    
            results.append(need_result)
                
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Create pivot table for the need matrix
    if not results_df.empty:
        need_matrix = results_df.pivot_table(
            index='player_name',
            columns='team_name',
            values='win_improvement'
        )

        # Shift all values in the need_matrix so that the minimum value starts at 0
        min_value = need_matrix.values.min()
        need_matrix = need_matrix - min_value
        
        # Print information about the transformation
        print(f"Shifted all win improvement values by {min_value:.2f} to start at 0")
        return need_matrix
    else:
        return pd.DataFrame()

def calculate_team_need(player_rating, player_name, team_name, player_position, team, team_model):
    """
    Calculate how much a team needs a specific free agent based on win prediction difference.
    
    Args:
        player_rating (float): Overall rating of the free agent player
        player_position (str): Position of the free agent player (e.g., 'HB')
        team (DataFrame): DataFrame containing the team data
        team_model (TeamModel): Trained team model for win prediction
        
    Returns:
        dict: Dictionary containing player rating, current win prediction, 
              win prediction with player, and win improvement
    """
    if player_rating is None:
        return None
    
    # Make a copy of team data to avoid modifying the original
    team_data = team.copy()
    
    if team_data.empty:
        print(f"Team data is empty.")
        return None
    
    # Get current win prediction
    current_win_prediction = team_model.predict(team_data)[0]
    
    # Simulate adding player to team based on position
    team_with_player = team_data.copy()
    
    # Handle different positions
    position_column = player_position + '1'
    
    # Update the team with the player if position column exists
    if position_column and position_column in team_with_player.columns:
        # Find all columns for this position (e.g., HB1, HB2, HB3)
        position_base = player_position # Remove the number
        position_columns = [col for col in team_with_player.columns if col.startswith(position_base)]
        
        # Get current ratings for all positions
        position_ratings = [team_with_player[col].values[0] for col in position_columns]
        
        # Only proceed if the player is better than at least one current player
        if player_rating > min(position_ratings):
            # Add the player rating to the list and sort in descending order
            position_ratings.append(player_rating)
            position_ratings.sort(reverse=True)
            
            # Remove the lowest rating (we're replacing the worst player)
            position_ratings = position_ratings[:-1]
            
            # Update the team with the new ordered ratings
            for i, col in enumerate(position_columns):
                if i < len(position_ratings):
                    team_with_player[col] = position_ratings[i]
    
    # Get win prediction with new player
    win_prediction_with_player = team_model.predict(team_with_player)[0]
    
    # Calculate improvement
    win_improvement = win_prediction_with_player - current_win_prediction
    
    return {
        'player_name': player_name,
        'player_rating': player_rating,
        'team_name': team_name,
        'current_win_prediction': current_win_prediction,
        'win_prediction_with_player': win_prediction_with_player,
        'win_improvement': win_improvement
    }
if __name__ == "__main__":
    import free_agency
    import team_model
    
    # Load free agent data
    free_agents = free_agency.get_free_agents_by_year(2024)
    teams = free_agency.get_teams_by_year(2024)

    need_matrix = calculate_team_needs(free_agents, teams)
    print(need_matrix)
    
