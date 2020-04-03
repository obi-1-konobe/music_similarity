import pylast
import pickle
from tqdm import tqdm

import utils

API_KEY = "80113e47bfd1c58983acc18b4d46e025"  # this is a sample key
API_SECRET = "604648c3611f684b077c83df8e3a00fd"
username = "obi-1-konobe"
password_hash = pylast.md5("T4s4rt!rlastfm")

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash)

tracks_df = utils.load('../data/pickles/fma_metadata/tracks.csv')
small = tracks_df[tracks_df['set', 'subset'] <= 'small']
artist_name = small['artist', 'name']
track_title = small['track', 'title']
tracks_zip = zip(artist_name.values, track_title.values, small.index.values)

result_dict = dict()
errors = list()
i = 0
for track in tqdm(tracks_zip):
    zip_artist, zip_title, zip_id = track

    try:
        artist = network.get_artist(zip_artist)
        track = network.get_track(artist, zip_title)

        artist_tags = artist.get_top_tags(10)
        track_tags = track.get_top_tags(10)
        similar_track = track.get_similar()
    except:
        errors.append(zip_id)
    else:
        temp_dict = dict()
        temp_dict['artist_name'] = zip_artist
        temp_dict['track_title'] = zip_title
        temp_dict['artist_tags'] = [(elem.item.name, elem.weight) for elem in artist_tags]
        temp_dict['track_tags'] = [(elem.item.name, elem.weight) for elem in track_tags]
        temp_dict['similar_tracks'] = [(elem.item.artist.name, elem.item.title, elem.match) for elem in similar_track]

        result_dict[zip_id] = temp_dict
    if i % 500 == 0:
        result_dict['errors'] = errors
        with open(f'{i}.pickle', 'wb') as f:
            pickle.dump(result_dict, f)

        result_dict = dict()
        errors = list()

    i += 1

result_dict['errors'] = errors
with open('../data/pickles/last.pickle', 'wb') as handle:
    pickle.dump(result_dict, handle)










