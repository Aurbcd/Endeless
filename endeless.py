import dataset_update, endeless_worker
import pandas as pd

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)

if __name__ == '__main__':
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

    can.add_argument("-D", "--dataset_path", metavar="D", default="Songs-dataset.csv", type=str,
                     help="The csv dataset path.")

    action.add_argument("-d", "--update_dataset",  action='store_true',
                     help="Update the dataset with all songs from the songs folder.")

    action.add_argument("-a", "--add_to_dataset", metavar="a", default=None,
                     help="Add a specific song to the dataset, give the path of this song.")

    action.add_argument("-r", "--reset_dataset", action='store_true',
                     help="Reset/create the csv dataset at the path given.")

    the = can.parse_args()


    if the.update_dataset:
        print("-Updating dataset-")
        dataset_update.update_dataset(the.dataset_path, "songs/")
        print("-Updating Done-")

    df_song = pd.read_csv(the.dataset_path)

    if the.mix is not None:
        print("-Creating a mix-")
        if the.number_of_songs is None:
            the.number_of_songs = 3
        endeless_worker.create_endeless_mix(the.mix, the.number_of_songs, df_song)

    if the.playlist is not None:
        print("-Creating a playlist-")
        endeless_worker.create_playlist(the.playlist[0], the.playlist[1], df_song, number_of_songs=the.number_of_songs)

    if the.reset_dataset:
        dataset_update.reset_dataset(the.dataset_path)

    if the.show_dataset:
        print(df_song)

    if the.add_to_dataset is not None:
        print(f"-Adding {the.add_to_dataset} dataset-")
        dataset_update.add_to_dataset(the.dataset_path, the.add_to_dataset)