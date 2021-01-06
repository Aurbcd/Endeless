import pandas as pd
from Endeless.workers.chord_recognition import *
from mutagen.easyid3 import EasyID3
import glob
import librosa
import libfmp.c5

chord_labels = libfmp.c5.get_chord_labels()

def update_dataset(df_path, path_directory, web_verification=True):
    """
    df_path: path of the dataframe containing all the songs data
    path_directory: path of the directory where all the audio files are
    web_verification: boolean to turn on web_verification

    returns the dataset updated
    """
    df_song = pd.read_csv(df_path)
    songs_mp3 = glob.glob(path_directory + "*.mp3")
    songs_wav = glob.glob(path_directory + "*.wav")
    songs = songs_mp3 + songs_wav
    for song in songs:
        if song not in df_song['File_Name'].to_numpy():
            audio = EasyID3(song)
            try:
                title = audio['title'][0]
                artist = audio['artist'][0]
            except KeyError:
                print(f"ERROR : Please fill title and artist metadata in the mp3 properties of {song}.")
                return
            if df_song[(df_song['Song'] == title) & (df_song['Artist'] == artist)].shape[0] == 0:
                print(f"{title} - {artist}")
                print('-----')
                x, Fs = librosa.load(song)
                duration = x.shape[0] / Fs

                First_Note_Time = ""
                Last_Note_Time = ""
                First_Note = ""
                Last_Note = ""
                while First_Note_Time == "":
                    First_Note_Time = int(input("Enter the first note time (ms) :\n"))

                while Last_Note_Time == "":
                    Last_Note_Time = int(input("Enter the last note time (ms) :\n"))

                while First_Note not in chord_labels:
                    First_Note = input("Enter the first chord (press enter for chord recognition) :")
                    if First_Note == "":
                        print("-- chord recognition --")
                        First_Note = chord_recognition(song, First_Note_Time, 2)
                        if web_verification:
                            if web_scrapping_verification(title, artist) is not None:
                                chords, last_chord = web_scrapping_verification(title, artist)
                                if First_Note not in chords:
                                    First_Note = input(f"According to the web, the chords of {title} by {artist} are {chords}, however chord recognition found {First_Note}. Choose a closest chord from the chord recognition according to this list :\n")
                            else:
                                print('Web verification : Page not found | Check the mp3 metadata.')
                    if First_Note not in chord_labels:
                        print(f"Must be a chord in this list : {chord_labels}")

                while Last_Note not in chord_labels:
                    Last_Note = input("Enter the last chord (press enter for chord recognition) :")
                    if Last_Note == "":
                        print("-- chord recognition --")
                        Last_Note = chord_recognition(song, Last_Note_Time, -2)
                        if web_verification & (web_scrapping_verification(title, artist) is not None):
                            if Last_Note not in chords:
                                Last_Note = input(
                                    f"According to the web, the chords of {title} by {artist} are {chords}, more specifically, the last chord seems to be {last_chord}. However chord recognition found {Last_Note}, choose the chord to add in the dataset :\n")
                    if Last_Note not in chord_labels:
                        print(f"Must be a chord in this list : {chord_labels}")


                df_song = df_song.append({"Song":title, 'Artist':artist, 'Duration': int(duration*1000), 'First_Note_Time':First_Note_Time, 'First_Note':First_Note, "Last_Note_Time": Last_Note_Time, 'Last_Note':Last_Note, 'File_Name':song}, ignore_index=True)
    df_song.to_csv(df_path, index=False)

def add_to_dataset(df_path,file,web_verification=True):
    """
    df_path: path of the dataframe containing all the songs data
    file: path of the audio file to add to the dataset
    web_verification: boolean to turn on web_verification

    returns the dataset updated
    """
    df_song = pd.read_csv(df_path)
    if file not in df_song['File_Name'].to_numpy():
        audio = EasyID3(file)
        try:
            title = audio['title'][0]
            artist = audio['artist'][0]
        except KeyError:
            print("Please fill title and artist metadata in the mp3 properties.")
            return
        if df_song[(df_song['Song'] == title) & (df_song['Artist'] == artist)].shape[0] == 0:
            print(f"{title} - {artist}")
            print('-----')
            First_Note_Time = ""
            Last_Note_Time = ""
            First_Note = ""
            Last_Note = ""
            while First_Note_Time == "":
                First_Note_Time = int(input("Enter the first note time (ms) :\n"))

            while Last_Note_Time == "":
                Last_Note_Time = int(input("Enter the last note time (ms) :\n"))

            while First_Note not in chord_labels:
                First_Note = input("Enter the first chord (press enter for chord recognition) :")
                if First_Note == "":
                    print("-- chord recognition --")
                    First_Note = chord_recognition(file, First_Note_Time, 2)
                    if web_verification:
                        if web_scrapping_verification(title, artist) is not None:
                            chords, last_chord = web_scrapping_verification(title, artist)
                            if First_Note not in chords:
                                First_Note, _ = input(f"According to the web, the chords of {title} by {artist} are {chords}, however chord recognition found {First_Note}. Choose a close chord from the chord recognition according to this list :\n")
                        else:
                            print('Web verification : Page not found | Check the mp3 metadata.')
                if First_Note not in chord_labels:
                    print(f"Must be a chord in this list : {chord_labels}")

            while Last_Note not in chord_labels:
                Last_Note = input("Enter the last chord (press enter for chord recognition) :")
                if Last_Note == "":
                    print("-- chord recognition --")
                    Last_Note = chord_recognition(file, Last_Note_Time, -2)
                    if web_verification & (web_scrapping_verification(title, artist) is not None):
                        if Last_Note not in chords:
                            Last_Note = input(f"According to the web, the chords of {title} by {artist} are {chords}, more specifically, the last chord seems to be {last_chord}. However chord recognition found {Last_Note}, choose the chord to add in the dataset :\n")
                if Last_Note not in chord_labels:
                    print(f"Must be a chord in this list : {chord_labels}")
        else:
            print("The song seems to already be in the dataset")
    else :
        print("The song seems to already be in the dataset")

    df_song.to_csv(df_path, index=False)

def reset_dataset(df_path):
    """
    df_path: path of the dataframe containing all the songs data

    returns the dataset reinitialized
    """
    dataset = pd.DataFrame(columns=['Song','Artist','Duration','First_Note','First_Note_Time','Last_Note','Last_Note_Time','File_Name'])
    dataset.to_csv(df_path, index=False)