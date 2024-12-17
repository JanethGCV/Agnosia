import tkinter as tk
from tkinter import messagebox
import sys
import os

# directorio path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.database_manager import DatabaseManager
from juego_gestos import JuegoGestos
from ui.admin_interface import AdminInterface  # Asegúrate de que este archivo esté en el mismo directorio

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Inicio de Sesión")
        self.root.geometry("400x500")
        self.root.configure(bg='#FFE5F1')

        self.db_manager = DatabaseManager()
        
        self.create_login_ui()
    
    def create_login_ui(self):
        tk.Label(self.root, text="Juego de Agnosia 🎮", 
                 font=('Comic Sans MS', 24), 
                 bg='#FFE5F1', 
                 fg='#6B4423').pack(pady=20)
        
        tk.Label(self.root, text="Email:", bg='#FFE5F1').pack()
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.pack(pady=10)
       
        tk.Label(self.root, text="Contraseña:", bg='#FFE5F1').pack()
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=10)
        
        tk.Button(self.root, text="Iniciar Sesión", 
                  command=self.login, 
                  bg='#7BF1A8', 
                  fg='#525050').pack(pady=10)
        
        tk.Button(self.root, text="Registrarse", 
                  command=self.register, 
                  bg='#FF85B3', 
                  fg='white').pack(pady=10)
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        usuario = self.db_manager.validar_login(email, password)
        
        if usuario:
            if usuario['es_admin']:
                self.root.destroy()
                admin_interface = AdminInterface()  # Abre la interfaz de administración
                admin_interface.run()
            else:
                self.root.destroy()
                juego = JuegoGestos(usuario['id'])  # ID de usuario
                juego.iniciar()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def register(self):
        registro_window = tk.Toplevel(self.root)
        registro_window.title("Registro")
        registro_window.geometry("300x400")
        registro_window.configure(bg='#FFE5F1')
        
        # Campos de registro
        tk.Label(registro_window, text="Nombre de Usuario:", bg='#FFE5F1').pack()
        username_entry = tk.Entry(registro_window, width=30)
        username_entry.pack(pady=5)
        
        tk.Label(registro_window, text="Email:", bg='#FFE5F1').pack()
        email_entry = tk.Entry(registro_window, width=30)
        email_entry.pack(pady=5)
        
        tk.Label(registro_window, text="Contraseña:", bg='#FFE5F1').pack()
        password_entry = tk.Entry(registro_window, show="*", width=30)
        password_entry.pack(pady=5)
        
        def confirmar_registro():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            
            if self.db_manager.crear_usuario(username, email, password):
                messagebox.showinfo("Registro", "Usuario registrado exitosamente")
                registro_window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")
        
        tk.Button(registro_window, text="Registrar", 
                  command=confirmar_registro, 
                  bg='#7BF1A8', 
                  fg='#525050').pack(pady=10)
    
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    login = LoginWindow()
    login.iniciar()