import customtkinter as ctk
import pytube

# Frames Import
import video_list_frame


class App(ctk.CTk):
    APP_NAME = "Youtube Downloader"
    WIDTH = "800"
    HEIGHT = "500"

    def __init__(self):
        super().__init__()

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(int(self.WIDTH), int(self.HEIGHT))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        video_list_frame.Frame(self)

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    App().start()
