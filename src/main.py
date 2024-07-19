import customtkinter as ctk
from main_window import MainWindow

class HotelReservationSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Hotel Reservation System")
        self.root.geometry("1024x768")
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.main_window = MainWindow(self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HotelReservationSystem()
    app.run()