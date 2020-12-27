# Endeless
> Making seamless transition in your playlists.

![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)

What Endeless can do :
1. Create a mix with a fix number of songs, starting with a song of your choice with seamless transitions
2. Create a playlist starting and ending with songs of your choosing, Endeless will fill the gap between these songs with songs and seamless transitions

## Installation
You will need a few packages :
- `pydub` to handle audio files and crossfades.[(link)](https://github.com/jiaaro/pydub)
- `librosa` for the analyse of audio files [(link)](https://github.com/librosa/librosa).
- `numpy`, `json`, `glob`, and `pandas`.
- `libfmp` for the Fundamentals of Music Processing [(link)](https://github.com/meinardmueller/libfmp).
- `requests` for web requests [(link)](https://github.com/psf/requests).
- `re` for regEx [(link)](https://github.com/psf/requests).
- `bs4` which allows to use BeautifulSoup for web parsing [(link)](https://github.com/psf/requests).
- `mutagen` to handle mp3 metadata. [(link)](https://github.com/quodlibet/mutagen)
<br>
 Thanks to all the creators of these libraries.
 
## How to make it work
You have to fill the songs folder with audio files (mp3 for now) of your songs. You must fill the metadata "name" and "artist" in the songs' properties for it to work well. I encourage you to select an important number of songs.
<br> Now that our songs are prepared, we can run :

  ```
  $ python endeless -r
  ```

This will reset the dataset that contains my examples. Now you can update your dataset :

  ```
  $ python endeless -d
  ```

You will be asked to submit the time in ms of the first note and last note of each songs. Next, you might enter the chords yourself or let chord recognition do the job.

  ```
  $ python endeless -s
  ```

Take a look at your dataset before creating playlists.

## What can Endeless do ?

- Create a mix with a fix number of songs, starting with a song (enter the exact name of the song, use -s to check) of your choice with seamless transitions
  ```
  $ python endeless -m "Thunder"
  ```
- Create a playlist starting and ending with songs of your choosing, Endeless will fill the gap between these songs with songs and seamless transitions

  ```
  $ python endeless -p "Thunder" "Animals"
  ```

### Possible problems:
- #### "What do you mean by 'the time of the last note' ?"
The time of the last note is actually the beginning of the last note (same for the first note), just like chords in a tablature.
- #### "I can't find enough songs to make this work."
I'm really sorry but you need a number of songs that is large enough for the program to find songs that match with each other. Still, I can suggest to you my Songs-dataset.csv from the repository which contains a few songs that work well together. 

### Warning :
This is a personal project, please email me at contact.keyofmagic@gmail.com if you have any problem with Endeless.
