[![Pylint](https://github.com/domx4q/youtubeDownloader/actions/workflows/pylint.yml/badge.svg)](https://github.com/domx4q/youtubeDownloader/actions/workflows/pylint.yml)

## _Warning_
Currently, this project won't work properly because of a bug in [PyTube #1678](https://github.com/pytube/pytube/issues/1678).
There is a temporary fix (see here [Fix](https://github.com/pytube/pytube/issues/1678#issuecomment-1603948730)), but it's currently not applied for a release.
So the fix need to be applied manually.

# Overview
This Project uses [PyTube](https://github.com/pytube/pytube) to download YouTube videos.<br>
It's combined with a GUI made with [Tkinter](https://docs.python.org/3/library/tkinter.html) and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

# Installation and Usage
## Installation
1. Clone the repository with `git clone https://github.com/domx4q/youtubeDownloader.git`
2. Open the directory with `cd youtubeDownloader`
3. Install the requirements with `pip install -r requirements.txt`

## Usage
1. Run the script with `python3 main.py` or on Windows `py main.py`
2. Paste the link of the YouTube video you want to download into the input field
3. Click on `Search`
4. Fill out the options:
   1. `Video or Audio`: Choose if you want to download the video or only the audio
   2. `Resolution`: Choose the resolution of the video (only if you choose `Video`)
   3. `Filename`: *[ Optional ]* Choose the filename of the downloaded file
5. Click on `Download`
6. Wait until the download is finished
7. _Enjoy your downloaded video/audio_

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
