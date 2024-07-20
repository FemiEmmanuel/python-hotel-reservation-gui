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

class BillManagement:
    def __init__(self, master):
        self.master = master
        self.bill_id_map = {}
        self.reservation_id_map = {}
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
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search bills...")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.search_entry.bind("<Return>", lambda event: self.search_customers())

        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_bills, width=100)
        self.search_button.grid(row=0, column=1)

        # Refresh button
        self.refresh_button = ctk.CTkButton(search_frame, text="Refresh", command=self.refresh, width=100)
        self.refresh_button.grid(row=0, column=2)

        self.list_title = ctk.CTkLabel(left_frame, text="All Bills", font=("Arial", 16, "bold"))
        self.list_title.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))

        # Bill list
        self.bill_list = CTkListbox(left_frame, command=self.on_select)
        self.bill_list.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Right frame
        self.right_frame = ctk.CTkFrame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid_rowconfigure(0, weight=1)  
        self.right_frame.grid_rowconfigure(1, weight=0) 
        self.right_frame.grid_rowconfigure(2, weight=1)

        # Variables
        self.reservation_search_var = ctk.StringVar()
        self.reservation_id_var = ctk.StringVar()
        self.amount_var = ctk.StringVar()
        self.date_var = ctk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        self.services_vars = []

        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Entry fields
        ctk.CTkLabel(form_frame, text="Search Reservation:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.reservation_search_frame = ctk.CTkFrame(form_frame)
        self.reservation_search_frame.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.reservation_entry = ctk.CTkEntry(self.reservation_search_frame, textvariable=self.reservation_search_var)
        self.reservation_entry.pack(side="left")
        self.reservation_search_button = ctk.CTkButton(self.reservation_search_frame, text="Search", command=self.search_reservation)
        self.reservation_search_button.pack(side="left")

        self.reservation_listbox = CTkListbox(form_frame, command=self.on_reservation_select)
        self.reservation_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.reservation_listbox.grid_remove()

        ctk.CTkLabel(form_frame, text="Services:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.services_frame = ctk.CTkFrame(form_frame)
        self.services_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.load_services()

        ctk.CTkLabel(form_frame, text="Date:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.date_entry = DateEntry(form_frame, textvariable=self.date_var, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Amount:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(form_frame, textvariable=self.amount_var).grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.button_frame = ctk.CTkFrame(form_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add Bill", command=self.add_bill)
        self.add_button.pack(side="left", padx=10)

        self.update_button = ctk.CTkButton(form_frame, text="Update Bill", command=self.update_bill)
        self.delete_button = ctk.CTkButton(form_frame, text="Delete Bill", command=self.delete_bill)
        self.generate_invoice_button = ctk.CTkButton(form_frame, text="Generate Invoice", command=self.generate_invoice)
        
        self.load_bills()


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
            
    def load_bills(self):
        bills = Bill.get_all_bill_details()
        self.bill_list.delete(0, "end")
        self.bill_id_map.clear()
        for index, bill in enumerate(bills):
            self.bill_list.insert("end", f"Bill {bill['bill_id']}: Reservation {bill['reservation_id']} - ${bill['amount']}")
            self.bill_id_map[index] = bill['bill_id']


    def on_select(self, event):
        selection = self.bill_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.bill_id_map.get(index)
            if bill_id:
                bill_details = Bill.get_bill_details(bill_id)
                if bill_details:
                    self.reservation_id_var.set(str(bill_details['reservation_id']))
                    self.amount_var.set(f"${bill_details['amount']:.2f}")
                    self.date_var.set(bill_details['date'])
                
                    # Set services checkboxes
                    for service_id, var in self.services_vars:
                        var.set(any(service['service_id'] == service_id for service in bill_details['services']))
                
                    self.button_frame.grid_remove()
                    self.update_button.grid(row=6, column=0, columnspan=2, pady=10)
                    self.delete_button.grid(row=7, column=0, columnspan=2, pady=10)
                    self.generate_invoice_button.grid(row=8, column=0, columnspan=2, pady=10)
                
                    # Update reservation entry
                    self.reservation_search_var.set(f"{bill_details['reservation_id']}: {bill_details['customer_name']} - {bill_details['check_in_date']} to {bill_details['check_out_date']}")
                    self.reservation_entry.configure(state="readonly")
                    self.reservation_search_button.pack_forget()
        else:
            # self.update_button.grid_forget()
            # self.delete_button.grid_forget()
            # self.button_frame.grid(row=4, column=0, columnspan=2, pady=10)
            self.clear_fields()

            
    def add_bill(self):
        try:
            selected_services = [service_id for service_id, var in self.services_vars if var.get()]
            Bill.create(
                int(self.reservation_id_var.get()),
                 float(self.amount_var.get().replace('$', '')),
                self.date_var.get(),
                selected_services
            )
            self.refresh()
            tkinter.messagebox.showinfo("Success", "Bill added successfully")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", str(e))

    def update_bill(self):
        selection = self.bill_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.bill_id_map.get(index)
            if bill_id:
                try:
                    selected_services = [service_id for service_id, var in self.services_vars if var.get()]
                    Bill.update(
                        bill_id,
                        int(self.reservation_id_var.get()),
                        float(self.amount_var.get().replace('$', '')),
                        self.date_var.get(),
                        selected_services
                    )
                    self.refresh()
                    tkinter.messagebox.showinfo("Success", "Bill updated successfully")
                except ValueError as e:
                    tkinter.messagebox.showerror("Error", str(e))
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a bill to update")

    def delete_bill(self):
        selection = self.bill_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.bill_id_map.get(index)
            if bill_id:
                if tkinter.messagebox.askyesno("Confirm", "Are you sure you want to delete this bill?"):
                    Bill.delete(bill_id)
                    self.refresh()
                    tkinter.messagebox.showinfo("Success", "Bill deleted successfully")
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a bill to delete")

    def search_bills(self):
        criteria = self.search_var.get()
        bills = Bill.search(criteria)
        self.bill_list.delete(0, "end")
        for bill in bills:
            reservation = Reservation.get(bill.reservation_id)
            self.bill_list.insert("end", f"Bill {bill.bill_id}: Reservation {reservation.reservation_id} - ${bill.amount}")
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

    def refresh(self):
        self.load_bills()
        self.clear_fields()
        self.list_title.configure(text="All Bills")

    def generate_invoice(self):
        selection = self.bill_list.curselection()
        if selection is not None:
            index = selection
            bill_id = self.bill_id_map.get(index)
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
                    tkinter.messagebox.showwarning("Error", "Bill details not found")
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a bill to generate an invoice")


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

        tkinter.messagebox.showinfo("Success", f"Invoice saved as {full_path}")