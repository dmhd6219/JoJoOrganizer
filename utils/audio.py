# modified bass-boost script from github
#
# https://github.com/paarthmadan/bass-boost

import math
from os import listdir, remove

from PyQt5 import QtCore
from pydub import AudioSegment

import numpy as np
from utils.other import musicdir


attenuate_db = 0
accentuate_db = 4


def bass_line_freq(track):
    sample_track = list(track)

    # c-value
    est_mean = np.mean(sample_track)

    # a-value
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor


class Bassbooster(QtCore.QObject):
    setProgress = QtCore.pyqtSignal(int)

    def run(self):
        list = listdir(musicdir)
        for filename in list:
            sample = AudioSegment.from_wav(musicdir + "/" + filename)
            filtered = sample.low_pass_filter(bass_line_freq(sample.get_array_of_samples()))
    
            combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
            combined.export(musicdir + '/' + filename, format="wav")
            progress = (list.index(filename) + 1) / len(list) * 100
            self.setProgress.emit(progress)


class Converter(QtCore.QObject):
    setProgress = QtCore.pyqtSignal(int)

    def run(self):
        list = listdir(musicdir)
        for filename in list:
            if not filename.endswith("wav"):            
                mp3 = AudioSegment.from_mp3(musicdir + "/" + filename)
        
                remove(musicdir + '/' + filename)
                mp3.export(musicdir + '/' + filename.replace(".mp3", ".wav"), format="wav")
            
            progress = (list.index(filename) + 1) / len(list) * 100
            self.setProgress.emit(progress)
