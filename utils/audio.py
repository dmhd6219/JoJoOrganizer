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
accentuate_db = 22


def bass_line_freq(track):
    sample_track = list(track)

    # c-value
    est_mean = np.mean(sample_track)

    # a-value
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor


class BaseAudioProcessor(QtCore.QObject):
    setProgress = QtCore.pyqtSignal(int)
    errCallback = QtCore.pyqtSignal(str, Exception)
    emptyCallback = QtCore.pyqtSignal()
    AllMP3Callback = QtCore.pyqtSignal()
    
    def run(self):
        dir = listdir(musicdir)
        if dir:
            try:
                self.process(dir)
            except IndexError:
                self.errCallback.emit(self.filename, Exception("Unsupported file format"))
            except PermissionError:
                self.errCallback.emit(self.filename, Exception("Cannot save, is file open in other program?"))
            except Exception as ex:
                self.errCallback.emit(self.filename, ex)    
        else:
            self.emptyCallback.emit()


class Converter(BaseAudioProcessor):
    
    def process(self, dir):
        if not list(filter(lambda x: not x.endswith("mp3"), dir)):
            self.AllMP3Callback.emit()
            return
        
        for filename in dir:
            self.filename = filename
            if not filename.endswith("mp3"):            
                mp3 = AudioSegment.from_file(musicdir + "/" + filename)
        
                remove(musicdir + '/' + filename)
                mp3.export(musicdir + '/' + "".join(filename.split(".")[:-1]) + ".mp3", format="mp3")
            
            progress = (dir.index(filename) + 1) / len(dir) * 100
            self.setProgress.emit(progress)


class Bassbooster(BaseAudioProcessor):
    
    def process(self, dir):
        for filename in dir:
            self.filename = filename
            if not filename.endswith("mp3"):
                raise IndexError()
                 
            sample = AudioSegment.from_mp3(musicdir + "/" + filename)
            filtered = sample.low_pass_filter(bass_line_freq(sample.get_array_of_samples()))
    
            combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
            combined.export(musicdir + '/' + filename, format="mp3")
            progress = (dir.index(filename) + 1) / len(dir) * 100
            self.setProgress.emit(progress)

