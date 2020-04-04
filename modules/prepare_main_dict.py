import pickle
import os
import utils
from lastfm_api import Last_fm_api

main_dict = dict()
list_dir = os.listdir('../data/pickles/')

for dump in list_dir:
    with open(f'../data/pickles/{dump}', 'rb') as f:
        data = pickle.load(f)
    main_dict.update(data)

tracks = utils.load('../data/fma_metadata/tracks.csv')
small = tracks[tracks['set', 'subset'] <= 'small']
artist_name = small['artist', 'name']
arist_id = small['artist', 'id']
track_title = small['track', 'title']
track_duration = small['track', 'duration']
track_genre = small['track', 'genre_top']

my_zip = zip(artist_name.values, track_title.values, small.index.values)
zip_list = list(my_zip)

errors = list()
for dump in list_dir:
    with open(f'../data/pickles/{dump}', 'rb') as f:
        data = pickle.load(f)
        errors += data['errors']

errors_zip = filter(lambda x: x[2] in errors, zip_list)
errors_list = list(errors_zip)

last_fm = Last_fm_api()
errors_dict = last_fm.get_response_lastfm(errors_list)

with open('../data/pickles/errors_dict.pickle', 'wb') as f:
    pickle.dump(errors_dict, f)

