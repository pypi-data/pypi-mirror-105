<p align = "center">
    <a href = "https://github.com/Devansh3712/DevPlayer"><img src = "https://socialify.git.ci/Devansh3712/DevPlayer/image?forks=1&language=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Dark"></a>
</p>

<h1 align = "center"> DevPlayer </h1>
<p align = "center"><i> CLI for playing music and creating playlists using Python </i></p>

<p align = "center">
    <a href = "https://www.python.org"><img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/></a>
    <a href = "./LICENSE"><img src = "https://img.shields.io/github/license/Devansh3712/PySQL?style=for-the-badge"></a>
    <a href = "https://pypi.org/project/pysql-cli/"><img src = "https://img.shields.io/badge/PyPi-0.1.2-blue?style=for-the-badge&logo=appveyor"></a>
</p>

---

## Installation

- Installation pre-requisites
    - `ffmpeg`

- Using `PyPi package`

    > Windows

    ```console
    pip install devplayer
    ```

    > MacOS / Linux

    ```console
    pip3 install devplayer
    ```

- Using `setup.py`
    - clone the repository to local machine

    ```console
    git clone https://github.com/Devansh3712/DevPlayer
    ```
    - install `devplayer`

    > Windows

    ```console
    python setup.py install
    ```

    > MacOS / Linux

    ```console
    python3 setup.py
    ```

## Usage

```
Usage: dev [OPTIONS] COMMAND [ARGS]...

  CLI for playing music and creating playlists

Options:
  --help  Show this message and exit.

Commands:
  add       add song to a playlist
  all       show all playlists
  delete    delete a playlist
  new       create a new playlist
  play      play a playlist
  playsong  play a song from a playlist
  remove    remove a song from a playlist
  show      show songs in a playlist
```

- `add`

    ```
    Usage: dev add [OPTIONS]

    add song to a playlist

    Options:
    -p, --playlist TEXT  name of playlist to add  [required]
    -c, --custom TEXT    give custom name to song
    -u, --url TEXT       URL of the song
    -n, --name TEXT      name of the song
    --help               Show this message and exit.
    ```

    - downloads and adds the given song to the input playlist. `YouTube URL` or `name` of song can be used to add, with respective flags

- `all`

    ```
    Usage: dev all [OPTIONS]

    show all playlists

    Options:
    --help  Show this message and exit.
    ```

    - shows all available playlists in the local machine

- `delete`

    ```
    Usage: dev delete [OPTIONS]

    delete a playlist

    Options:
    -p, --playlist TEXT  name of playlist  [required]
    --help               Show this message and exit.
    ```

    - delete a playlist along with all its contents

- `new`

    ```
    Usage: dev new [OPTIONS]

    create a new playlist

    Options:
    -n, --name TEXT  name of the playlist  [required]
    --help           Show this message and exit.
    ```

    - creates a new empty playlist in the local machine

- `play`

    ```
    Usage: dev play [OPTIONS]

    play a playlist

    Options:
    -s, --shuffle        shuffle the playlist
    -p, --playlist TEXT  name of playlist to play  [required]
    --help               Show this message and exit.
    ```

    - play all the songs in the input playlist, use `-s` or `--shuffle` flag to shuffle the songs in the playlist

- `playsong`

    ```
    Usage: dev playsong [OPTIONS]

    play a song from a playlist

    Options:
    -n, --name TEXT      name of the song  [required]
    -p, --playlist TEXT  name of playlist  [required]
    --help               Show this message and exit.
    ```

    - play a single specified song from the input playlist

- `remove`

    ```
    Usage: dev remove [OPTIONS]

    remove a song from a playlist

    Options:
    -n, --name TEXT      name of the song  [required]
    -p, --playlist TEXT  name of playlist  [required]
    --help               Show this message and exit.
    ```

    - remove a single specified song from the input playlist

- `show`

    ```
    Usage: dev show [OPTIONS]

    show songs in a playlist

    Options:
    -p, --playlist TEXT  name of the playlist  [required]
    --help               Show this message and exit.
    ```

    - shows all available songs of the input playlist
