from pytube import YouTube
import customtkinter
from tkinter import messagebox, filedialog, simpledialog
from pathlib import Path
from datetime import datetime
import threading
from subprocess import Popen
from PIL import Image


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

with open("log.log", "w") as file:
    file.write("")


class App(customtkinter.CTk):
    APP_NAME = "Youtube Downloader"
    WIDTH = "800"
    HEIGHT = "500"

    video_counter = 0  # Counter index video_list
    download_counter = 0  # Counter index download_list
    status = 0  # Download status
    total_video_download = 0
    videos_widget = {}
    video_list_label = {}
    download_video_list_label = {}
    download_status_list_label = {}
    remove_video_widgets_button = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(self.APP_NAME)
        self.iconbitmap("img/icon.ico")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(int(self.WIDTH), int(self.HEIGHT))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.trash_img = customtkinter.CTkImage(
            Image.open("img/trash.png"),
            size=(16, 16),
        )

        self.left_frame = customtkinter.CTkFrame(
            master=self,
        )
        self.left_frame.grid(
            column=0, row=0,
            padx=0, pady=0,
            sticky="NS"
        )
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.video_frame = customtkinter.CTkScrollableFrame(
            master=self.left_frame,
        )
        self.video_frame.grid(
            column=0, row=2,
            padx=0, pady=0,
            sticky="NS"
        )
        self.video_frame.grid_columnconfigure(0, weight=1)

        self.right_frame = customtkinter.CTkFrame(
            master=self,
        )
        self.right_frame.grid(
            column=1, row=0,
            padx=0, pady=0,
            sticky="NSEW"
        )
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=1)

        self.status_frame = customtkinter.CTkFrame(
            master=self.right_frame,
        )
        self.status_frame.grid(
            column=0, row=3,
            columnspan=2,
            padx=0, pady=0,
            sticky="NSEW",
        )
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_frame.grid_columnconfigure(1, weight=1)

        # Left Frame
        self.url_entry = customtkinter.CTkEntry(
            master=self.left_frame,
            placeholder_text="Youtube URL",
        )
        self.url_entry.grid(
            column=0, row=0,
            padx=5, pady=5,
            sticky="EW"
        )

        self.add_video_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="Add",
            text_color="black",
            command=self.search_ytVideo,
        )
        self.add_video_button.grid(
            column=0, row=1,
            padx=5, pady=(0, 5),
            sticky="EW"
        )

        # Right Frame
        self.dir_path_entry = customtkinter.CTkEntry(
            master=self.right_frame,
            placeholder_text="Save Directory Path"
        )
        self.dir_path_entry.grid(
            column=0, row=0,
            columnspan=2,
            padx=5, pady=(5, 0),
            sticky="EW"
        )
        self.dir_path_entry.bind("<Button-3>", self.get_download_path)
        self.dir_path_entry.insert(0, Path.home()/"Music/Youtube Downloader")

        self.quality_option = customtkinter.CTkOptionMenu(
            master=self.right_frame,
            values=["High Quality - 720p", "Low Quality - 360p", "Audio Only"],
            text_color="black",
        )
        self.quality_option.grid(
            column=0, row=1,
            padx=5, pady=(5, 0),
            sticky="EW"
        )

        self.download_button = customtkinter.CTkButton(
            master=self.right_frame,
            text="Download",
            text_color="black",
            command=self.download_video
        )
        self.download_button.grid(
            column=1, row=1,
            padx=(0, 5), pady=(5, 0),
            sticky="EW"
        )

        self.download_progress_bar = customtkinter.CTkProgressBar(
            master=self.right_frame,
        )
        self.download_progress_bar.grid(
            column=0, row=2,
            columnspan=2,
            padx=5, pady=(5, 0),
            sticky="EW"
        )
        self.download_progress_bar.set(0)

    def get_download_path(self, event):
        dir_path = filedialog.askdirectory()
        if dir_path != "":
            self.dir_path_entry.delete(0, "end")
            self.dir_path_entry.insert(0, dir_path)

    def search_ytVideo(self):
        url = self.url_entry.get()
        if url != "":
            try:
                yt_video = YouTube(url, on_progress_callback=self.on_progress)
                self.url_entry.delete(0, "end")
                self.video_list_label[self.video_counter] = {
                    "title": yt_video.title,
                    "youtube": yt_video
                }
                self.add_widget(yt_video)
            except Exception as e:
                with open("log.log", "a") as file:
                    file.write(
                        f"{datetime.now().strftime('%H:%M:%S ->')} - {e}\n")
                self.url_entry.delete(0, "end")
                open_log_file = messagebox.askyesno(
                    "Error", "Url mancante o errato.\nAprire il file log?", icon="error")
                if open_log_file:
                    Popen("explorer log.log")

    def add_widget(self, yt_video: YouTube):
        self.videos_widget[self.video_counter] = customtkinter.CTkLabel(
            master=self.video_frame,
            text=yt_video.title,
            anchor="w",
        )
        self.videos_widget[self.video_counter].grid(
            column=0, row=self.video_counter,
            padx=0, pady=0,
            sticky="EW",
        )
        self.videos_widget[self.video_counter].bind(
            "<Button-3>",
            lambda event, i=self.video_counter, title=self.videos_widget[self.video_counter].cget("text"):
            self.change_file_name(event, i, title)
        )

        self.remove_video_widgets_button[self.video_counter] = customtkinter.CTkButton(
            master=self.video_frame,
            text="",
            image=self.trash_img,
            text_color="black",
            width=0,
            command=lambda i=self.video_counter: self.remove_entry(i)
        )
        self.remove_video_widgets_button[self.video_counter].grid(
            column=1, row=self.video_counter,
            padx=(5, 0), pady=(5, 0),
        )
        self.video_counter += 1

    def change_file_name(self, event, index, title):
        video_name = customtkinter.CTkInputDialog(
            title="New Video Name",
            text=title
        ).get_input()

        if (video_name is not None):
            self.videos_widget[index].configure(text=video_name)
            self.video_list_label[index]["title"] = video_name

    def remove_entry(self, index):
        self.videos_widget[index].destroy()
        self.videos_widget.pop(index)

        self.video_list_label.pop(index)

        self.remove_video_widgets_button[index].destroy()
        self.remove_video_widgets_button.pop(index)

    def download_thread(self):
        download_type = self.quality_option.get()
        directory = self.dir_path_entry.get()

        for i in range(self.video_counter):
            try:
                video = self.video_list_label[i]
                self.current_video_download = video
                filename = f"{video['title']}.mp{
                    '3' if download_type == 'Audio Only' else '4'}"
                for character in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]:
                    filename = filename.replace(character, "&")
                match download_type:
                    case "High Quality - 720p":
                        video["youtube"].streams.get_highest_resolution().download(
                            output_path=directory, filename=filename)
                    case "Low Quality - 360p":
                        video["youtube"].streams.get_lowest_resolution().download(
                            output_path=directory, filename=filename)
                    case "Audio Only":
                        video["youtube"].streams.filter(
                            only_audio=True).first().download(output_path=directory, filename=filename)

                print(f"{filename} scaricato")
                self.total_video_download += 1
            except Exception as e:
                print(e)

    def download_video(self):
        if len(self.video_list_label) == 0:
            return

        for widget in self.status_frame.winfo_children():
            widget.destroy()
        self.download_counter = 0

        for i in range(self.video_counter):
            try:
                self.download_video_list_label[self.download_counter] = customtkinter.CTkLabel(
                    master=self.status_frame,
                    anchor="w",
                )
                self.download_video_list_label[self.download_counter].grid(
                    column=0, row=self.download_counter,
                    padx=5, pady=(5, 0),
                    sticky="EW",
                )
                self.download_video_list_label[self.download_counter].configure(
                    text=self.video_list_label[i]["title"])

                self.download_status_list_label[self.download_counter] = customtkinter.CTkLabel(
                    master=self.status_frame,
                    anchor="w",
                )
                self.download_status_list_label[self.download_counter].grid(
                    column=1, row=self.download_counter,
                    padx=(0, 5), pady=(5, 0),
                    sticky="EW",
                )
                self.download_status_list_label[self.download_counter].configure(
                    text="0.0 %")

                self.download_counter += 1
            except Exception as e:
                print(e)

        self.download_button.configure(state="disabled")
        threading.Thread(
            target=self.download_thread
        ).start()

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        self.status = pct_completed
        self.download_progress_bar.set(pct_completed / 100)
        self.download_status_list_label[self.total_video_download].configure(
            text=f"{round(pct_completed, 2)} %")

        if int(pct_completed) == 100:
            self.download_status_list_label[self.total_video_download].configure(
                text="Completed")

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    App().start()
