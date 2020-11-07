# modified bass-boost script from github
#
# https://github.com/paarthmadan/bass-boost

import math
from os import listdir, remove

from pydub import AudioSegment

import numpy as np

attenuate_db = 0
accentuate_db = 22


def bass_line_freq(track):
    sample_track = list(track)

    # c-value
    est_mean = np.mean(sample_track)

    # a-value
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor


def bassboost(songs_dir):
    for filename in listdir(songs_dir):
        sample = AudioSegment.from_wav(songs_dir + "/" + filename)
        filtered = sample.low_pass_filter(bass_line_freq(sample.get_array_of_samples()))
    
        combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
        combined.export(songs_dir + filename, format="wav")


def convertAll(dir):
    for filename in listdir(dir):
        mp3 = AudioSegment.from_mp3(dir + "/" + filename)
        
        remove(dir + filename)
        mp3.export(dir + filename.replace(".mp3", ".wav"), format="wav")
