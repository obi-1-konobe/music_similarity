import json
import os
import pandas as pd
from tqdm import tqdm


class Vector:
    def __init__(self):
        pass

    def run(self):
        audio_listdir = os.listdir('../data/fma_small/')
        col_name = self.get_col_name()
        i = 1
        vec_list = list()
        for some_dir in audio_listdir:
            list_dir = os.listdir(f'../data/fma_small/{some_dir}/')
            for track_name in list_dir:
                try:
                    json_list = self.find_json(track_name)
                except Exception:
                    with open('../data/essentia_errors.txt', 'a+') as f:
                        f.write(track_name + '\n')
                    continue

                vec = [track_name] + self.make_vector(json_list)
                vec_list.append(vec)

                if len(vec_list) % 1000 == 0:
                    df = pd.DataFrame(vec_list, columns=col_name)
                    df.to_csv(f'../data/csv/new_track_vectors_{i}.csv')
                    vec_list = list()
                    i += 1

        df = pd.DataFrame(vec_list, columns=col_name)
        df.to_csv(f'../data/csv/new_track_vectors_{i}.csv')

    @staticmethod
    def find_json(track_name):
        result = list()

        for i in range(1, 9):
            file = f'../data/essentia/{track_name[:-4]}_{i}.json'
            with open(file, 'r') as f:
                json_file = json.load(f)
            result.append(json_file)

        file = f'../data/essentia/{track_name[:-4]}.json'
        with open(file, 'r') as f:
            json_file = json.load(f)
        result.append(json_file)

        return result

    @staticmethod
    def make_vector(json_list):
        vec = list()
        for i in range(8):
            data = json_list[i]

            vec += data['lowlevel']['mfcc']['mean']
            vec += list(data['lowlevel']['spectral_centroid'].values())
            vec += list(data['lowlevel']['spectral_kurtosis'].values())
            vec += list(data['lowlevel']['spectral_skewness'].values())
            vec += list(data['lowlevel']['spectral_spread'].values())
            vec += list(data['lowlevel']['spectral_rolloff'].values())
            vec += list(data['lowlevel']['spectral_flux'].values())
            vec += list(data['lowlevel']['spectral_complexity'].values())
            vec += list(data['lowlevel']['spectral_entropy'].values())
            vec += list(data['lowlevel']['zerocrossingrate'].values())
            vec += list(data['lowlevel']['melbands_crest'].values())
            vec += list(data['lowlevel']['melbands_flatness_db'].values())
            vec += list(data['lowlevel']['pitch_salience'].values())
            vec += list(data['tonal']['chords_strength'].values())
            vec += list(data['tonal']['hpcp_crest'].values())

        data = json_list[8]

        vec.append(data['lowlevel']['average_loudness'])
        vec.append(data['lowlevel']['dynamic_complexity'])
        vec.append(data['rhythm']['beats_count'])
        vec.append(data['rhythm']['bpm'])
        vec.append(data['rhythm']['onset_rate'])
        vec.append(data['rhythm']['danceability'])
        vec.append(data['tonal']['chords_changes_rate'])
        vec.append(data['tonal']['chords_number_rate'])

        vec += data['lowlevel']['mfcc']['mean']
        vec += list(data['lowlevel']['spectral_centroid'].values())
        vec += list(data['lowlevel']['spectral_kurtosis'].values())
        vec += list(data['lowlevel']['spectral_skewness'].values())
        vec += list(data['lowlevel']['spectral_spread'].values())
        vec += list(data['lowlevel']['spectral_rolloff'].values())
        vec += list(data['lowlevel']['spectral_flux'].values())
        vec += list(data['lowlevel']['spectral_complexity'].values())
        vec += list(data['lowlevel']['spectral_entropy'].values())
        vec += list(data['lowlevel']['zerocrossingrate'].values())
        vec += list(data['lowlevel']['melbands_crest'].values())
        vec += list(data['lowlevel']['melbands_flatness_db'].values())
        vec += list(data['lowlevel']['pitch_salience'].values())
        vec += list(data['tonal']['chords_strength'].values())
        vec += list(data['tonal']['hpcp_crest'].values())

        return vec

    @staticmethod
    def get_col_name():
        col_name = list()
        col_name.append('file')
        for i in range(1, 9):
            for j in range(1, 14):
                col_name.append(f'mfcc{j}_mean')
            col_name += ['centroid.max', 'centroid.mean', 'centroid.min', 'centroid.std']
            col_name += ['kurtosis.max', 'kurtosis.mean', 'kurtosis.min', 'kurtosis.std']
            col_name += ['skewness.max', 'skewness.mean', 'skewness.min', 'skewness.std']
            col_name += ['spread.max', 'spread.mean', 'spread.min', 'spread.std']
            col_name += ['rolloff.max', 'rolloff.mean', 'rolloff.min', 'rolloff.std']
            col_name += ['flux.max', 'flux.mean', 'flux.min', 'flux.std']
            col_name += ['complexity.max', 'complexity.mean', 'complexity.min', 'complexity.std']
            col_name += ['entropy.max', 'entropy.mean', 'entropy.min', 'entropy.std']
            col_name += ['zcr_max', 'zcr_mean', 'zcr_min', 'zcr_std']
            col_name += ['crest.max', 'crest.mean', 'crest.min', 'crest.std']
            col_name += ['flatness.max', 'flatness.mean', 'flatness.min', 'flatness.std']
            col_name += ['pitch_salience.max', 'pitch_salience.mean', 'pitch_salience.min', 'pitch_salience.std']
            col_name += ['chords.max', 'chords.mean', 'chords.min', 'chords.std']
            col_name += ['hpcp.max', 'hpcp.mean', 'hpcp.min', 'hpcp.std']
        col_name.append('average_loudness')
        col_name.append('dynamic_complexity')
        col_name.append('beats_count')
        col_name.append('bpm')
        col_name.append('onset_rate')
        col_name.append('danceability')
        col_name.append('chords_changes')
        col_name.append('chords_number')
        for j in range(1, 14):
            col_name.append(f'mfcc{j}_mean')
        col_name += ['centroid.max', 'centroid.mean', 'centroid.min', 'centroid.std']
        col_name += ['kurtosis.max', 'kurtosis.mean', 'kurtosis.min', 'kurtosis.std']
        col_name += ['skewness.max', 'skewness.mean', 'skewness.min', 'skewness.std']
        col_name += ['spread.max', 'spread.mean', 'spread.min', 'spread.std']
        col_name += ['rolloff.max', 'rolloff.mean', 'rolloff.min', 'rolloff.std']
        col_name += ['flux.max', 'flux.mean', 'flux.min', 'flux.std']
        col_name += ['complexity.max', 'complexity.mean', 'complexity.min', 'complexity.std']
        col_name += ['entropy.max', 'entropy.mean', 'entropy.min', 'entropy.std']
        col_name += ['zcr_max', 'zcr_mean', 'zcr_min', 'zcr_std']
        col_name += ['crest.max', 'crest.mean', 'crest.min', 'crest.std']
        col_name += ['flatness.max', 'flatness.mean', 'flatness.min', 'flatness.std']
        col_name += ['pitch_salience.max', 'pitch_salience.mean', 'pitch_salience.min', 'pitch_salience.std']
        col_name += ['chords.max', 'chords.mean', 'chords.min', 'chords.std']
        col_name += ['hpcp.max', 'hpcp.mean', 'hpcp.min', 'hpcp.std']

        return col_name

    @staticmethod
    def get_col_name_bow():
        col_name = list()
        col_name.append('file')
        for j in range(1, 14):
            col_name.append(f'mfcc{j}_mean')
        col_name += ['centroid.max', 'centroid.mean', 'centroid.min', 'centroid.std']
        col_name += ['kurtosis.max', 'kurtosis.mean', 'kurtosis.min', 'kurtosis.std']
        col_name += ['skewness.max', 'skewness.mean', 'skewness.min', 'skewness.std']
        col_name += ['spread.max', 'spread.mean', 'spread.min', 'spread.std']
        col_name += ['rolloff.max', 'rolloff.mean', 'rolloff.min', 'rolloff.std']
        col_name += ['flux.max', 'flux.mean', 'flux.min', 'flux.std']
        col_name += ['complexity.max', 'complexity.mean', 'complexity.min', 'complexity.std']
        col_name += ['entropy.max', 'entropy.mean', 'entropy.min', 'entropy.std']
        col_name += ['zcr_max', 'zcr_mean', 'zcr_min', 'zcr_std']
        col_name += ['crest.max', 'crest.mean', 'crest.min', 'crest.std']
        col_name += ['flatness.max', 'flatness.mean', 'flatness.min', 'flatness.std']
        col_name += ['pitch_salience.max', 'pitch_salience.mean', 'pitch_salience.min', 'pitch_salience.std']
        col_name += ['chords.max', 'chords.mean', 'chords.min', 'chords.std']
        col_name += ['hpcp.max', 'hpcp.mean', 'hpcp.min', 'hpcp.std']
        col_name.append('average_loudness')
        col_name.append('dynamic_complexity')
        col_name.append('beats_count')
        col_name.append('bpm')
        col_name.append('onset_rate')
        col_name.append('danceability')
        col_name.append('chords_changes')
        col_name.append('chords_number')

        return col_name

    def vec_for_bow(self):
        json_dir = '../data/essentia/'
        list_dir = os.listdir(json_dir)
        all_data = list()
        for file in tqdm(list_dir):
            if '_' not in file:
                continue
            name = file[:-5]
            with open(f'{json_dir}{file}', 'r') as f:
                data = json.load(f)

            vec = [name]
            vec += data['lowlevel']['mfcc']['mean']
            vec += list(data['lowlevel']['spectral_centroid'].values())
            vec += list(data['lowlevel']['spectral_kurtosis'].values())
            vec += list(data['lowlevel']['spectral_skewness'].values())
            vec += list(data['lowlevel']['spectral_spread'].values())
            vec += list(data['lowlevel']['spectral_rolloff'].values())
            vec += list(data['lowlevel']['spectral_flux'].values())
            vec += list(data['lowlevel']['spectral_complexity'].values())
            vec += list(data['lowlevel']['spectral_entropy'].values())
            vec += list(data['lowlevel']['zerocrossingrate'].values())
            vec += list(data['lowlevel']['melbands_crest'].values())
            vec += list(data['lowlevel']['melbands_flatness_db'].values())
            vec += list(data['lowlevel']['pitch_salience'].values())
            vec += list(data['tonal']['chords_strength'].values())
            vec += list(data['tonal']['hpcp_crest'].values())

            vec.append(data['lowlevel']['average_loudness'])
            vec.append(data['lowlevel']['dynamic_complexity'])
            vec.append(data['rhythm']['beats_count'])
            vec.append(data['rhythm']['bpm'])
            vec.append(data['rhythm']['onset_rate'])
            vec.append(data['rhythm']['danceability'])
            vec.append(data['tonal']['chords_changes_rate'])
            vec.append(data['tonal']['chords_number_rate'])

            all_data.append(vec)

        col_name = self.get_col_name_bow()
        df = pd.DataFrame(all_data, columns=col_name)
        df.to_csv(f'../data/csv/track_vectors_bow.csv')



