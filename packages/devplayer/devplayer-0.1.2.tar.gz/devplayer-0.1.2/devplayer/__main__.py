import halo
import os
import click
import sys
import playsound
import random
import shutil
from colorama import init, Fore, Style
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import devplayer.songs as songs

init(convert = True)

# create "playlist" directory if it doesn't exist
playlist_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "playlists")
if not os.path.isdir(playlist_dir):
    os.mkdir(playlist_dir)

@click.group()
def dev():
    """CLI for playing music and creating playlists"""

@dev.command()
def all():
    """show all playlists"""

    try:
        directory = os.path.dirname(os.path.realpath(__file__))
        playlists = [folder for folder in os.listdir(os.path.join(directory, "playlists"))]

        print(f"\n{Fore.LIGHTMAGENTA_EX}Available Playlists:{Style.RESET_ALL}")

        for playlist in playlists:
            print(f"• {playlist}")

    except:
        print(f"{Fore.RED}Unable to show playlists{Style.RESET_ALL}")

@click.option("-p", "--playlist", help = "name of playlist to play", required = True)
@click.option("-s", "--shuffle", type = bool, default = False, is_flag = True, help = "shuffle the playlist")
@dev.command()
def play(playlist: str, shuffle: bool):
    """play a playlist"""

    try:
        if playlist is not None:
            directory = os.path.dirname(os.path.realpath(__file__))
            playlists = [folder for folder in os.listdir(os.path.join(directory, "playlists"))]

            if playlist in playlists:
                songs = os.listdir(os.path.join(directory, "playlists", playlist))
                max_len = 0

                if shuffle is False:
                    for song in songs:
                        max_len = max(max_len, len(song))
                        spaces = " " * abs(len(song) - max_len)
                        spin_dict = {"interval": 80, "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]}
                        spinner = halo.Halo(text = f"{Fore.GREEN}Now playing:{Style.RESET_ALL} {song[:-4]}{spaces}\r", spinner = spin_dict, color = "grey")
                        spinner.start()
                        playsound.playsound(os.path.join(directory, "playlists", playlist, song))
                        spinner.stop()

                else:
                    # shuffle the list of songs
                    shuffled = random.shuffle(songs)

                    for song in songs:
                        max_len = max(max_len, len(song))
                        spaces = " " * abs(len(song) - max_len)
                        spin_dict = {"interval": 80, "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]}
                        spinner = halo.Halo(text = f"{Fore.GREEN}Now playing:{Style.RESET_ALL} {song[:-4]}{spaces}\r", spinner = spin_dict, color = "grey")
                        spinner.start()
                        playsound.playsound(os.path.join(directory, "playlists", playlist, song))
                        spinner.stop()

            else:
                print(f"{Fore.YELLOW}Playlist not found{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}Unable to play the playlist{Style.RESET_ALL}")

    except:
        print(f"{Fore.RED}Unable to play the playlist{Style.RESET_ALL}")

@click.option("-n", "--name", help = "name of the playlist", required = True)
@dev.command()
def new(name: str):
    """create a new playlist"""

    if name is not None:
        directory = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(os.path.join(directory, "playlists", name)):
            os.mkdir(os.path.join(directory, "playlists", name))
            print(f"{Fore.GREEN}{name} playlist created{Style.RESET_ALL}")
        
        else:
            print(f"{Fore.YELLOW}{name} playlist already exists{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}Unable to create playlist{Style.RESET_ALL}")

@click.option("-p", "--playlist", help = "name of the playlist", required = True)
@dev.command()
def show(playlist: str):
    """show songs in a playlist"""

    if playlist is not None:
        directory = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(os.path.join(directory, "playlists", playlist)):
            print(f"{Fore.YELLOW}{playlist} playlist not found{Style.RESET_ALL}")

        else:
            songs = os.listdir(os.path.join(directory, "playlists", playlist))
            print(f"\n{Fore.LIGHTMAGENTA_EX}Songs in {playlist}:{Style.RESET_ALL}")

            for song in songs:
                print(f"• {song[:-4]}")
    
    else:
        print(f"{Fore.RED}Unable to show songs{Style.RESET_ALL}")

@click.option("-n", "--name", help = "name of the song")
@click.option("-u", "--url", help = "URL of the song")
@click.option("-c", "--custom", help = "give custom name to song")
@click.option("-p", "--playlist", help = "name of playlist to add", required = True)
@dev.command()
def add(name: str, url: str, custom: str, playlist: str):
    """add song to a playlist"""

    if name:

        url = songs.get_song_url(name)

        if custom is not None:
            result = songs.download_song(url, playlist, file_name = custom)

        else:
            result = songs.download_song(url, playlist)

        if result is not False:
            print(f"{Fore.GREEN}Song added to {playlist} playlist{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}Unable to add song to {playlist}{Style.RESET_ALL}")

    elif url:

        check = songs.check_url(url)

        if check is True:
            if custom is not None:
                result = songs.download_song(url, playlist, file_name = custom)

            else:
                result = songs.download_song(url, playlist)

            if result is not False:
                print(f"{Fore.GREEN}Song added to {playlist} playlist{Style.RESET_ALL}")

            else:
                print(f"{Fore.YELLOW}Unable to add song to {playlist}{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}URL is not valid{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}Unable to add the song{Style.RESET_ALL}")

@click.option("-p", "--playlist", help = "name of playlist", required = True)
@dev.command()
def delete(playlist: str):
    """delete a playlist"""

    if playlist is not None:

        try:
            directory = os.path.dirname(os.path.realpath(__file__))
            shutil.rmtree(os.path.join(directory, "playlists", playlist))

            print(f"{Fore.GREEN}{playlist} playlist deleted{Style.RESET_ALL}")

        except:
            print(f"{Fore.RED}Unable to delete {playlist} playlist{Style.RESET_ALL}")

@click.option("-p", "--playlist", help = "name of playlist", required = True)
@click.option("-n", "--name", help = "name of the song", required = True)
@dev.command()
def remove(playlist: str, name: str):
    """remove a song from a playlist"""

    if playlist is not None:

        if name is not None:

            directory = os.path.dirname(os.path.realpath(__file__))

            if os.path.isfile(os.path.join(directory, "playlists", playlist, f"{name}.mp3")):
                os.remove(os.path.join(directory, "playlists", playlist, f"{name}.mp3"))
                print(f"{Fore.GREEN}{name} removed from {playlist} playlist{Style.RESET_ALL}")

            else:
                print(f"{Fore.YELLOW}Song not found in playlist{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}Song not found in playlist{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}Unable to remove song from playlist{Style.RESET_ALL}")

@click.option("-p", "--playlist", help = "name of playlist", required = True)
@click.option("-n", "--name", help = "name of the song", required = True)
@dev.command()
def playsong(playlist: str, name: str):
    """play a song from a playlist"""

    if playlist is not None:

        if name is not None:

            directory = os.path.dirname(os.path.realpath(__file__))

            if os.path.isfile(os.path.join(directory, "playlists", playlist, f"{name}.mp3")):
                spin_dict = {"interval": 80, "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]}
                spinner = halo.Halo(text = f"{Fore.GREEN}Now playing:{Style.RESET_ALL} {name}", spinner = spin_dict, color = "grey")
                spinner.start()
                playsound.playsound(os.path.join(directory, "playlists", playlist, f"{name}.mp3"))
                spinner.stop()

            else:
                print(f"{Fore.YELLOW}Song not found in playlist{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}Song not found in playlist{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}Unable to play song from playlist{Style.RESET_ALL}")

if __name__ == "__main__":
    dev(prog_name = "dev")

"""
DevPlayer
Devansh Singh, 2021
"""
