import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox
from model.reservation import Reservation
from model.customer import Customer
from model.room import Room
from utils.colors import *
from tkcalendar import DateEntry
from datetime import datetime

class ReservationManagement:
    def __init__(self, master):
        self.master = master
        self.reservation_id_map = {}
        self.customer_id_map = {}
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
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search reservations...", width=200)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.search_entry.bind("<Return>", lambda event: self.search_reservations())

        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_reservations, width=100, fg_color=SEARCH_COLOR)
        self.search_button.grid(row=0, column=1)

        # Refresh button
        self.refresh_button = ctk.CTkButton(search_frame, text="Refresh", command=self.refresh, width=100, fg_color=REFRESH_COLOR)
        self.refresh_button.grid(row=0, column=2)

        self.list_title = ctk.CTkLabel(left_frame, text="All Reservations", font=("Arial", 16, "bold"))
        self.list_title.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))

        # Reservation list
        self.reservation_list = CTkListbox(left_frame, command=self.on_select)
        self.reservation_list.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Right frame
        self.right_frame = ctk.CTkFrame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid_rowconfigure(0, weight=1)  
        self.right_frame.grid_rowconfigure(1, weight=0) 
        self.right_frame.grid_rowconfigure(2, weight=1)

        # Variables
        self.customer_search_var = ctk.StringVar()
        self.customer_id_var = ctk.StringVar()
        self.room_search_var = ctk.StringVar()
        self.room_id_var = ctk.StringVar()
        self.check_in_var = ctk.StringVar()
        self.check_out_var = ctk.StringVar()
        self.total_cost_var = ctk.StringVar()

        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Entry fields
        ctk.CTkLabel(form_frame, text="Customer:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.customer_search_frame = ctk.CTkFrame(form_frame)
        self.customer_search_frame.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.customer_entry = ctk.CTkEntry(self.customer_search_frame, textvariable=self.customer_search_var)
        self.customer_entry.pack(side="left")
        self.customer_search_button = ctk.CTkButton(self.customer_search_frame, text="Search", command=self.search_customer, fg_color=SEARCH_COLOR)
        self.customer_search_button.pack(side="left")
        
        self.customer_listbox = CTkListbox(form_frame, command=self.on_customer_select)
        self.customer_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.customer_listbox.grid_remove()

        ctk.CTkLabel(form_frame, text="Room:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.room_search_frame = ctk.CTkFrame(form_frame)
        self.room_search_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.room_entry = ctk.CTkEntry(self.room_search_frame, textvariable=self.room_search_var)
        self.room_entry.pack(side="left")
        self.room_search_button = ctk.CTkButton(self.room_search_frame, text="Search", command=self.search_room, fg_color=SEARCH_COLOR)
        self.room_search_button.pack(side="left")
        
        self.room_listbox = CTkListbox(form_frame, command=self.on_room_select)
        self.room_listbox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.room_listbox.grid_remove()

        ctk.CTkLabel(form_frame, text="Check-in Date:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.check_in_entry = DateEntry(form_frame, textvariable=self.check_in_var, date_pattern='yyyy-mm-dd')
        self.check_in_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.check_in_entry.bind("<<DateEntrySelected>>", self.calculate_total_cost)

        ctk.CTkLabel(form_frame, text="Check-out Date:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.check_out_entry = DateEntry(form_frame, textvariable=self.check_out_var, date_pattern='yyyy-mm-dd')
        self.check_out_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        self.check_out_entry.bind("<<DateEntrySelected>>", self.calculate_total_cost)

        ctk.CTkLabel(form_frame, text="Total Cost:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(form_frame, textvariable=self.total_cost_var, state="readonly").grid(row=6, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.button_frame = ctk.CTkFrame(form_frame)
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.check_availability_button = ctk.CTkButton(self.button_frame, text="Check Availability", command=self.check_availability, fg_color=INVOICE_COLOR)
        self.check_availability_button.pack(side="left", padx=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add Reservation", command=self.add_reservation, state="disabled")
        self.add_button.pack(side="left", padx=10)

        self.update_button = ctk.CTkButton(form_frame, text="Update Reservation", command=self.update_reservation, fg_color=UPDATE_COLOR)
        self.delete_button = ctk.CTkButton(form_frame, text="Delete Reservation", command=self.delete_reservation, fg_color=DELETE_COLOR)

        self.load_reservations()

    def load_reservations(self):
        reservations = Reservation.get_all_reservation_details()
        self.reservation_list.delete(0, "end")
        self.reservation_id_map.clear()
        for index, reservation in enumerate(reservations):
            display_text = f"{reservation['customer_name']} - Room {reservation['room_number']} ({reservation['room_type']})"
            self.reservation_list.insert("end", display_text)
            self.reservation_id_map[index] = reservation['reservation_id']

    def on_select(self, event):
        selection = self.reservation_list.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.reservation_id_map.get(index)
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
                tkinter.messagebox.showinfo("Availability", "The room is available for the selected dates.")
                self.add_button.configure(state="normal")
            else:
                tkinter.messagebox.showwarning("Availability", "The room is not available for the selected dates.")
                self.add_button.configure(state="disabled")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", str(e))

    def add_reservation(self):
        try:
            Reservation.create(
                int(self.customer_id_var.get()),
                int(self.room_id_var.get()),
                self.check_in_var.get(),
                self.check_out_var.get(),
                float(self.total_cost_var.get().replace('$', ''))
            )
            self.refresh()
            tkinter.messagebox.showinfo("Success", "Reservation added successfully")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", str(e))

    def update_reservation(self):
        selection = self.reservation_list.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.reservation_id_map.get(index)
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
                    tkinter.messagebox.showinfo("Success", "Reservation updated successfully")
                except ValueError as e:
                    tkinter.messagebox.showerror("Error", str(e))
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a reservation to update")

    def delete_reservation(self):
        selection = self.reservation_list.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.reservation_id_map.get(index)
            if reservation_id:
                if tkinter.messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?"):
                    Reservation.delete(reservation_id)
                    self.refresh()
                    tkinter.messagebox.showinfo("Success", "Reservation deleted successfully")
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a reservation to delete")

    def search_reservations(self):
        criteria = self.search_var.get()
        reservations = Reservation.search(criteria)
        self.reservation_list.delete(0, "end")
        self.reservation_id_map.clear()
        for index, reservation in enumerate(reservations):
            display_text = f"{reservation['customer_name']} - Room {reservation['room_number']} ({reservation['room_type']})"
            self.reservation_list.insert("end", display_text)
            self.reservation_id_map[index] = reservation['reservation_id']
        
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


    def refresh(self):
        self.load_reservations()
        self.clear_fields()
        self.list_title.configure(text="All Reservations")

