"""
This is the main file for the project. It contains the entire code for the project.
The Goal of this project is to create a simple GUI to download videos or playlists from YouTube.
**********
Ideas:
- Resolution [✅]
- Downloading progress [✅]
- save name [✅]
- audio and video and file format options [❓]
- progress bar [✅]
- expected time and file size [✅]
- video title [✅]
- hyperlink to open file [❌]
"""

import _thread
import os
from datetime import datetime

import customtkinter as ctk
import pytube as pt
import pytube.exceptions


class GUI:
    """
    This class contains the GUI for the project.
    """

    def __init__(self):
        self.download_start_time = None
        self.progress_bar = None
        self.feedback_label = None
        self.resolution_select = None
        self.download_button = None
        self.hidden_group = None
        self.videoSettings = {}
        self.file_name = None
        self.progress_label = None
        self.stats_label = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.geometry("700x600")
        self.app.title("YouTube Downloader")
        self.app.configure(expand=True)

        self.create_widgets()

        self.app.mainloop()

    def create_widgets(self):
        url_input = ctk.CTkEntry(self.app, placeholder_text="Enter URL")
        url_input.pack(fill="x", padx=10, pady=10)

        search_button = ctk.CTkButton(self.app, text="Search", command=lambda: self.search(url_input.get()))
        search_button.pack(fill="x", padx=10, pady=10)

        # region hidden group
        self.hidden_group = ctk.CTkFrame(self.app)
        resolution_label = ctk.CTkLabel(self.hidden_group, text="Settings")
        resolution_label.pack(fill="x", padx=10, pady=10)

        mode_select = ctk.CTkComboBox(self.hidden_group, values=["Video", "Audio"],
                                      command=lambda x: self.update_settings("mode", x))
        mode_select.pack(fill="x", padx=10, pady=10)
        self.resolution_select = ctk.CTkComboBox(self.hidden_group, values=["Lädt ..."],
                                                 command=lambda x: self.update_settings("resolution", x))
        self.resolution_select.pack(fill="x", padx=10, pady=10)

        self.file_name = ctk.CTkEntry(self.hidden_group, placeholder_text="Enter file name")
        self.file_name.pack(fill="x", padx=10, pady=10)

        # endregion hidden group

        self.download_button = ctk.CTkButton(self.app, text="Download")

        def lDownload():
            _thread.start_new_thread(self.download, (url_input.get(),))

        self.download_button.configure(command=lDownload)

        progress_area = ctk.CTkFrame(self.app)
        progress_area.pack(fill="x", padx=10, pady=10, side="bottom")
        progress_row = ctk.CTkFrame(progress_area)
        progress_row.pack(fill="x", padx=10, pady=10, side="top")
        self.progress_bar = ctk.CTkProgressBar(progress_row, mode="determinate")
        self.progress_bar.pack(fill="x", padx=10, pady=10, side="left", expand=True)
        self.progress_label = ctk.CTkLabel(progress_row, text="0%")
        self.progress_label.pack(fill="x", padx=10, pady=10, side="left")
        self.resetProgress()
        self.stats_label = ctk.CTkLabel(progress_area, text=self.convertStatsString(), font=ctk.CTkFont(size=14))
        self.stats_label.pack(fill="x", padx=10, pady=10, side="bottom")

        self.feedback_label = ctk.CTkLabel(self.app, text="", text_color="white")
        self.feedback_label.pack(fill="x", padx=10, pady=10, side="bottom")

    def print(self, text, color="white"):
        self.feedback_label.configure(text=text, text_color=color)
        self.app.after(3500, lambda: self.__resetText()) # pylint: disable=unnecessary-lambda

    def __resetText(self):
        self.feedback_label.configure(text="", text_color="white")

    def update_settings(self, key, value):
        self.videoSettings[key] = value
        if key == "mode":
            if value == "Audio":
                self.resolution_select.pack_forget()
            else:
                self.resolution_select.pack(fill="x", padx=10, pady=10)

    def parse_settings(self):
        # return default parameters
        return {
            "mode": self.videoSettings.get("mode", "Video"),
            "resolution": self.videoSettings.get("resolution", "max")
        }

    def download(self, url):
        try:
            video = pt.YouTube(url,
                               on_progress_callback=self.on_progress,
                               on_complete_callback=self.on_complete)
            self.resetProgress()
        except pytube.exceptions.RegexMatchError:
            self.print("Invalid URL")
            return

        self.download_start_time = datetime.now()
        self.print("Downloading...")
        streams = video.streams
        settings = self.parse_settings()
        if settings["mode"] == "Video":
            if settings["resolution"] == "max":
                stream = streams.filter(progressive=True).order_by("resolution").desc().first()
            else:
                stream = streams.filter(progressive=True, resolution=settings["resolution"]).first()
        else:
            stream = streams.filter(only_audio=True).first()
        extension = "." + stream.default_filename.rsplit(".", 1)[1]
        if self.file_name.get() == "":
            fileName = stream.default_filename.rsplit(".", 1)[0]
        else:
            fileName = self.file_name.get()
        IS_MP3 = False
        if self.file_name.get().endswith(".mp3"):
            IS_MP3 = True
        else:
            fileName = fileName + extension
        stream.download("downloads", skip_existing=False, filename=fileName)
        self.print("Downloaded")
        if IS_MP3:
            self.convertToMP3("downloads/" + fileName)
            self.print("Converted to MP3")

    @staticmethod
    def convertToMP3(fileName):
        # rename
        os.rename(fileName, fileName.replace(".mp4", ".mp3"))
        return fileName.replace(".mp4", ".mp3")

    def search(self, url):
        try:
            video = pt.YouTube(url)

            resolutions = list(video.streams.filter(progressive=True).order_by("resolution").desc())
            resolutions = [resolution.resolution for resolution in resolutions]
            resolutions.append("max")
            # we need to recreate the entire combobox because we can't change the values
            self.resolution_select.destroy()
            self.resolution_select = ctk.CTkComboBox(self.hidden_group, values=resolutions,
                                                     command=lambda x: self.update_settings("resolution", x))
            self.resolution_select.pack(fill="x", padx=10, pady=10)
            self.file_name.configure(placeholder_text=video.title)

            self.download_button.pack_forget()
            self.hidden_group.pack(fill="x", padx=10, pady=10)
            self.download_button.pack(fill="x", padx=10, pady=10)  # pack again to make it appear at the bottom

            self.update_settings("resolution", resolutions[0])
        except pytube.exceptions.RegexMatchError:
            self.print("Invalid URL")
            return

    def on_progress(self, stream: pt.Stream, chunk: bytes, bytes_remaining: int) -> None: # pylint: disable=unused-argument
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent = (bytes_downloaded / total_size)
        self.progress_bar.set(percent)
        self.progress_label.configure(text=f"{round(percent * 100, 2)}%")
        self.progress_bar.configure(progress_color="#1f6aa5")
        print(f"{percent * 100:.2f}%")

        if self.download_start_time is None:
            self.download_start_time = datetime.now()
        seconds = (datetime.now() - self.download_start_time).total_seconds()
        try:
            speed = bytes_downloaded / seconds
            seconds_remaining = bytes_remaining / speed
        except ZeroDivisionError:
            seconds_remaining = 0
        seconds_remaining = int(seconds_remaining)
        self.stats_label.configure(text=self.convertStatsString(seconds_remaining, total_size, stream.title))

    def on_complete(self, stream: pt.Stream, file_path: str) -> None: # pylint: disable=unused-argument
        self.progress_bar.set(1)
        self.progress_label.configure(text="100%")
        self.progress_bar.configure(progress_color="green")

    def resetProgress(self):
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.progress_bar.configure(progress_color="#1f6aa5")

    def convertStatsString(self, seconds=0, size=0, title="Unknown"):
        return f"Estimated time: {self.convertSeconds(seconds)} | File size: {self.convertSize(size)} | Title: {title}"

    @staticmethod
    def convertSeconds(seconds):
        if seconds < 60: # pylint: disable=no-else-return
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{round(seconds / 60, 2)}m"
        else:
            return f"{round(seconds / 3600, 2)}h"

    @staticmethod
    def convertSize(size):
        if size < 1_000_000: # pylint: disable=no-else-return
            return f"{round(size / 1_000, 2)}KB"
        elif size < 1_000_000_000:
            return f"{round(size / 1_000_000, 2)}MB"
        else:
            return f"{round(size / 1_000_000_000, 2)}GB"


if __name__ == "__main__":
    GUI()
