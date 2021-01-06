import os
import librosa
import numpy as np
import libfmp.c5
import requests
from bs4 import BeautifulSoup
import json
import re


def compute_chromagram_from_filename(fn_wav, Fs=22050, N=4096, H=2048,seperation=None, gamma=None, version='STFT', norm='2'):
    """Compute chromagram for WAV file specified by filename
    Args :
        fn_wav : Filenname of WAV
        Fs : Sampling rate
        N : Window size
        H : Hop size
        seperation : represents a way for me to only analyse the first half (set it to 2) or second half of the song (set it to -2)
        gamma : Constant for logarithmic compression
        version : Technique used for front-end decomposition ('STFT', 'IIS', 'CQT')
        norm : If not 'None', chroma vectors are normalized by norm as specified ('1', '2', 'max')

    Returns:
        X : Chromagram
        Fs_X : Feature reate of chromagram
        x : Audio signal
        Fs : Sampling rate of audio signal
        x_dur : Duration (seconds) of audio signal
    """
    x, Fs = librosa.load(fn_wav, sr=Fs)
    if seperation == None:
        x=x
    elif seperation > 0:
        x = x[:int(x.shape[0]/seperation)]
    elif seperation < 0:
        x = x[int(x.shape[0]/(-seperation)):]
    x_dur = x.shape[0] / Fs
    if version == 'STFT':
        # Compute chroma features with STFT
        X = librosa.stft(x, n_fft=N, hop_length=H, pad_mode='constant', center=True)
        if gamma is not None:
            X = np.log(1 + gamma * np.abs(X) ** 2)
        else:
            X = np.abs(X) ** 2
        X = librosa.feature.chroma_stft(S=X, sr=Fs, tuning=0, norm=None, hop_length=H, n_fft=N)
    if version == 'CQT':
        # Compute chroma features with CQT decomposition
        X = librosa.feature.chroma_cqt(y=x, sr=Fs, hop_length=H, norm=None)
    if version == 'IIR':
        # Compute chroma features with filter bank (using IIR elliptic filter)
        X = librosa.iirt(y=x, sr=Fs, win_length=N, hop_length=H, center=True, tuning=0.0)
        if gamma is not None:
            X = np.log(1.0 + gamma * X)
        X = librosa.feature.chroma_cqt(C=X, bins_per_octave=12, n_octaves=7,
                                       fmin=librosa.midi_to_hz(24), norm=None)
    if norm is not None:
        X = libfmp.c3.normalize_feature_sequence(X, norm='2')
    Fs_X = Fs / H
    return X, Fs_X, x, Fs, x_dur

def optimize(chord_max):
    """
    chord_max : matrix containing a 1 for each chord it thinks is the most probable
    returns the same matrix but links outliers to the next chord to make more relevant data
    """
    matrix = chord_max.T.copy()
    for i in range(1,matrix.shape[0]-1):
        if (np.argmax(matrix[i]) != np.argmax(matrix[i-1])) & (np.argmax(matrix[i]) != np.argmax(matrix[i+1])):
            matrix[i] = matrix[i+1]
    return matrix.T

def chord_recognition(filepath, time, separation=None, N=4096, H = 2048):
    """
    filepath : path of the file to analyse
    time: when to do the chord recognition (in milliseconds)
    seperation : represents a way for me to only analyse the first half (set it to 2) or second half of the song (set it to -2)
    N : Window size
    H : Hop size
    returns the same matrix but links outliers to the next chord to make more relevant data
    """
    fn_wav = os.path.join(filepath)
    list_X=[]
    X, Fs_X, x, Fs, x_dur = compute_chromagram_from_filename(fn_wav, N=N, H=H, seperation=separation, version='CQT')
    list_X.append(X)
    X, Fs_X, x, Fs, x_dur = compute_chromagram_from_filename(fn_wav, N=N, H=H, gamma=0.1, seperation=separation, version='STFT')
    list_X.append(X)
    X, Fs_X, x, Fs, x_dur = compute_chromagram_from_filename(fn_wav, N=N, H=H, gamma=100, seperation=separation, version='IIR')
    list_X.append(X)

    weights=[0.9,1,1.1]

    chromagram = np.zeros((24,X.shape[1]))
    for i in range(len(list_X)):
        chord_sim, chord_max = libfmp.c5.chord_recognition_template(list_X[i], norm_sim='max')
        chord_max = optimize(chord_max)
        chromagram += chord_max*weights[i]
    chord_labels = libfmp.c5.get_chord_labels()

    time /= 10000
    print(chord_labels[(np.argmax(chromagram.T[int(time*Fs_X)]))])
    return chord_labels[(np.argmax(chromagram.T[int(time*Fs_X)]))]

def web_scrapping_verification(song, artist):
    """
    string song : Name of the song
    string artist : name of the artist
    returns : the list of chords in the song according to the web
    """
    req = requests.get("https://www.ultimate-guitar.com/search.php?title=" + artist +"+"+ song + "&type=300")
    html = BeautifulSoup(req.text,"html.parser")

    if 'No results' in html.text :
        return None

    j = json.loads(html.body.find(class_="js-store").get('data-content'))

    most_voted = 0
    best_link = ""
    for link in j["store"]["page"]["data"]['results']:
        try:
            if most_voted < link['votes']:
                most_voted = link['votes']
                best_link = link
        except:
            pass

    chord_labels = libfmp.c5.get_chord_labels() #for later

    req = requests.get(best_link['tab_url'])
    html = BeautifulSoup(req.text,"html.parser")
    tab = json.loads(html.body.find(class_="js-store").get('data-content'))['store']["page"]['data']['tab_view']['wiki_tab']['content']
    list_chords = []
    number_of_chords = len(list(re.finditer('/ch]', tab)))
    for i in range(number_of_chords):
        match = list(re.finditer('/ch]', tab))[i]
        chord = tab[match.start() - 2]
        if chord == 'm':
            chord = tab[match.start() - 3] + tab[match.start() - 2]
        if (chord in chord_labels) & (chord not in list_chords):
            list_chords.append(chord)
        if (chord in chord_labels) & (i == number_of_chords - 1):
            most_likely_last_chord = chord

    return list_chords, most_likely_last_chord