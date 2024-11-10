import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# Spotify API credentials
client_id = 'abb2d8c758694ce69102cff591143534'
client_secret = 'c45c0b7bc4c740b889ba024873f8cb94'
redirect_uri = 'http://localhost:8888/callback'  # Replace with your redirect URI

# Initialize Spotipy with OAuth
scope = 'user-library-read'  # Required scope to read your saved tracks
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope))

def get_liked_songs(limit=10):
    results = sp.current_user_saved_tracks(limit=limit)
    liked_songs = []

    if results['items']:
        for item in results['items']:
            track = item['track']
            liked_songs.append({
                'track_name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']])
            })
    else:
        print("No liked songs found.")

    return liked_songs

def save_to_csv(songs, filename='liked_songs.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['track_name', 'artist'])
        writer.writeheader()
        writer.writerows(songs)
    print(f"Liked songs saved to {filename}.")

# Main function to run the script
def main():
    liked_songs = get_liked_songs()  # Retrieve liked songs
    if liked_songs:
        save_to_csv(liked_songs)  # Save to CSV

if __name__ == "__main__":
    main()
