import os
import essentia.standard as es


class Extractor:

    def __init__(self):
        pass

    def run(self):
        path = '../data/fma_small/'
        dirs = os.listdir(path)
        essentia_listdir = os.listdir('../data/essentia_bow/')
        for some_dir in dirs:
            list_dir = os.listdir(f'{path}{some_dir}/')
            for track in list_dir:
                if (track[:-4] + '.json') in essentia_listdir:
                    continue
                try:
                    # self.extract_features_all(f'{path}{some_dir}/', track)
                    self.extract_features_intervals(f'{path}{some_dir}/', track)
                except Exception:
                    with open('../data/essentia_errors.txt', 'a+') as f:
                        f.write(track + '\n')
                    continue

    @staticmethod
    def extract_features_intervals(path, track_name):
        intervals = list(range(1, 31))
        for i in intervals:
            start = i - 1
            end = i
            features, features_frames = es.MusicExtractor(
                lowlevelStats=['mean', 'stdev', 'min', 'max'],
                rhythmStats=['mean', 'stdev', 'min', 'max'],
                tonalStats=['mean', 'stdev', 'min', 'max'],
                startTime=start,
                endTime=end
            )(f'{path}{track_name}')
            save_file = f'../data/essentia_bow/{track_name[:-4]}_{i}.json'
            es.YamlOutput(filename=save_file, format="json")(features)

    @staticmethod
    def extract_features_all(path, track_name):
        features, features_frames = es.MusicExtractor(
            lowlevelStats=['mean', 'stdev', 'min', 'max'],
            rhythmStats=['mean', 'stdev', 'min', 'max'],
            tonalStats=['mean', 'stdev', 'min', 'max'],
        )(f'{path}{track_name}')
        save_file = f'../data/essentia/{track_name[:-4]}.json'
        es.YamlOutput(filename=save_file, format="json")(features)


