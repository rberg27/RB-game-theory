#!/usr/bin/env python3
"""
Working script to download Madden NFL team ratings from maddenratings.weebly.com
This version correctly handles the direct Excel file links
"""

import requests
from bs4 import BeautifulSoup
import os
import time
import re

# Create a directory to store the downloaded files
os.makedirs("madden_ratings", exist_ok=True)

# User-Agent to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Years to download (from 2015 to 2024)
years = range(15, 25)

def clean_filename(text):
    """Clean text to make it suitable for filenames"""
    if not text:
        return "unknown"
    cleaned = re.sub(r'[^\w\s\-\.]', '', text)
    cleaned = re.sub(r'\s+', '_', cleaned)
    cleaned = cleaned.strip('_')
    return cleaned if cleaned else 'unknown'

def extract_team_name_from_url(url):
    """Extract team name from URL"""
    # Remove file extension and path
    filename = url.split('/')[-1].replace('.xlsx', '').replace('.xls', '')
    
    # Remove common prefixes and suffixes
    team_name = filename.replace('_madden_nfl_15', '')
    team_name = team_name.replace('roster_update_', 'update_')
    team_name = team_name.replace('team_', '')
    
    # Handle special cases
    if 'st._louis_rams' in filename:
        team_name = 'st_louis_rams'
    elif 'team_carter_pro_bowl' in filename:
        team_name = 'pro_bowl_carter'
    elif 'team_irvin_pro_bowl' in filename:
        team_name = 'pro_bowl_irvin'
    
    return team_name

def download_ratings(year):
    """Download Madden NFL ratings for a specific year"""
    url = f"https://maddenratings.weebly.com/madden-nfl-{year}.html"
    print(f"\nDownloading Madden NFL {year}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        download_count = 0
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # Check if this is an Excel file
            if any(ext in href.lower() for ext in ['.xlsx', '.xls']):
                # Get team/file name from URL
                team_name = extract_team_name_from_url(href)
                
                # Create filename
                filename = f"madden_ratings/madden_{year}_{team_name}.xlsx"
                
                # Construct absolute URL
                if not href.startswith('http'):
                    if href.startswith('/'):
                        absolute_url = f"https://maddenratings.weebly.com{href}"
                    else:
                        absolute_url = f"https://maddenratings.weebly.com/{href}"
                else:
                    absolute_url = href
                
                # Download the file
                try:
                    print(f"  Downloading: {team_name}")
                    
                    file_response = requests.get(absolute_url, headers=headers, timeout=30)
                    file_response.raise_for_status()
                    
                    with open(filename, 'wb') as f:
                        f.write(file_response.content)
                    
                    print(f"  ✓ Saved: {filename}")
                    download_count += 1
                    time.sleep(0.5)  # Be nice to the server
                    
                except Exception as e:
                    print(f"  ✗ Failed: {str(e)}")
        
        if download_count == 0:
            print(f"  ⚠️ No files downloaded for Madden NFL {year}")
        else:
            print(f"  ✅ Downloaded {download_count} files for Madden NFL {year}")
        
    except Exception as e:
        print(f"  ❌ Error accessing Madden NFL {year}: {str(e)}")

def main():
    print("Madden NFL Ratings Downloader")
    print("============================")
    
    for year in years:
        download_ratings(year)
        time.sleep(2)  # Pause between years
    
    print("\n" + "="*50)
    print("Download complete!")
    print("="*50)
    
    print("\nDownloaded files:")
    
    # Get all files
    files = []
    for file in os.listdir("madden_ratings"):
        if file.endswith(('.xlsx', '.xls')):
            files.append(file)
    
    # Sort files by year and team
    files.sort()
    
    # Group by year for display
    files_by_year = {}
    for file in files:
        year_match = re.search(r'madden_(\d+)', file)
        if year_match:
            year = year_match.group(1)
            if year not in files_by_year:
                files_by_year[year] = []
            files_by_year[year].append(file)
    
    for year in sorted(files_by_year.keys()):
        print(f"\nMadden NFL {year} ({len(files_by_year[year])} files):")
        for file in files_by_year[year]:
            print(f"  - {file}")
    
    # Summary
    print(f"\nTotal files downloaded: {len(files)}")

if __name__ == "__main__":
    main()