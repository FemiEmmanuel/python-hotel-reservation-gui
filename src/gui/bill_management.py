import os
from datetime import date, datetime
import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox
from tkcalendar import DateEntry

from model.bill import Bill
from model.customer import Customer
from model.reservation import Reservation
from model.service import Service
from gui.base_management import BaseManagement
from utils.colors import *

class BillManagement(BaseManagement):
    def __init__(self, master):
        super().__init__(master, "Bills")
        self.reservation_id_map = {}
        self.create_bill_specific_widgets()

    def create_bill_specific_widgets(self):
        # Variables
        self.reservation_search_var = ctk.StringVar()
        self.reservation_id_var = ctk.StringVar()
        self.amount_var = ctk.StringVar()
        self.date_var = ctk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        self.services_vars = []

        # Entry fields
        ctk.CTkLabel(self.form_frame, text="Search Reservation:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.reservation_search_frame = ctk.CTkFrame(self.form_frame)
        self.reservation_search_frame.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(self.reservation_search_frame, 
                text="Enter customer name or room type:", 
                text_color="gray").pack(side="top", padx=(0, 5), anchor="w")
        
        entry_button_frame = ctk.CTkFrame(self.reservation_search_frame)
        entry_button_frame.pack(side="top", fill="x")
        
        self.reservation_entry = ctk.CTkEntry(entry_button_frame, textvariable=self.reservation_search_var)
        self.reservation_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.reservation_search_button = ctk.CTkButton(entry_button_frame, text="Search", command=self.search_reservation, fg_color=SEARCH_COLOR)
        self.reservation_search_button.pack(side="right")

        self.reservation_listbox = CTkListbox(self.form_frame, command=self.on_reservation_select)
        self.reservation_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.reservation_listbox.grid_remove()

        ctk.CTkLabel(self.form_frame, text="Services:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.services_frame = ctk.CTkFrame(self.form_frame)
        self.services_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.load_services()

        ctk.CTkLabel(self.form_frame, text="Date:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.date_entry = DateEntry(self.form_frame, textvariable=self.date_var, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text="Amount:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(self.form_frame, textvariable=self.amount_var).grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add Bill", command=self.add_item)
        self.add_button.pack(side="left", padx=10)

        self.update_button = ctk.CTkButton(self.form_frame, text="Update Bill", command=self.update_item, fg_color=UPDATE_COLOR)
        self.delete_button = ctk.CTkButton(self.form_frame, text="Delete Bill", command=self.delete_item, fg_color=DELETE_COLOR)
        self.generate_invoice_button = ctk.CTkButton(self.form_frame, text="Generate Invoice", command=self.generate_invoice, fg_color=INVOICE_COLOR)
        
        self.load_items()

    def load_services(self):
        services = Service.get_all()
        for service in services:
            var = ctk.BooleanVar()
            self.services_vars.append((service.service_id, var))
            ctk.CTkCheckBox(self.services_frame, text=service.name, variable=var, command=self.update_amount).pack(anchor="w")

    def search_reservation(self):
        search_term = self.reservation_search_var.get()
        reservations = Reservation.search(search_term)
        self.reservation_listbox.delete(0, "end")
        self.reservation_id_map.clear()
        for index, reservation in enumerate(reservations):
            display_text = f"Reservation {reservation['reservation_id']}: {reservation['customer_name']} - Room {reservation['room_number']}"
            self.reservation_listbox.insert("end", display_text)
            self.reservation_id_map[index] = reservation['reservation_id']
        self.reservation_listbox.grid()

    def on_reservation_select(self, event):
        selection = self.reservation_listbox.curselection()
        if selection is not None:
            index = selection
            reservation_id = self.reservation_id_map.get(index)
            if reservation_id:
                reservation = Reservation.get_reservation_details(reservation_id)
                if reservation:
                    self.reservation_id_var.set(str(reservation_id))
                    self.amount_var.set(f"${reservation['total_cost']:.2f}")
                    self.reservation_entry.configure(state="readonly")
                    self.reservation_search_button.pack_forget()
                    self.reservation_listbox.grid_remove()
                    self.update_amount()

                    display_text = f"Reservation {reservation['reservation_id']}: {reservation['customer_name']}"
                    self.reservation_search_var.set(display_text)

    def update_amount(self):
        if self.reservation_id_var.get():
            reservation = Reservation.get(int(self.reservation_id_var.get()))
            total_amount = reservation.total_cost
            for service_id, var in self.services_vars:
                if var.get():
                    service = Service.get(service_id)
                    total_amount += service.price
            self.amount_var.set(f"${total_amount:.2f}")

    def load_items(self):
        bills = Bill.get_all_bill_details()
        self.item_list.delete(0, "end")
        self.id_map.clear()

        for index, bill in enumerate(bills):
            bill_description = f"💲 Bill #{bill['bill_id']}: Reservation #{bill['reservation_id']} - ${bill['amount']:.2f} (Customer: {bill['customer_name']})"
            self.item_list.insert("end", bill_description)
            self.id_map[index] = bill['bill_id']

    def on_select(self, event):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.id_map.get(index)
            if bill_id:
                bill_details = Bill.get_bill_details(bill_id)
                if bill_details:
                    self.reservation_id_var.set(str(bill_details['reservation_id']))
                    self.amount_var.set(f"${bill_details['amount']:.2f}")
                    self.date_var.set(bill_details['date'])
                
                    for service_id, var in self.services_vars:
                        var.set(any(service['service_id'] == service_id for service in bill_details['services']))
                
                    self.button_frame.grid_remove()
                    self.update_button.grid(row=6, column=0, columnspan=2, pady=10)
                    self.delete_button.grid(row=7, column=0, columnspan=2, pady=10)
                    self.generate_invoice_button.grid(row=8, column=0, columnspan=2, pady=10)
                
                    self.reservation_search_var.set(f"{bill_details['reservation_id']}: {bill_details['customer_name']} - {bill_details['check_in_date']} to {bill_details['check_out_date']}")
                    self.reservation_entry.configure(state="readonly")
                    self.reservation_search_button.pack_forget()
        else:
            self.clear_fields()

    def add_item(self):
        reservation_id = self.reservation_id_var.get()
        amount = self.amount_var.get()
        date = self.date_var.get()

        if not all([reservation_id, amount, date]):
            self.handle_validation_error("Reservation field required.")
            return
        
        try:
            selected_services = [service_id for service_id, var in self.services_vars if var.get()]
            Bill.create(
                int(reservation_id),
                float(amount.replace('$', '')),
                date,
                selected_services
            )
            self.refresh()
            self.handle_success("added")
        except ValueError as e:
            self.handle_error("adding bill", e)

    def update_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.id_map.get(index)
            if bill_id:
                reservation_id = self.reservation_id_var.get()
                amount = self.amount_var.get()
                date = self.date_var.get()

                if not all([reservation_id, amount, date]):
                    self.handle_validation_error("Reservation field required.")
                    return
                
                try:
                    selected_services = [service_id for service_id, var in self.services_vars if var.get()]
                    Bill.update(
                        bill_id,
                        int(reservation_id),
                        float(amount.replace('$', '')),
                        date,
                        selected_services
                    )
                    self.refresh()
                    self.handle_success("updated")
                except ValueError as e:
                    self.handle_error("updating bill", e)
        else:
           self.handle_not_selected_error()

    def delete_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.id_map.get(index)
            if bill_id:
                if self.confirm("Confirm", "Are you sure you want to delete this bill?"):
                    try:
                        Bill.delete(bill_id)
                        self.refresh()
                        self.handle_success("deleted")
                    except ValueError as e:
                        self.handle_error("deleting bill", e)
        else:
            self.handle_not_selected_error()

    def search_items(self):
        criteria = self.search_var.get()
        bills = Bill.search(criteria)
        self.item_list.delete(0, "end")
        for bill in bills:
            reservation = Reservation.get(bill.reservation_id)
            self.item_list.insert("end", f"Bill {bill.bill_id}: Reservation {reservation.reservation_id} - ${bill.amount}")
        self.search_var.set("")

        if criteria:
            self.list_title.configure(text=f"Search Results for '{criteria}'")
        else:
            self.list_title.configure(text="All Bills")

    def clear_fields(self):
        self.reservation_search_var.set("")
        self.reservation_id_var.set("")
        self.amount_var.set("")
        self.date_var.set(date.today().strftime('%Y-%m-%d'))
        for _, var in self.services_vars:
            var.set(False)
        self.reservation_listbox.delete(0, "end")
        self.reservation_entry.configure(state="normal")
        self.reservation_search_button.pack(side="left")
        self.update_button.grid_forget()
        self.delete_button.grid_forget()
        self.generate_invoice_button.grid_forget()
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=10)

    def generate_invoice(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.id_map.get(index)
            if bill_id:
                bill_details = Bill.get_bill_details(bill_id)
            
                if bill_details:
                    invoice_text = f"Invoice for Bill {bill_details['bill_id']}\n\n"
                    invoice_text += f"Reservation ID: {bill_details['reservation_id']}\n"
                    invoice_text += f"Customer: {bill_details['customer_name']}\n"
                    invoice_text += f"Check-in Date: {bill_details['check_in_date']}\n"
                    invoice_text += f"Check-out Date: {bill_details['check_out_date']}\n"
                    invoice_text += f"Date: {bill_details['date']}\n"
                    invoice_text += f"Amount: ${bill_details['amount']}\n\n"
                    invoice_text += "Services:\n"
                    
                    for service in bill_details['services']:
                        invoice_text += f"- {service['name']}: ${service['price']}\n"
                    
                    invoice_window = ctk.CTkToplevel(self.master)
                    invoice_window.title(f"Invoice for Bill {bill_details['bill_id']}")
                    invoice_window.geometry("400x300")
                    
                    invoice_text_widget = ctk.CTkTextbox(invoice_window, width=380, height=250)
                    invoice_text_widget.pack(padx=10, pady=10)
                    invoice_text_widget.insert("1.0", invoice_text)
                    invoice_text_widget.configure(state="disabled")
                    
                    save_button = ctk.CTkButton(invoice_window, text="Save Invoice", command=lambda: self.save_invoice(invoice_text, bill_details['bill_id']))
                    save_button.pack(pady=5)
                else:
                    self.show_warning("Error", "Bill details not found")
        else:
            self.show_warning("Warning", "Please select a bill to generate an invoice")

    def save_invoice(self, invoice_text, bill_id):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        invoices_dir = os.path.join(src_dir, 'invoices')
        
        if not os.path.exists(invoices_dir):
            os.makedirs(invoices_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"invoice_bill_{bill_id}_{timestamp}.txt"
        full_path = os.path.join(invoices_dir, filename)

        with open(full_path, 'w') as file:
            file.write(invoice_text)

        self.show_info("Success", f"Invoice saved as {full_path}")