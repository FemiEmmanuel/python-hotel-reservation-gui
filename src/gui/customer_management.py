import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox

from gui.base_management import BaseManagement
from model.customer import Customer
from utils.colors import *

class CustomerManagement(BaseManagement):
    def __init__(self, master):
        super().__init__(master, "Customers")
        self.create_customer_specific_widgets()

    def create_customer_specific_widgets(self):
        # Variables
        self.name_var = ctk.StringVar()
        self.contact_var = ctk.StringVar()
        self.address_var = ctk.StringVar()
        self.email_var = ctk.StringVar()

        # Entry fields
        ctk.CTkLabel(self.form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text="Contact:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(self.form_frame, textvariable=self.contact_var).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text="Address:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(self.form_frame, textvariable=self.address_var).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text="Email:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(self.form_frame, textvariable=self.email_var).grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.add_button = ctk.CTkButton(self.form_frame, text="Add Customer", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.update_button = ctk.CTkButton(self.form_frame, text="Update Customer", command=self.update_item, fg_color=UPDATE_COLOR)
        self.delete_button = ctk.CTkButton(self.form_frame, text="Delete Customer", command=self.delete_item, fg_color=DELETE_COLOR)

        # Load customers
        self.load_items()

    def load_items(self):
        customers = Customer.get_all()
        self.item_list.delete(0, "end")
        self.id_map.clear()
        for index, customer in enumerate(customers):
            self.item_list.insert("end", f"{customer.name}")
            self.id_map[index] = customer.customer_id

    def on_select(self, event):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            customer_id = self.id_map.get(index)
            if customer_id:
                customer = Customer.get(customer_id)
                self.name_var.set(customer.name)
                self.contact_var.set(customer.contact)
                self.address_var.set(customer.address)
                self.email_var.set(customer.email)

                self.add_button.grid_forget()
                self.update_button.grid(row=5, column=0, columnspan=2, pady=10)
                self.delete_button.grid(row=6, column=0, columnspan=2, pady=10)
        else:
            self.update_button.grid_forget()
            self.delete_button.grid_forget()

    def add_item(self):
        name = self.name_var.get()
        contact = self.contact_var.get()
        address = self.address_var.get()
        email = self.email_var.get()

        if not all([name, contact, email]):
            self.handle_validation_error("Name, contact, and email are required fields.")
            return

        try:
            Customer.create(name, contact, address, email)
            self.refresh()
            self.handle_success("added")
        except ValueError as e:
            self.handle_error("adding customer", e)

    def update_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            customer_id = self.id_map.get(index)
            if customer_id:
                name = self.name_var.get()
                contact = self.contact_var.get()
                address = self.address_var.get()
                email = self.email_var.get()

                if not all([name, contact, email]):
                    self.handle_validation_error("Name, contact, and email are required fields.")
                    return

                try:
                    Customer.update(customer_id, name, contact, address, email)
                    self.refresh()
                    self.handle_success("updated")
                except ValueError as e:
                    self.handle_error("updating customer", e)
        else:
            self.handle_not_selected_error()

    def delete_item(self):
        selection = self.item_list.curselection()
        if selection is not None:
            index = selection
            customer_id = self.id_map.get(index)
            if customer_id:
                if self.confirm("Confirm", "Are you sure you want to delete this customer?"):
                    try:
                        Customer.delete(customer_id)
                        self.refresh()
                        self.handle_success("deleted")
                    except ValueError as e:
                        self.handle_error("deleting customer", e)
        else:
            self.handle_not_selected_error()

    def search_items(self):
        criteria = self.search_var.get()
        customers = Customer.search(criteria)
        self.item_list.delete(0, "end")
        self.id_map.clear()
        for index, customer in enumerate(customers):
            self.item_list.insert("end", f"{customer.name}")
            self.id_map[index] = customer.customer_id
        self.search_var.set("")

        if criteria:
            self.list_title.configure(text=f"Search Results for '{criteria}'")
        else:
            self.list_title.configure(text="All Customers")

    def clear_fields(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.address_var.set("")
        self.email_var.set("")

        self.update_button.grid_forget()
        self.delete_button.grid_forget()
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)