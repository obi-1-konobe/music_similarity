import pylast
import pickle
from tqdm import tqdm

import utils


class Last_fm_api:

    API_KEY = "80113e47bfd1c58983acc18b4d46e025"
    API_SECRET = "604648c3611f684b077c83df8e3a00fd"
    username = "obi-1-konobe"
    password_hash = pylast.md5("T4s4rt!rlastfm")

    def __init__(self):
        self.API_KEY = "80113e47bfd1c58983acc18b4d46e025"
        self.API_SECRET = "604648c3611f684b077c83df8e3a00fd"
        self.username = "obi-1-konobe"
        self.password_hash = pylast.md5("T4s4rt!rlastfm")
        self.network = pylast.LastFMNetwork(
            api_key=self.API_KEY,
            api_secret=self.API_SECRET,
            username=self.username,
            password_hash=self.password_hash
        )

    # tracks_df = utils.load('../data/fma_metadata/tracks.csv')
    # small = tracks_df[tracks_df['set', 'subset'] <= 'small']
    # artist_name = small['artist', 'name']
    # track_title = small['track', 'title']
    # tracks_zip = zip(artist_name.values, track_title.values, small.index.values)

    def get_response_lastfm(self, tracks_zip):
        result_dict = dict()
        errors = list()
        for track in tqdm(tracks_zip):
            zip_artist, zip_title, zip_id = track

            try:
                artist = self.network.get_artist(zip_artist)
                track = self.network.get_track(artist, zip_title)

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

        result_dict['errors'] = errors
        return result_dict

    def run(self):

        tracks_df = utils.load('../data/fma_metadata/tracks.csv')
        small = tracks_df[tracks_df['set', 'subset'] <= 'small']
        artist_name = small['artist', 'name']
        track_title = small['track', 'title']
        tracks_zip = zip(artist_name.values, track_title.values, small.index.values)

        main_dict = self.get_response_lastfm(tracks_zip)

        # if i % 500 == 0:
        #     result_dict['errors'] = errors
        #     with open(f'../data/pickles/{i}.pickle', 'wb') as f:
        #         pickle.dump(result_dict, f)
        #
        #     result_dict = dict()
        #     errors = list()
        #
        # i += 1

    # result_dict['errors'] = errors
        with open('../data/pickles/main_dict.pickle', 'wb') as handle:
            pickle.dump(main_dict, handle)










