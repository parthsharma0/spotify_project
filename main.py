import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# Set up your Spotify API credentials
client_id = 'abb2d8c758694ce69102cff591143534'
client_secret = 'c45c0b7bc4c740b889ba024873f8cb94'
redirect_uri = 'http://localhost:8888/callback'

# Authenticate with Spotify
scope = "user-top-read user-library-read playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Function to get top tracks with time range
def get_top_tracks(limit=50, time_range='long_term'):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    top_tracks = []
    if results['items']:
        for idx, track in enumerate(results['items']):
            track_info = {
                'Type': 'Top Track',
                'Index': idx + 1,
                'Name': track['name'],
                'Artists': ', '.join([artist['name'] for artist in track['artists']]),
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date'],
            }
            top_tracks.append(track_info)
    return top_tracks

# Function to get top artists with time range
def get_top_artists(limit=50, time_range='long_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    top_artists = []
    if results['items']:
        for idx, artist in enumerate(results['items']):
            artist_info = {
                'Type': 'Top Artist',
                'Index': idx + 1,
                'Name': artist['name'],
                'Artists': '',
                'Album': '',
                'Release Date': '',
                'Genres': ', '.join(artist['genres']),
                'Followers': artist['followers']['total'],
                'Popularity': artist['popularity'],
            }
            top_artists.append(artist_info)
    return top_artists

# Function to get saved tracks
def get_saved_tracks(limit=50):
    results = sp.current_user_saved_tracks(limit=limit)
    saved_tracks = []
    if results['items']:
        for idx, item in enumerate(results['items']):
            track = item['track']
            track_info = {
                'Type': 'Saved Track',
                'Index': idx + 1,
                'Name': track['name'],
                'Artists': ', '.join([artist['name'] for artist in track['artists']]),
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date'],
            }
            saved_tracks.append(track_info)
    return saved_tracks

# Function to get playlists
def get_playlists(limit=10):
    results = sp.current_user_playlists(limit=limit)
    playlists = []
    if results['items']:
        for idx, playlist in enumerate(results['items']):
            playlist_info = {
                'Type': 'Playlist',
                'Index': idx + 1,
                'Name': playlist['name'],
                'Total Tracks': playlist['tracks']['total'],
                'Owner': playlist['owner']['display_name']
            }
            playlists.append(playlist_info)
    return playlists

# Function to save data to a specific CSV file
def save_to_csv(data, filename):
    if data:
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")
    else:
        print(f"No data to save in {filename}.")

# Main function to gather and save each dataset in a separate CSV
def main():
    # Collect and save each dataset in separate CSV files
    top_tracks = get_top_tracks(time_range='short_term')
    save_to_csv(top_tracks, "top_tracks.csv")
    
    top_artists = get_top_artists(time_range='short_term')
    save_to_csv(top_artists, "top_artists.csv")
    
    saved_tracks = get_saved_tracks(limit=10)
    save_to_csv(saved_tracks, "saved_tracks.csv")
    
    playlists = get_playlists(limit=10)
    save_to_csv(playlists, "playlists.csv")

if __name__ == "__main__":
    main()
