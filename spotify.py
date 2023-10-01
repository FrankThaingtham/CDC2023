import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

# Initialize Spotipy with credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create a list to store song data
song_data = []

# Define a function to fetch songs released between 2000 and 2010
def fetch_songs():
    for year in range(2000, 2011):
        # Search for tracks released in a specific year
        results = sp.search(q=f'year:{year}', type='track', limit=50)
        for track in results['tracks']['items']:
            # Get audio features for the track
            audio_features = sp.audio_features(track['id'])[0]
            
            # Get artist information to extract genres
            artist_info = sp.artist(track['artists'][0]['id'])
            genres = artist_info['genres']
            
            song_info = {
                'Title': track['name'],
                'Artist': ', '.join([artist['name'] for artist in track['artists']]),
                'Release Year': year,
                'Danceability': audio_features['danceability'],
                'Liveness': audio_features['liveness'],
                'Tempo': audio_features['tempo'],
                'Genres': ', '.join(genres),
                'Popularity': track['popularity'],
            }
            song_data.append(song_info)

# Call the function to fetch songs
fetch_songs()

# Create a DataFrame from the song data
df = pd.DataFrame(song_data)

# Export data to Excel
df.to_excel('songs_between_2000_and_2010_with_audio_and_genre_features.xlsx', index=False)
