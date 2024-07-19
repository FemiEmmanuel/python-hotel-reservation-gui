import customtkinter as ctk
from CTkListbox import *
import tkinter.messagebox
from model.customer import Customer

class CustomerManagement:
    def __init__(self, master):
        self.master = master
        self.customer_id_map = {}
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
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search customers...", width=200)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.search_entry.bind("<Return>", lambda event: self.search_customers())

        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_customers, width=100)
        self.search_button.grid(row=0, column=1)

        # Refresh button
        self.refresh_button = ctk.CTkButton(search_frame, text="Refresh", command=self.refresh, width=100)
        self.refresh_button.grid(row=0, column=2)

        self.list_title = ctk.CTkLabel(left_frame, text="All Customers", font=("Arial", 16, "bold"))
        self.list_title.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))

        # Customer list
        self.customer_list = CTkListbox(left_frame, command=self.on_select)
        self.customer_list.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Right frame
        self.right_frame = ctk.CTkFrame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid_rowconfigure(0, weight=1)  
        self.right_frame.grid_rowconfigure(1, weight=0) 
        self.right_frame.grid_rowconfigure(2, weight=1)

        # Variables
        self.name_var = ctk.StringVar()
        self.contact_var = ctk.StringVar()
        self.address_var = ctk.StringVar()
        self.email_var = ctk.StringVar()

        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Entry fields
        ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Contact:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(form_frame, textvariable=self.contact_var).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Address:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(form_frame, textvariable=self.address_var).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Email:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(form_frame, textvariable=self.email_var).grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.add_button = ctk.CTkButton(form_frame, text="Add Customer", command=self.add_customer)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.update_button = ctk.CTkButton(form_frame, text="Update Customer", command=self.update_customer)
        self.delete_button = ctk.CTkButton(form_frame, text="Delete Customer", command=self.delete_customer)

        # Load customers
        self.load_customers()

    def load_customers(self):
        customers = Customer.get_all()
        self.customer_list.delete(0, "end")
        self.customer_id_map.clear()
        for index, customer in enumerate(customers):
            self.customer_list.insert("end", f"{customer.name}")
            self.customer_id_map[index] = customer.customer_id

    def on_select(self, event):
        selection = self.customer_list.curselection()
        if selection is not None:
            index = selection
            customer_id = self.customer_id_map.get(index)
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

    def add_customer(self):
        name = self.name_var.get()
        contact = self.contact_var.get()
        address = self.address_var.get()
        email = self.email_var.get()

        if not all([name, contact, email]):
            tkinter.messagebox.showerror("Error", "Name, contact, and email are required fields.")
            return

        try:
            Customer.create(name, contact, address, email)
            self.refresh()
            tkinter.messagebox.showinfo("Success", "Customer added successfully")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", str(e))

    def update_customer(self):
        selection = self.customer_list.curselection()
        if selection is not None:
            index = selection
            customer_id = self.customer_id_map.get(index)
            if customer_id:
                name = self.name_var.get()
                contact = self.contact_var.get()
                address = self.address_var.get()
                email = self.email_var.get()

                if not all([name, contact, email]):
                    tkinter.messagebox.showerror("Error", "Name, contact, and email are required fields.")
                    return

                try:
                    Customer.update(customer_id, name, contact, address, email)
                    self.refresh()
                    tkinter.messagebox.showinfo("Success", "Customer updated successfully")
                except ValueError as e:
                    tkinter.messagebox.showerror("Error", str(e))
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a customer to update")

    def delete_customer(self):
        selection = self.customer_list.curselection()
        if selection is not None:
            index = selection
            customer_id = self.customer_id_map.get(index)
            if customer_id:
                if tkinter.messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
                    try:
                        Customer.delete(customer_id)
                        self.refresh()
                        tkinter.messagebox.showinfo("Success", "Customer deleted successfully")
                    except ValueError as e:
                        tkinter.messagebox.showerror("Error", str(e))
        else:
            tkinter.messagebox.showwarning("Warning", "Please select a customer to delete")

    def search_customers(self):
        criteria = self.search_var.get()
        customers = Customer.search(criteria)
        self.customer_list.delete(0, "end")
        self.customer_id_map.clear()
        for index, customer in enumerate(customers):
            self.customer_list.insert("end", f"{customer.name}")
            self.customer_id_map[index] = customer.customer_id
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

    def refresh(self):
        self.load_customers()
        self.clear_fields()
        self.list_title.configure(text="All Customers")