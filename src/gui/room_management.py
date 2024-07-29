import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox

from model.room import Room, RoomType
from utils.colors import *

class RoomManagement:
    def __init__(self, master):
        self.master = master
        self.room_id_map = {}
        self.create_widgets()

    def create_widgets(self):

        self.master.grid_columnconfigure(0, weight=7)
        self.master.grid_columnconfigure(1, weight=3)
        self.master.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self.master)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.grid_rowconfigure(0, weight=0) 
        left_frame.grid_rowconfigure(1, weight=0) 
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

         # Search bar frame
        search_frame = ctk.CTkFrame(left_frame)
        search_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search rooms...")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_rooms, width=100, fg_color=SEARCH_COLOR)
        self.search_button.grid(row=0, column=1)

         # Refresh button
        self.refresh_button = ctk.CTkButton(search_frame, text="Refresh", command=self.refresh, width=100, fg_color=REFRESH_COLOR)
        self.refresh_button.grid(row=0, column=2)

        self.list_title = ctk.CTkLabel(left_frame, text="All Rooms", font=("Arial", 16, "bold"))
        self.list_title.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))

        # Room list
        self.room_list = CTkListbox(left_frame, command=self.on_select)
        self.room_list.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Right frame (40% of space)
        self.right_frame = ctk.CTkFrame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid_rowconfigure(0, weight=1)  
        self.right_frame.grid_rowconfigure(1, weight=0) 
        self.right_frame.grid_rowconfigure(2, weight=1)

        # Variables
        self.room_type_var = ctk.StringVar()
        self.price_var = ctk.StringVar()
        self.status_var = ctk.StringVar()
        self.features_var = ctk.StringVar()
        self.location_var = ctk.StringVar()

        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Room Type Dropdown
        ctk.CTkLabel(form_frame, text="Room Type:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.room_type_var.set("Select Room-type")
        self.room_types = [rt.name for rt in RoomType.get_all()]
        self.room_type_dropdown = ctk.CTkOptionMenu(
            form_frame, variable=self.room_type_var,
            values=self.room_types, command=self.on_room_type_change
        )
        self.room_type_dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=5)        

        # Price (read-only)
        ctk.CTkLabel(form_frame, text="Price:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.price_entry = ctk.CTkEntry(form_frame, textvariable=self.price_var, state="readonly")
        self.price_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Status Dropdown
        ctk.CTkLabel(form_frame, text="Status:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.status_var.set("Select Status")
        self.status_dropdown = ctk.CTkOptionMenu(
            form_frame, variable=self.status_var,
            values=["Available", "Occupied", "Maintenance"]
        )
        self.status_dropdown.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Features (read-only)
        ctk.CTkLabel(form_frame, text="Features:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.features_entry = ctk.CTkEntry(form_frame, textvariable=self.features_var, state="readonly")
        self.features_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Location Dropdown
        ctk.CTkLabel(form_frame, text="Location:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.location_var.set("Select Location")
        self.location_dropdown = ctk.CTkOptionMenu(
            form_frame, variable=self.location_var,
            values=["North Wing", "South Wing", "East Wing", "West Wing", "Penthouse"]
        )
        self.location_dropdown.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.add_button = ctk.CTkButton(form_frame, text="Add Room", command=self.add_room)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.update_button = ctk.CTkButton(form_frame, text="Update Room", command=self.update_room, fg_color=UPDATE_COLOR)
        self.delete_button = ctk.CTkButton(form_frame, text="Delete Room", command=self.delete_room, fg_color=DELETE_COLOR)

        # Load rooms
        self.load_rooms()

    def on_room_type_change(self, choice):
        room_type = next((rt for rt in RoomType.get_all() if rt.name == choice), None)
        if room_type:
            self.price_var.set(f"${room_type.price:.2f}")
            self.features_var.set(room_type.features)

    def load_rooms(self):
        rooms = Room.get_all()
        self.room_list.delete(0, "end")
        self.room_id_map.clear()
        for index, room in enumerate(rooms):
            self.room_list.insert("end", f"Room {room.room_id}: {room.room_type.name} - {room.status}")
            self.room_id_map[index] = room.room_id
    

    def on_select(self, event):
        selection = self.room_list.curselection()
        if selection is not None:
            index = selection
            room_id = self.room_id_map.get(index)
            if room_id:
                room = Room.get(room_id)
                self.room_type_var.set(room.room_type.name)
                self.price_var.set(f"${room.room_type.price:.2f}")
                self.status_var.set(room.status)
                self.features_var.set(room.room_type.features)
                self.location_var.set(room.location)

                self.room_type_dropdown.configure(state="readonly")
                self.location_dropdown.configure(state="readonly")

                self.add_button.grid_forget()
                self.update_button.grid(row=6, column=0, columnspan=2, pady=10)
                self.delete_button.grid(row=7, column=0, columnspan=2, pady=10)
        else:
            self.update_button.grid_forget()
            self.delete_button.grid_forget()

    def add_room(self):
        try:
            room_type = next((rt for rt in RoomType.get_all() if rt.name == self.room_type_var.get()), None)
            if room_type:
                # Get the highest room number currently in use
                existing_rooms = Room.get_all()
                highest_room_number = max([int(room.room_number[1:]) for room in existing_rooms], default=0)

                # Generate the next room number
                next_room_number = highest_room_number + 1
                new_room_number = f"R{next_room_number:03d}"

                Room.create(
                    room_type_id=room_type.room_types_id,
                    room_number=new_room_number,
                    status=self.status_var.get(),
                    location=self.location_var.get()
                )
                self.refresh()
                tkinter.messagebox.showinfo("Success", "Room added successfully")
            else:
                tkinter.messagebox.showerror("Error", "Invalid room type selected")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", str(e))


    def update_room(self):
        selection = self.room_list.curselection()
        if selection is not None:
            index = selection
            room_id = self.room_id_map.get(index)
            if room_id:
                try:
                    Room.update(
                        room_id,
                        status=self.status_var.get(),
                    )
                    self.refresh()
                    tkinter.messagebox.showinfo("Success", "Room updated successfully")
                except ValueError as e:
                    tkinter.messagebox.showerror("Error", str(e))
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a room to update")

    def delete_room(self):
        selection = self.room_list.curselection()
        if selection is not None:
            index = selection
            room_id = self.room_id_map.get(index)
            if room_id:
                if tkinter.messagebox.askyesno("Confirm", "Are you sure you want to delete this room?"):
                    Room.delete(room_id)
                    self.refresh()
                    tkinter.messagebox.showinfo("Success", "Room deleted successfully")
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a room to delete")

    def search_rooms(self):
        criteria = self.search_var.get()
        rooms = Room.search(criteria)
        self.room_list.delete(0, "end")
        self.room_id_map.clear()
        for index, room in enumerate(rooms):
            self.room_list.insert("end", f"Room {room.room_id}: {room.room_type.name} - {room.status}")
            self.room_id_map[index] = room.room_id
        self.search_var.set("")

        if criteria:
            self.list_title.configure(text=f"Search Results for '{criteria}'")
        else:
            self.list_title.configure(text="All Rooms")


    def clear_fields(self):
        self.room_type_var.set("")
        self.price_var.set("")
        self.status_var.set("")
        self.features_var.set("")
        self.location_var.set("")

        self.update_button.grid_forget()
        self.delete_button.grid_forget()
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def refresh(self):
        self.load_rooms()
        self.clear_fields()
        self.list_title.configure(text="All Rooms")
