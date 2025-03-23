import requests
import json
from datetime import datetime

class GiantsRosterFetcher:
    def __init__(self):
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/19"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_roster(self):
        try:
            # Make request to ESPN API
            response = requests.get(f"{self.base_url}/roster", headers=self.headers)
            response.raise_for_status()
            
            # Parse the JSON response
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse API response: {e}")
            
            # Check if we got valid data
            if not isinstance(data, dict):
                raise Exception("Invalid API response format")
            
            # Extract and format roster information
            roster = []
            print("test")
            print()
            print()
            print()
            print(data.get('athletes',[]))
            for athlete in data.get('athletes', []):
                try:
                    player = {
                        'name': f"{athlete.get('displayName', '')}",
                        'position': athlete.get('position', {}).get('abbreviation', ''),
                        'jersey': athlete.get('jersey', ''),
                        'age': athlete.get('age', ''),
                        'height': athlete.get('height', ''),
                        'weight': athlete.get('weight', ''),
                        'experience': athlete.get('experience', {}).get('years', 0),
                        'college': athlete.get('college', {}).get('name', '')
                    }
                    roster.append(player)
                except Exception as e:
                    print(f"Warning: Failed to process player data: {e}")
                    continue
            
            if not roster:
                raise Exception("No roster data found")
                
            return roster
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch roster data: {e}")
        except Exception as e:
            raise Exception(f"Error processing roster data: {e}")

    def save_roster_to_file(self, roster, filename=None):
        if filename is None:
            # Generate filename with current date
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"giants_roster_{date_str}.json"
        
        with open(filename, 'w') as f:
            json.dump(roster, f, indent=4)
        
        return filename

def main():
    # Create fetcher instance
    fetcher = GiantsRosterFetcher()
   
    try:
        # Fetch roster
        print("Fetching Giants roster...")
        roster = fetcher.fetch_roster()
        
        # Save to file
        filename = fetcher.save_roster_to_file(roster)
        print(f"\nRoster successfully saved to {filename}")
        
        # Print summary
        print(f"\nRoster Summary:")
        print(f"Total players: {len(roster)}")
        
        # Print positions breakdown
        positions = {}
        for player in roster:
            pos = player['position']
            positions[pos] = positions.get(pos, 0) + 1
        
        print("\nPlayers by position:")
        for pos, count in sorted(positions.items()):
            print(f"{pos}: {count}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching roster: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    
    
    
'''
{'id': '4361516', 'uid': 's:20~l:28~a:4361516', 'guid': '64087152-2041-1e48-7a62-35689f62505c', 'alternateIds': {'sdr': '4361516'}, 'firstName': 'Daniel', 'lastName': 'Bellinger', 'fullName': 'Daniel Bellinger', 'displayName': 'Daniel Bellinger', 'shortName': 'D. Bellinger', 'weight': 255.0, 'displayWeight': '255 lbs', 'height': 78.0, 'displayHeight': '6\' 6"', 'age': 24, 'dateOfBirth': '2000-09-22T07:00Z', 'links': [{'language': 'en-US', 'rel': ['playercard', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/_/id/4361516/daniel-bellinger', 'text': 'Player Card', 'shortText': 'Player Card', 'isExternal': False, 'isPremium': False}, {'language': 'en-US', 'rel': ['stats', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/stats/_/id/4361516/daniel-bellinger', 'text': 'Stats', 'shortText': 'Stats', 'isExternal': False, 'isPremium': False}, {'language': 'en-US', 'rel': ['splits', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/splits/_/id/4361516/daniel-bellinger', 'text': 'Splits', 'shortText': 'Splits', 'isExternal': False, 'isPremium': False}, {'language': 'en-US', 'rel': ['gamelog', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/gamelog/_/id/4361516/daniel-bellinger', 'text': 'Game Log', 'shortText': 'Game Log', 'isExternal': False, 'isPremium': False}, {'language': 'en-US', 'rel': ['news', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/news/_/id/4361516/daniel-bellinger', 'text': 'News', 'shortText': 'News', 'isExternal': False, 'isPremium': False}, {'language': 'en-US', 'rel': ['bio', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/bio/_/id/4361516/daniel-bellinger', 'text': 'Bio', 'shortText': 'Bio', 'isExternal': False, 'isPremium': False}, {'language': 'en-US', 'rel': ['overview', 'desktop', 'athlete'], 'href': 'https://www.espn.com/nfl/player/_/id/4361516/daniel-bellinger', 'text': 'Overview', 'shortText': 'Overview', 'isExternal': False, 'isPremium': False}], 'birthPlace': {'city': 'Las Vegas', 'state': 'NV', 'country': 'USA'}, 'college': {'id': '21', 'mascot': 'Aztecs', 'name': 'San Diego State', 'shortName': 'San Diego State', 'abbrev': 'SDSU', 'logos': [{'href': 'https://a.espncdn.com/i/teamlogos/ncaa/500/21.png', 'width': 500, 'height': 500, 'alt': '', 'rel': ['full', 'default'], 'lastUpdated': '2018-06-05T12:08Z'}, {'href': 'https://a.espncdn.com/i/teamlogos/ncaa/500-dark/21.png', 'width': 500, 'height': 500, 'alt': '', 'rel': ['full', 'dark'], 'lastUpdated': '2023-09-02T00:34Z'}]}, 'slug': 'daniel-bellinger', 'headshot': {'href': 'https://a.espncdn.com/i/headshots/nfl/players/full/4361516.png', 'alt': 'Daniel Bellinger'}, 'jersey': '82', 'position': {'id': '7', 'name': 'Tight End', 'displayName': 'Tight End', 'abbreviation': 'TE', 'leaf': True, 'parent': {'id': '70', 'name': 'Offense', 'displayName': 'Offense', 'abbreviation': 'OFF', 'leaf': False}}, 'injuries': [], 'teams': [{'$ref': 'http://sports.core.api.espn.pvt/v2/sports/football/leagues/nfl/seasons/2024/teams/19?lang=en&region=us'}], 'contracts': [], 'experience': {'years': 3}, 'status': {'id': '1', 'name': 'Active', 'type': 'active', 'abbreviation': 'Active'}}

'''