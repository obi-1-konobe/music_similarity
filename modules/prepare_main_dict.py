import pickle
# import os
import utils
# from lastfm_api import Last_fm_api

with open('../data/pickles/main_dict.pickle', 'rb') as f:
    main_dict = pickle.load(f)

tracks = utils.load('../data/fma_metadata/tracks.csv')
small = tracks[tracks['set', 'subset'] <= 'small']
artist_name = small['artist', 'name']
track_title = small['track', 'title']
track_genre = small['track', 'genre_top']
track_all_genres = small['track', 'genres_all']
fma_tags = small['track', 'tags']

my_zip = zip(
    small.index.values,
    artist_name.values,
    track_title.values,
    track_genre.values,
    track_all_genres.values,
    fma_tags.values,
)
zip_list = list(my_zip)

for idx, artist, track, genre, all_genres, tags in zip_list:
    if idx in main_dict:
        main_dict[idx]['genre'] = genre
        main_dict[idx]['all_genres'] = all_genres
        main_dict[idx]['fma_tags'] = tags
    else:
        main_dict[idx] = {
            'artist_name': artist,
            'track_title': track,
            'artist_tags': [],
            'track_tags': [],
            'similar_tracks': [],
            'similar_list': [],
            'genre': genre,
            'all_genres': all_genres,
            'fma_tags': tags
        }

with open('../data/pickles/new_main_dict.pickle','wb') as f:
    pickle.dump(main_dict, f)

