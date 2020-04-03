import os
import essentia.standard as es


class Extractor:

    def __init__(self):
        pass

    def run(self):
        path = '../data/fma_small/'
        dirs = os.listdir(path)
        for some_dir in dirs:
            list_dir = os.listdir(f'{path}{some_dir}/')
            for track in list_dir:
                self.extract_features_all(f'{path}{some_dir}/', track)
                self.extract_features_intervals(f'{path}{some_dir}/', track)

    @staticmethod
    def extract_features_intervals(path, track_name):
        intervals = list(range(4, 33, 4))
        for i in intervals:
            start = i - 4
            end = i
            features, features_frames = es.MusicExtractor(
                lowlevelStats=['mean', 'stdev', 'min', 'max'],
                rhythmStats=['mean', 'stdev', 'min', 'max'],
                tonalStats=['mean', 'stdev', 'min', 'max'],
                startTime=start,
                endTime=end
            )(f'{path}{track_name}')
            save_file = f'../data/essentia/{track_name[:-4]}_{i/4}.json'
            es.YamlOutput(filename=save_file, format="json")(features)

    @staticmethod
    def extract_features_all(path, track_name):
        features, features_frames = es.MusicExtractor(
            lowlevelStats=['mean', 'stdev', 'min', 'max'],
            rhythmStats=['mean', 'stdev', 'min', 'max'],
            tonalStats=['mean', 'stdev', 'min', 'max'],
        )(f'{path}{track_name}')
        save_file = f'../data/essentia/{track_name}.json'
        es.YamlOutput(filename=save_file, format="json")(features)


