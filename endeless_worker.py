import random
from pydub import AudioSegment
import pandas as pd
import numpy as np


class NoMoreSongToFitIn(Exception):
    """Exception raised when there is no more song to fit in the playlist."""
    pass


def random_search_next_song(playlist, df, song=None):
    """
    string song : initial song OR int song : index of the song

    df : dataframe of all the songs
    """
    if song == None:
        index = playlist[-1]
    elif isinstance(song, str):
        index = df[df['Song'] == song].index[0]
    else:
        index = song
    df_next_song = df[df["First_Note"] == df["Last_Note"][index]]
    if (all([i in playlist for i in df_next_song.index.tolist()])) or df_next_song.shape[0]==0:
        raise NoMoreSongToFitIn()
    index_next_song = random.choice(df_next_song.index.tolist())  # random search, show be more like dominos
    while index_next_song in playlist:  # Do not select the same song
        index_next_song = random.choice(df_next_song.index.tolist())
    return index_next_song


def add_with_transition(endless, song_in, playlist, df):
    """
    endless : list of songs

    string song_out : song ending OR int song : index of the song ending

    string song_in : song beginning OR int song_in : index of the song beginning

    df : dataframe of all the songs
    """
    if isinstance(song_in, str):
        index_in = df[df['Song'] == song_in].index[0]
    else:
        index_in = song_in

    index_out = playlist[-1]
    mp3_in = AudioSegment.from_mp3(df["File_Name"][index_in])


    # crossfade
    endless = endless.fade(from_gain=0, to_gain=-120, start=len(endless) - df["Duration"][index_out] + df["Last_Note_Time"][index_out], end=min(len(endless), len(endless) - df["Duration"][index_out] + df["Last_Note_Time"][index_out] + 5000))
    mp3_in = mp3_in.fade(from_gain=-120, to_gain=0, start=max(0, df["First_Note_Time"][index_in] - 5000),end=df["First_Note_Time"][index_in])
    position_start_song_in = len(endless) - df["First_Note_Time"][index_in] - (df["Duration"][index_out] - df["Last_Note_Time"][index_out])

    endless = endless.overlay(mp3_in, position=position_start_song_in)
    endless = endless.append(mp3_in[df["First_Note_Time"][index_in] + df["Duration"][index_out] - df["Last_Note_Time"][index_out]:])

    playlist.append(index_in)
    return endless


def begin_with(song, playlist, df):
    """
    endless : list of songs

    string song_in : song to begin with OR int song_in : index of the song to begin with

    df : dataframe of all the songs
    """
    if isinstance(song, str):
        index = df[df['Song'] == song].index[0]
    else:
        index = song
    endless = AudioSegment.from_mp3(df["File_Name"][index])
    playlist.append(index)
    return endless

def specific_search_fill_song(playlist, df, song_start=None,song_end=None):
    """
    string song : initial song OR int song : index of the song

    df : dataframe of all the songs
    """
    if song_start == None:
        index_start = playlist[-2]
    elif isinstance(song_start, str):
        index_start = df[df['Song'] == song_start].index[0]
    else:
        index_start = song_start

    if song_end == None:
        index_end = playlist[-1]
    elif isinstance(song_end, str):
        index_end = df[df['Song'] == song_end].index[0]
    else:
        index_end = song_end

    df_fill_song = df[df["First_Note"] == df["Last_Note"][index_start]]
    df_fill_song = df_fill_song[df_fill_song["Last_Note"] == df["First_Note"][index_end]]
    if (all([i in playlist for i in df_fill_song.index.tolist()])) or df_fill_song.shape[0]==0:
        raise NoMoreSongToFitIn()
    index_next_song = random.choice(df_fill_song.index.tolist())  # random search, show be more like dominos
    while index_next_song in playlist:  # Do not select the same song
        index_next_song = random.choice(df_fill_song.index.tolist())
    return index_next_song

def create_playlist(song_to_start, song_to_end, df, number_of_songs, export_file=True, show_playlist=True):
    if isinstance(song_to_start, str):
        index_start = df[df['Song'] == song_to_start].index[0]
    else:
        index_start = song_to_start

    if isinstance(song_to_end, str):
        index_end = df[df['Song'] == song_to_end].index[0]
    else:
        index_end = song_to_end

    #First we get the playlist, then we construct the endless
    playlist=[]
    endless = begin_with(index_start, playlist, df)
    temporary_playlist = [index_start, index_end]
    try:
        number_of_songs-=2
        while number_of_songs>0:
            fill_song_index = specific_search_fill_song(temporary_playlist, df, temporary_playlist[-2], temporary_playlist[-1])
            temporary_playlist.insert(len(temporary_playlist)-1,fill_song_index)
            number_of_songs -= 1

        for i in range(1,len(temporary_playlist)):
            endless = add_with_transition(endless, temporary_playlist[i], playlist, df)

    except NoMoreSongToFitIn:
        # Didn't reach the number of songs attended, retry
        endless, playlist = create_playlist(song_to_start, song_to_end, df, number_of_songs, export_file)

    if show_playlist:
        print("Playlist :",[df["Song"][i] for i in playlist])

    if export_file:
        with open(f"From {df['Song'][playlist[0]]} to {df['Song'][playlist[-1]]} - playlist.mp3",'wb') as out_f:
            endless.export(out_f, format='mp3')
        return endless, playlist
    else:
        return endless, playlist

def create_endeless_mix(song_to_start,number_of_songs, df, export_file=True, show_mix=True):
    if isinstance(song_to_start, str):
        index = df[df['Song'] == song_to_start].index[0]
    else:
        index = song_to_start

    if number_of_songs is None:
        raise ValueError("You have to give a number of songs in the playlist")

    playlist = []  # list of index
    endless = begin_with(index, playlist, df)
    try:
        song_counter = 1
        while song_counter != number_of_songs:
            next_song_index = random_search_next_song(playlist, df)
            endless = add_with_transition(endless, next_song_index, playlist, df)
            song_counter += 1
    except NoMoreSongToFitIn:
        # Didn't reach the number of songs attended, retry
        endless, playlist = create_endeless_mix(song_to_start,number_of_songs, df, export_file)

    if show_mix:
        print("Mix : ",[df["Song"][i] for i in playlist])

    if export_file:
        with open(f"Mix starting with {df['Song'][playlist[0]]} - playlist.mp3",'wb') as out_f:
            endless.export(out_f, format='mp3')
        return endless, playlist
    else:
        return endless, playlist
