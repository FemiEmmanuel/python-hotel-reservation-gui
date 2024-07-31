import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox
from utils.colors import *

class BaseManagement:
    def __init__(self, master, title):
        self.master = master
        self.title = title
        self.id_map = {}
        self.create_base_widgets()

    def create_base_widgets(self):
        self.master.grid_columnconfigure(0, weight=7)
        self.master.grid_columnconfigure(1, weight=3)
        self.master.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(self.master)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.create_search_frame()
        self.create_list_frame()

        self.right_frame = ctk.CTkFrame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=0)
        self.right_frame.grid_rowconfigure(2, weight=1)

        self.create_form_frame()

    def create_search_frame(self):
        search_frame = ctk.CTkFrame(self.left_frame)
        search_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text=f"Search {self.title.lower()}...")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.search_entry.bind("<Return>", lambda event: self.search_items())

        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_items, width=100, fg_color=SEARCH_COLOR)
        self.search_button.grid(row=0, column=1)

        self.refresh_button = ctk.CTkButton(search_frame, text="Refresh", command=self.refresh, width=100, fg_color=REFRESH_COLOR)
        self.refresh_button.grid(row=0, column=2)

    def create_list_frame(self):
        self.list_title = ctk.CTkLabel(self.left_frame, text=f"All {self.title}", font=("Arial", 16, "bold"))
        self.list_title.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))

        self.item_list = CTkListbox(self.left_frame, command=self.on_select)
        self.item_list.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    def create_form_frame(self):
        self.form_frame = ctk.CTkFrame(self.right_frame)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def on_select(self, event):
        # To be implemented in child classes
        pass

    def add_item(self):
        # To be implemented in child classes
        pass

    def update_item(self):
        # To be implemented in child classes
        pass

    def delete_item(self):
        # To be implemented in child classes
        pass

    def search_items(self):
        # To be implemented in child classes
        pass

    def load_items(self):
        # To be implemented in child classes
        pass

    def clear_fields(self):
        # To be implemented in child classes
        pass

    def refresh(self):
        self.load_items()
        self.clear_fields()
        self.list_title.configure(text=f"All {self.title}")

    def show_info(self, title, message):
        tkinter.messagebox.showinfo(title, message)

    def show_error(self, title, message):
        tkinter.messagebox.showerror(title, message)

    def show_warning(self, title, message):
        tkinter.messagebox.showwarning(title, message)

    def confirm(self, title, message):
        return tkinter.messagebox.askyesno(title, message)