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
                    df.to_csv(f'../data/csv/track_vectors_{i}.csv')
                    vec_list = list()
                    i += 1

        df = pd.DataFrame(vec_list, columns=col_name)
        df.to_csv(f'../data/csv/track_vectors_{i}.csv')

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
            vec += list(data['lowlevel']['spectral_rolloff'].values())
            vec += list(data['lowlevel']['spectral_skewness'].values())
            vec += list(data['lowlevel']['spectral_flux'].values())
            vec += list(data['lowlevel']['zerocrossingrate'].values())

        data = json_list[8]

        vec.append(data['rhythm']['beats_count'])
        vec.append(data['rhythm']['bpm'])
        vec.append(data['rhythm']['onset_rate'])
        vec.append(data['rhythm']['danceability'])
        vec += data['lowlevel']['mfcc']['mean']
        vec += list(data['lowlevel']['spectral_centroid'].values())
        vec += list(data['lowlevel']['spectral_kurtosis'].values())
        vec += list(data['lowlevel']['spectral_rolloff'].values())
        vec += list(data['lowlevel']['spectral_skewness'].values())
        vec += list(data['lowlevel']['spectral_flux'].values())
        vec += list(data['lowlevel']['zerocrossingrate'].values())

        return vec

    @staticmethod
    def get_col_name():
        col_name = list()
        col_name.append('file')
        # for i in range(1, 9):
        for j in range(1, 14):
            col_name.append(f'mfcc_{j}')
        col_name += ['sc_max', 'sc_mean', 'sc_min', 'sc_std']
        col_name += ['sk_max', 'sk_mean', 'sk_min', 'sk_std']
        col_name += ['sr_max', 'sr_mean', 'sr_min', 'sr_std']
        col_name += ['ss_max', 'ss_mean', 'ss_min', 'ss_std']
        col_name += ['sf_max', 'sf_mean', 'sf_min', 'sf_std']
        col_name += ['zcr_max', 'zcr_mean', 'zcr_min', 'zcr_std']
        # col_name.append('all_bc')
        # col_name.append('all_bpm')
        # col_name.append('all_or')
        # col_name.append('all_da')
        # for j in range(1, 14):
        #     col_name.append(f'all_mfcc_{j}')
        # col_name += ['all_sc_max', 'all_sc_mean', 'all_sc_min', 'all_sc_std']
        # col_name += ['all_sk_max', 'all_sk_mean', 'all_sk_min', 'all_sk_std']
        # col_name += ['all_sr_max', 'all_sr_mean', 'all_sr_min', 'all_sr_std']
        # col_name += ['all_ss_max', 'all_ss_mean', 'all_ss_min', 'all_ss_std']
        # col_name += ['all_sf_max', 'all_sf_mean', 'all_sf_min', 'all_sf_std']
        # col_name += ['all_zcr_max', 'all_zcr_mean', 'all_zcr_min', 'all_zcr_std']

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
            vec += list(data['lowlevel']['spectral_rolloff'].values())
            vec += list(data['lowlevel']['spectral_skewness'].values())
            vec += list(data['lowlevel']['spectral_flux'].values())
            vec += list(data['lowlevel']['zerocrossingrate'].values())

            all_data.append(vec)

        col_name = self.get_col_name()
        df = pd.DataFrame(all_data, columns=col_name)
        df.to_csv(f'../data/csv/track_vectors_bow.csv')



