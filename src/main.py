import customtkinter as ctk
from app_controller import AppController

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = AppController()
    app.mainloop()