import Endeless.dataset.dataset_update as dataset_update
import Endeless.workers.endeless_worker as endeless_worker
import pandas as pd
import glob

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)

def console_entry_point():
    import argparse

    can = argparse.ArgumentParser()

    action = can.add_mutually_exclusive_group()

    action.add_argument("-s", "--show_dataset", action='store_true',
                     help="Show the dataset.")

    action.add_argument("-m", "--mix", metavar="m", default=None,
                     help="Creates a mix starting with the song you chose.")

    action.add_argument("-p", "--playlist", metavar="p", default=None, nargs="+",
                     help="Creates a playlist links the two songs you chose with songs.")

    can.add_argument("-n", "--number_of_songs", metavar="n", default=3, type=int,
                     help="Number of songs in the playlist.")

    action.add_argument("-d", "--update_dataset",  action='store_true',
                     help="Update the dataset with all songs from the songs folder.")

    action.add_argument("-a", "--add_to_dataset", metavar="a", default=None,
                     help="Add a specific song to the dataset, give the path of this song.")

    action.add_argument("-r", "--reset_dataset", action='store_true',
                     help="Reset/create the csv dataset at the path given.")

    action.add_argument("-S", "--change_songs_path",  action='store_true',
                     help="Change the path of the folder with all the audio files.")

    the = can.parse_args()

    f = open(dataset_update.__file__[:-17] + "dataset_path.txt", "r") #get path of module
    dirpath= f.read()
    f.close()

    if the.update_dataset:
        print("-Updating dataset-")
        print(dirpath)
        dataset_update.update_dataset(dataset_update.__file__[:-17] + "Songs-dataset.csv", dirpath)
        print("-Updating Done-")

    df_song = pd.read_csv(dataset_update.__file__[:-17] + "Songs-dataset.csv")

    if the.mix is not None:
        print("-Creating a mix-")
        endeless_worker.create_endeless_mix(the.mix, the.number_of_songs, df_song)

    if the.playlist is not None:
        print("-Creating a playlist-")
        endeless_worker.create_playlist(the.playlist[0], the.playlist[1], df_song, number_of_songs=the.number_of_songs)

    if the.reset_dataset:
        print("-Resetting the dataset-")
        dataset_update.reset_dataset(dataset_update.__file__[:-17] + "Songs-dataset.csv")

    if the.show_dataset:
        print(df_song)

    if the.add_to_dataset is not None:
        print(f"-Adding {the.add_to_dataset} dataset-")
        dataset_update.add_to_dataset(the.dataset_path, the.add_to_dataset)

    if the.change_songs_path:
        print("-Changing the path of the folder with audio files-")
        p = input(f"For now, the path to the folder is {dirpath}, press enter to pass or enter the new path :\n")
        if p != "":
            f = open(dataset_update.__file__[:-17] + "dataset_path.txt", "w")
            f.write(p)
            songs_mp3 = glob.glob(p + "*.mp3")
            songs_wav = glob.glob(p + "*.wav")
            songs = songs_mp3 + songs_wav
            if not songs:
                print("-Warning : The folder at this path have no audio files (mp3 or wav) in it-")
            f.close()
            print("-Changing the path of the folder with audio files : Done-")
        else:
            print("-Path not changed-")

if __name__ == '__main__':
    console_entry_point()