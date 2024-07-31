import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox

from model.room import Room, RoomType
from utils.colors import *
from gui.base_management import BaseManagement

class RoomManagement(BaseManagement):
    def __init__(self, master):
        super().__init__(master, "Rooms")
        self.create_room_specific_widgets()

    def create_room_specific_widgets(self):
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
        self.add_button = ctk.CTkButton(form_frame, text="Add Room", command=self.add_item)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.update_button = ctk.CTkButton(form_frame, text="Update Room", command=self.update_item, fg_color=UPDATE_COLOR)
        self.delete_button = ctk.CTkButton(form_frame, text="Delete Room", command=self.delete_item, fg_color=DELETE_COLOR)

        self.load_items()

    def on_room_type_change(self, choice):
        room_type = next((rt for rt in RoomType.get_all() if rt.name == choice), None)
        if room_type:
            self.price_var.set(f"${room_type.price:.2f}")
            self.features_var.set(room_type.features)

    def load_items(self):
        rooms = Room.get_all()
        self.item_list.delete(0, "end")
        self.id_map.clear()
        for index, room in enumerate(rooms):
            self.item_list.insert("end", f"Room {room.room_id}: {room.room_type.name} - {room.status}")
            self.id_map[index] = room.room_id

    def on_select(self, event):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            room_id = self.id_map.get(index)
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

    def add_item(self):
        try:
            room_type = next((rt for rt in RoomType.get_all() if rt.name == self.room_type_var.get()), None)
            if room_type:
                existing_rooms = Room.get_all()
                highest_room_number = max([int(room.room_number[1:]) for room in existing_rooms], default=0)
                next_room_number = highest_room_number + 1
                new_room_number = f"R{next_room_number:03d}"

                Room.create(
                    room_type_id=room_type.room_types_id,
                    room_number=new_room_number,
                    status=self.status_var.get(),
                    location=self.location_var.get()
                )
                self.refresh()
                self.handle_success("added")
            else:
                self.handle_error("invalid room type selected", e)
        except ValueError as e:
            self.handle_error("adding room", e)

    def update_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            room_id = self.id_map.get(index)
            if room_id:
                try:
                    Room.update(
                        room_id,
                        status=self.status_var.get(),
                    )
                    self.refresh()
                    self.handle_success("updated")
                except ValueError as e:
                    self.handle_error("updating room", e)
        else:
            self.handle_not_selected_error()

    def delete_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            room_id = self.id_map.get(index)
            if room_id:
                if self.confirm("Confirm", "Are you sure you want to delete this room?"):
                    Room.delete(room_id)
                    self.refresh()
                    self.handle_success("deleted")
        else:
            self.handle_not_selected_error()

    def search_items(self):
        criteria = self.search_var.get()
        rooms = Room.search(criteria)
        self.item_list.delete(0, "end")
        self.id_map.clear()
        for index, room in enumerate(rooms):
            self.item_list.insert("end", f"Room {room.room_id}: {room.room_type.name} - {room.status}")
            self.id_map[index] = room.room_id
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
        self.load_items()
        self.clear_fields()
        self.list_title.configure(text="All Rooms")