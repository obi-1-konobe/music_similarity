import os
from multiprocessing import Pool
import librosa as lr
import numpy as np
from skimage.io import imshow, imsave
from tqdm import tqdm

import modules.config as c

class Spectrograms:

    def __init__(self):
        pass

    def run(self):
        images = set(os.listdir(c.IMG_SAVE_PATH))
        process_list = list()
        folders = os.listdir(c.AUDIO_FOLDERS_PATH)
        for folder_name in tqdm(folders):
            files = os.listdir(f'{c.AUDIO_FOLDERS_PATH}{folder_name}')
            for file_name in files:
                img_name = f'{file_name[:-3]}.png'
                if img_name not in images:
                    audio_path = f'{c.AUDIO_FOLDERS_PATH}{folder_name}/{file_name}'
                    img_path = f'{c.IMG_SAVE_PATH}{img_name}'
                    process_list.append((audio_path, img_path))

        pool = Pool(4)
        pool.map(self.get_mel_spec, process_list)


    def scale_minmax(self, X, min=0.0, max=1.0):
        X_std = (X - X.min()) / (X.max() - X.min())
        X_scaled = X_std * (max - min) + min
        X_scaled = X_scaled[:, :c.SPEC_X_SIZE]
        return X_scaled.astype(np.uint8)

    def get_mel_spec(self, process_tuple):
        path_sound, path_img = process_tuple
        try:
            y, sr = lr.load(path_sound)
            S = lr.feature.melspectrogram(y=y, sr=sr, hop_length=512, win_length=1024)
            S_dB = lr.power_to_db(S, ref=np.max)
            img = self.scale_minmax(S_dB, 0, 255)
            img = np.flip(img, axis=0)
            imsave(path_img, img)
        except Exception:
            pass
