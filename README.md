# Endeless
> Making seamless transition in your playlists.

![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)

What Endeless can do :
1. Create a mix with a fix number of songs, starting with a song of your choice with seamless transitions
2. Create a playlist starting and ending with songs of your choosing, Endeless will fill the gap between these songs with songs and seamless transitions

## Install Endeless
Simply run :

  ```
  $ pip install Endeless==0.1
  ```

## Requirements
You will need a few packages (if you don't use pip install) :
- `pydub` to handle audio files and crossfades [(link)](https://github.com/jiaaro/pydub).
- `librosa` for the analyse of audio files [(link)](https://github.com/librosa/librosa).
- `numpy`, and `pandas`.
- `libfmp` for the Fundamentals of Music Processing [(link)](https://github.com/meinardmueller/libfmp).
- `requests` for web requests [(link)](https://github.com/psf/requests).
- `beautifulsoup4` which allows to use BeautifulSoup for web parsing.
- `mutagen` to handle mp3 metadata [(link)](https://github.com/quodlibet/mutagen).
<br>
 Thanks to all the creators of these libraries.
 
## How to make it work
You have to fill the songs folder with audio files (mp3 for now) of your songs. You must fill the metadata "name" and "artist" in the songs' properties for it to work well. I encourage you to select an important number of songs.
<br> Now that our songs are prepared, we can run :

  ```
  $ Endeless -r
  ```

This will reset the dataset that contains my examples. Now you can specify the path to your folder with the audio files or put the songs in the dedicated folder in the repository : 


  ```
  $ Endeless -S
  ```


Now you can update your dataset :

  ```
  $ Endeless -d
  ```

You will be asked to submit the time in ms of the first note and last note of each songs. Then, you might enter the chords yourself or let chord recognition do the job.

  ```
  $ Endeless -s
  ```

Take a look at your dataset before creating playlists.

## What can Endeless do ?

- Create a mix with a fix number of songs, starting with a song (enter the exact name of the song, use -s to check) of your choice with seamless transitions
  
  ```
  $ Endeless -m "Thunder"
  ```
  
- Create a playlist starting and ending with songs of your choosing, Endeless will fill the gap between these songs with songs and seamless transitions

  ```
  $ Endeless -p "Thunder" "Animals"
  ```

### Possible problems:
- #### "What do you mean by 'the time of the last note' ?"
The time of the last note is actually the beginning of the last note (same for the first note), just like chords in a tablature.
- #### "I can't find enough songs to make this work."
I'm really sorry but you need a number of songs that is large enough for the program to find songs that match with each other. Still, I can suggest to you my Songs-dataset.csv from the repository which contains a few songs that work well together. 

### Warning :
This is a personal project, please email me at contact.keyofmagic@gmail.com if you have any problem with Endeless.
