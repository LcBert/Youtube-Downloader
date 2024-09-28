import customtkinter as ctk

import video_class


class Frame(ctk.CTkFrame):
    x = 0
    video_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(
            column=0, row=0,
            padx=0, pady=0,
            sticky="nsew"
        )
        self.grid_rowconfigure(1, weight=1)

        self.url_entry = ctk.CTkEntry(
            self,
            placeholder_text="URL"
        )
        self.url_entry.grid(
            column=0, row=0,
            padx=(5, 2), pady=(5, 5),
            sticky="ew"
        )

        self.url_button = ctk.CTkButton(
            self,
            text="+",
            width=25,
            font=("Arial", 20),
            command=lambda: self.add_link(self.url_entry.get())
        )
        self.url_button.grid(
            column=1, row=0,
            padx=(0, 5), pady=(5, 5)
        )

        self.video_list_frame = ctk.CTkScrollableFrame(self, width=0, height=0)
        self.video_list_frame.grid(
            column=0, row=1,
            columnspan=2,
            padx=(5, 5), pady=(5, 5),
            sticky="nsew"
        )

    def add_link(self, url):
        self.video_list.append(video_class.Video(url))

        ctk.CTkLabel(
            self.video_list_frame,
            text=self.video_list[self.x].yt_object.title
        ).grid(
            column=0, row=self.x,
            padx=0, pady=0
        )
        self.x += 1
