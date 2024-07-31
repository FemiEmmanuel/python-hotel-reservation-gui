import customtkinter as ctk
from CTkListbox import *
from tkcalendar import DateEntry
from datetime import datetime

from gui.base_management import BaseManagement
from model.reservation import Reservation
from model.customer import Customer
from model.room import Room
from utils.colors import *


class ReservationManagement(BaseManagement):
    def __init__(self, master):
        super().__init__(master, "Reservations")
        self.customer_id_map = {}
        self.room_id_map = {}
        self.create_reservation_specific_widgets()

    def create_reservation_specific_widgets(self):
        # Variables
        self.customer_search_var = ctk.StringVar()
        self.customer_id_var = ctk.StringVar()
        self.room_search_var = ctk.StringVar()
        self.room_id_var = ctk.StringVar()
        self.check_in_var = ctk.StringVar()
        self.check_out_var = ctk.StringVar()
        self.total_cost_var = ctk.StringVar()

        # Customer fields
        ctk.CTkLabel(self.form_frame, text="Customer:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.customer_search_frame = ctk.CTkFrame(self.form_frame)
        self.customer_search_frame.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.customer_entry = ctk.CTkEntry(self.customer_search_frame, textvariable=self.customer_search_var)
        self.customer_entry.pack(side="left")
        self.customer_search_button = ctk.CTkButton(self.customer_search_frame, text="Search", command=self.search_customer, fg_color=SEARCH_COLOR)
        self.customer_search_button.pack(side="left")
        
        self.customer_listbox = CTkListbox(self.form_frame, command=self.on_customer_select)
        self.customer_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.customer_listbox.grid_remove()

        # Room fields
        ctk.CTkLabel(self.form_frame, text="Room:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.room_search_frame = ctk.CTkFrame(self.form_frame)
        self.room_search_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.room_entry = ctk.CTkEntry(self.room_search_frame, textvariable=self.room_search_var)
        self.room_entry.pack(side="left")
        self.room_search_button = ctk.CTkButton(self.room_search_frame, text="Search", command=self.search_room, fg_color=SEARCH_COLOR)
        self.room_search_button.pack(side="left")
        
        self.room_listbox = CTkListbox(self.form_frame, command=self.on_room_select)
        self.room_listbox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.room_listbox.grid_remove()

        # Date fields
        ctk.CTkLabel(self.form_frame, text="Check-in Date:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.check_in_entry = DateEntry(self.form_frame, textvariable=self.check_in_var, date_pattern='yyyy-mm-dd')
        self.check_in_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.check_in_entry.bind("<<DateEntrySelected>>", self.calculate_total_cost)

        ctk.CTkLabel(self.form_frame, text="Check-out Date:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.check_out_entry = DateEntry(self.form_frame, textvariable=self.check_out_var, date_pattern='yyyy-mm-dd')
        self.check_out_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        self.check_out_entry.bind("<<DateEntrySelected>>", self.calculate_total_cost)

        ctk.CTkLabel(self.form_frame, text="Total Cost:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(self.form_frame, textvariable=self.total_cost_var, state="readonly").grid(row=6, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.check_availability_button = ctk.CTkButton(self.button_frame, text="Check Availability", command=self.check_availability, fg_color=INVOICE_COLOR)
        self.check_availability_button.pack(side="left", padx=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add Reservation", command=self.add_item, state="disabled")
        self.add_button.pack(side="left", padx=10)

        self.update_button = ctk.CTkButton(self.form_frame, text="Update Reservation", command=self.update_item, fg_color=UPDATE_COLOR)
        self.delete_button = ctk.CTkButton(self.form_frame, text="Delete Reservation", command=self.delete_item, fg_color=DELETE_COLOR)

        self.load_items()

    def load_items(self):
        reservations = Reservation.get_all_reservation_details()
        self.item_list.delete(0, "end")
        self.id_map.clear()
        for index, reservation in enumerate(reservations):
            display_text = f"{reservation['customer_name']} - Room {reservation['room_number']} ({reservation['room_type']})"
            self.item_list.insert("end", display_text)
            self.id_map[index] = reservation['reservation_id']

    def on_select(self, event):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.id_map.get(index)
            if reservation_id:
                reservation = Reservation.get_reservation_details(reservation_id)
                self.customer_search_var.set(reservation['customer_name'])
                self.customer_id_var.set(str(reservation['customer_id']))
                self.room_search_var.set(reservation['room_number'])
                self.room_id_var.set(str(reservation['room_id']))
                self.check_in_var.set(reservation['check_in_date'])
                self.check_out_var.set(reservation['check_out_date'])
                self.total_cost_var.set(f"${reservation['total_cost']:.2f}")

                self.button_frame.grid_remove()
                self.update_button.grid(row=8, column=0, columnspan=2, pady=10)
                self.delete_button.grid(row=9, column=0, columnspan=2, pady=10)
                self.customer_entry.configure(state="readonly")
                self.customer_search_button.pack_forget()
                self.customer_listbox.grid_remove()
                self.room_entry.configure(state="readonly")
                self.room_search_button.pack_forget()
                self.room_listbox.grid_remove()
        else:
            self.update_button.grid_forget()
            self.delete_button.grid_forget()
            self.customer_entry.configure(state="normal")
            self.customer_search_button.pack(side="left")
            self.room_entry.configure(state="normal")
            self.room_search_button.pack(side="left")

    def search_customer(self):
        search_term = self.customer_search_var.get()
        customers = Customer.search(search_term)
        self.customer_listbox.delete(0, "end")
        self.customer_id_map.clear()
        for index, customer in enumerate(customers):
            self.customer_listbox.insert("end", f"{customer.name}")
            self.customer_id_map[index] = customer.customer_id
        self.customer_listbox.grid()

    def on_customer_select(self, event):
        selection = self.customer_listbox.curselection()
        if selection is not None:
            index = selection
            customer_id = self.customer_id_map.get(index)
            if customer_id:
                customer = Customer.get(customer_id)
                self.customer_id_var.set(str(customer_id))
                self.customer_search_var.set(customer.name)
                self.customer_entry.configure(state="readonly")
                self.customer_search_button.pack_forget()
                self.customer_listbox.grid_remove()

    def search_room(self):
        search_term = self.room_search_var.get()
        rooms = Room.search(search_term)
        self.room_listbox.delete(0, "end")
        self.room_id_map.clear()
        for index, room in enumerate(rooms):
            self.room_listbox.insert("end", f"{room.room_number} - {room.room_type.name}")
            self.room_id_map[index] = room.room_id
        self.room_listbox.grid()

    def on_room_select(self, event):
        selection = self.room_listbox.curselection()
        if selection is not None:
            index = selection
            room_id = self.room_id_map.get(index)
            if room_id:
                room = Room.get(room_id)
                self.room_id_var.set(str(room_id))
                self.room_search_var.set(f"{room.room_number} - {room.room_type.name}")
                self.room_entry.configure(state="readonly")
                self.room_search_button.pack_forget()
                self.room_listbox.grid_remove()
                self.calculate_total_cost()

    def calculate_total_cost(self, event=None):
        if self.room_id_var.get() and self.check_in_var.get() and self.check_out_var.get():
            room_id = int(self.room_id_var.get())
            room = Room.get(room_id)
            check_in = datetime.strptime(self.check_in_var.get(), '%Y-%m-%d')
            check_out = datetime.strptime(self.check_out_var.get(), '%Y-%m-%d')
            days = (check_out - check_in).days
            if room:
                total_cost = room.room_type.price * days
            self.total_cost_var.set(f"${total_cost:.2f}")

    def check_availability(self):
        try:
            room_id = int(self.room_id_var.get())
            check_in = self.check_in_var.get()
            check_out = self.check_out_var.get()
            
            overlapping_reservations = Reservation.check_overlapping_reservations(room_id, check_in, check_out)
            
            if not overlapping_reservations:
                self.show_info("Availability", "The room is available for the selected dates.")
                self.add_button.configure(state="normal")
            else:
                self.show_warning("Availability", "The room is not available for the selected dates.")
                self.add_button.configure(state="disabled")
        except ValueError as e:
            self.show_error("Error", str(e))

    def add_item(self):
        try:
            Reservation.create(
                int(self.customer_id_var.get()),
                int(self.room_id_var.get()),
                self.check_in_var.get(),
                self.check_out_var.get(),
                float(self.total_cost_var.get().replace('$', ''))
            )
            self.refresh()
            self.handle_success("added")
        except ValueError as e:
            self.handle_error("adding reservation", e)

    def update_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.id_map.get(index)
            if reservation_id:
                try:
                    Reservation.update(
                        reservation_id,
                        int(self.customer_id_var.get()),
                        int(self.room_id_var.get()),
                        self.check_in_var.get(),
                        self.check_out_var.get(),
                        float(self.total_cost_var.get().replace('$', ''))
                    )
                    self.refresh()
                    self.handle_success("updated")
                except ValueError as e:
                    self.handle_error("updating reservation", e)
        else:
            self.handle_not_selected_error()

    def delete_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.id_map.get(index)
            if reservation_id:
                if self.confirm("Confirm", "Are you sure you want to delete this reservation?"):
                    Reservation.delete(reservation_id)
                    self.refresh()
                    self.handle_success("deleted")
        else:
            self.handle_not_selected_error()

    def search_items(self):
        criteria = self.search_var.get()
        reservations = Reservation.search(criteria)
        self.item_list.delete(0, "end")
        self.id_map.clear()
        for index, reservation in enumerate(reservations):
            display_text = f"{reservation['customer_name']} - Room {reservation['room_number']} ({reservation['room_type']})"
            self.item_list.insert("end", display_text)
            self.id_map[index] = reservation['reservation_id']
        
        if criteria:
            self.list_title.configure(text=f"Search Results for '{criteria}'")
        else:
            self.list_title.configure(text="All Reservations")

    def clear_fields(self):
        self.customer_search_var.set("")
        self.customer_id_var.set("")
        self.room_search_var.set("")
        self.room_id_var.set("")
        self.check_in_var.set("")
        self.check_out_var.set("")
        self.total_cost_var.set("")
        self.customer_listbox.delete(0, "end")
        self.room_listbox.delete(0, "end")

        self.update_button.grid_forget()
        self.delete_button.grid_forget()
        
        self.customer_entry.configure(state="normal") 
        self.customer_search_button.pack(side="left")
        self.customer_listbox.grid_remove()

        self.room_entry.configure(state="normal")  
        self.room_search_button.pack(side="left") 
        self.room_listbox.grid_remove()

        self.customer_id_map.clear()
        self.room_id_map.clear()

        self.button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        self.add_button.configure(state="disabled")

    def refresh(self):
        super().refresh()
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        self.add_button.configure(state="disabled")

    def update_list_title(self, criteria=""):
        if criteria:
            self.list_title.configure(text=f"Search Results for '{criteria}'")
        else:
            self.list_title.configure(text="All Reservations")