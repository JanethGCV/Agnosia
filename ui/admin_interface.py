import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.database_manager import DatabaseManager

class AdminInterface:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.root = tk.Tk()
        self.root.title("Interfaz de Administración")
        self.root.geometry("800x600")
        self.usuario_actual = None

        self.create_admin_ui()

    def create_admin_ui(self):
        tk.Label(self.root, text="Usuarios Registrados", font=('Arial', 24)).pack(pady=10)

        # Cambiar Listbox por Combobox para mejor visualización
        self.lista_usuarios = ttk.Combobox(self.root, width=50)
        self.lista_usuarios.pack(pady=10)
        self.cargar_usuarios()

        tk.Button(self.root, text="Gráfica de Puntajes", command=self.graficar_puntajes).pack(pady=10)

        # Menú desplegable para seleccionar el tipo de gráfico
        self.selected_graph = tk.StringVar(value='Resumen de Juego')
        opciones_graficos = ['Resumen de Juego', 'Distribución de Puntajes', 'Puntaje Máximo y Mínimo', 'Progreso de Puntajes']
        tk.OptionMenu(self.root, self.selected_graph, *opciones_graficos).pack(pady=10)

        tk.Button(self.root, text="Ver Estadísticas", command=self.mostrar_estadisticas).pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill='both')

    def cargar_usuarios(self):
        usuarios = self.db_manager.obtener_usuarios()
        # Extraer solo los nombres de usuario para el combobox
        nombres_usuarios = [f"{usuario['username']} (ID: {usuario['id']})" for usuario in usuarios]
        self.lista_usuarios['values'] = nombres_usuarios

    def mostrar_estadisticas(self):
        seleccion = self.lista_usuarios.current()  # Obtener el índice seleccionado
        if seleccion >= 0:
            usuario_id = self.db_manager.obtener_usuarios()[seleccion]['id']
            estadisticas = self.db_manager.obtener_estadisticas_usuario(usuario_id)
            puntajes = self.db_manager.obtener_puntajes(usuario_id)

            # Mostrar estadísticas en un mensaje
            messagebox.showinfo("Estadísticas", f"Total Partidas: {estadisticas['total_partidas']}\n"
                                                 f"Promedio Puntuación: {estadisticas['promedio_puntuacion']}\n"
                                                 f"Máximo Puntaje: {estadisticas['maximo_puntaje']}\n"
                                                 f"Mínimo Puntaje: {estadisticas['minimo_puntaje']}")

            # Obtener el tipo de gráfico seleccionado
            tipo_grafico = self.selected_graph.get()
            self.ax.clear()  # Limpiar el gráfico actual

            if tipo_grafico == 'Resumen de Juego':
                categorias = ['Total Partidas', 'Puntaje Promedio', 'Máximo Puntaje']
                valores = [estadisticas['total_partidas'], estadisticas['promedio_puntuacion'], estadisticas['maximo_puntaje']]
                self.ax.bar(categorias, valores, color=['#7BF1A8', '#FF85B3', '#46DBCF'])
                self.ax.set_title('Resumen de Juego')
                self.ax.set_ylabel('Valor')
                self.ax.set_ylim(0, max(valores) + 5)  # Ajustar el límite del eje Y

            elif tipo_grafico == 'Distribución de Puntajes':
                self.ax.hist([p['puntuacion'] for p in puntajes], bins= 10, color='blue', alpha=0.7)
                self.ax.set_title('Distribución de Puntajes')
                self.ax.set_xlabel('Puntuación')
                self.ax.set_ylabel('Frecuencia')
                self.ax.set_ylim(0, max([p['puntuacion'] for p in puntajes]) + 1)  # Ajustar el límite del eje Y

            elif tipo_grafico == 'Puntaje Máximo y Mínimo':
                maximo = estadisticas['maximo_puntaje']
                minimo = estadisticas['minimo_puntaje']
                self.ax.bar(['Máximo', 'Mínimo'], [maximo, minimo], color=['green', 'red'])
                self.ax.set_title('Puntaje Máximo y Mínimo')
                self.ax.set_ylabel('Puntuación')
                self.ax.set_ylim(0, max(maximo, minimo) + 5)  # Ajustar el límite del eje Y

            elif tipo_grafico == 'Progreso de Puntajes':
                fechas = [p['fecha'] for p in puntajes]  # Suponiendo que cada puntaje tiene una fecha
                puntuaciones = [p['puntuacion'] for p in puntajes]
                self.ax.plot(fechas, puntuaciones, marker='o', linestyle='-', color='purple')
                self.ax.set_title('Progreso de Puntajes a lo Largo del Tiempo')
                self.ax.set_xlabel('Fecha')
                self.ax.set_ylabel('Puntuación')
                self.ax.tick_params(axis='x', rotation=45)  # Rotar etiquetas de fecha
                self.ax.set_ylim(0, max(puntuaciones) + 5)  # Ajustar el límite del eje Y

            self.canvas.draw()  # Redibujar el gráfico
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")

    def graficar_puntajes(self):
        usuarios = self.db_manager.obtener_usuarios()
        nombres = []
        promedios = []
        maximos = []

        for usuario in usuarios:
            estadisticas = self.db_manager.obtener_estadisticas_usuario(usuario['id'])
            nombres.append(usuario['username'])
            promedios.append(estadisticas['promedio_puntuacion'])
            maximos.append(estadisticas['maximo_puntaje'])

        # Graficar puntajes promedio y máximo
        self.ax.clear()
        bar_width = 0.35
        index = range(len(nombres))

        self.ax.bar(index, promedios, bar_width, label='Puntaje Promedio', color='b')
        self.ax.bar([i + bar_width for i in index], maximos, bar_width, label='Puntaje Máximo', color='r')

        self.ax.set_xlabel('Usuarios')
        self.ax.set_ylabel('Puntuaciones')
        self.ax.set_title('Puntuaciones Promedio y Máximo por Usuario')
        self.ax.set_xticks([i + bar_width / 2 for i in index])
        self.ax.set_xticklabels(nombres)
        self.ax.legend()
        self.ax.grid()
        self.ax.set_ylim(0, max(maximos) + 5)  # Ajustar el límite del eje Y

        self.canvas.draw()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AdminInterface()
    app.run()