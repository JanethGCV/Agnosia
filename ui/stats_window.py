import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.database_manager import DatabaseManager

class StatsWindow:
    def __init__(self, usuario_id):
        self.root = tk.Tk()
        self.root.title("🏆 Estadísticas de Juego")
        self.root.geometry("800x600")
        self.usuario_id = usuario_id
        self.db_manager = DatabaseManager()
        self.crear_interfaz_estadisticas()

    def crear_interfaz_estadisticas(self):
        # Obtener estadísticas y puntajes del usuario
        self.estadisticas = self.db_manager.obtener_estadisticas_usuario(self.usuario_id)
        self.puntajes = self.db_manager.obtener_puntajes(self.usuario_id)  # Método que debes implementar

        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#FFE5F1')
        frame_principal.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        tk.Label(frame_principal, text="Estadísticas de Juego", font=('Comic Sans MS', 24), bg='#FFE5F1', fg='#6B4423').pack(pady=10)

        # Menú desplegable para seleccionar tipo de gráfico
        self.selected_graph = tk.StringVar(value='Resumen de Juego')
        opciones_graficos = ['Resumen de Juego', 'Distribución de Puntajes', 'Puntaje Máximo y Mínimo', 'Progreso de Puntajes']
        tk.OptionMenu(frame_principal, self.selected_graph, *opciones_graficos, command=self.mostrar_grafico).pack(pady=10)

        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_principal)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill='both')

        self.mostrar_grafico(self.selected_graph.get())  # Mostrar gráfico inicial

    def mostrar_grafico(self, tipo_grafico):
        self.ax.clear()  # Limpiar el gráfico actual
        if tipo_grafico == 'Resumen de Juego':
            categorias = ['Total Partidas', 'Puntaje Promedio', 'Máximo Puntaje']
            valores = [self.estadisticas['total_partidas'], self.estadisticas['promedio_puntuacion'], self.estadisticas['maximo_puntaje']]
            self.ax.bar(categorias, valores, color=['#7BF1A8', '#FF85B3', '#46DBCF'])
            self.ax.set_title('Resumen de Juego')
            self.ax.set_ylabel('Valor')

        elif tipo_grafico == 'Distribución de Puntajes':
            self.ax.hist([p['puntuacion'] for p in self.puntajes], bins=10, color='blue', alpha=0.7)
            self.ax.set_title('Distribución de Puntajes')
            self.ax.set_xlabel('Puntuación')
            self.ax.set_ylabel('Frecuencia')

        elif tipo_grafico == 'Puntaje Máximo y Mínimo':
            maximo = self.estadisticas['maximo_puntaje']
            minimo = self.estadisticas['minimo_puntaje']
            self.ax.bar(['Máximo', 'Mínimo'], [maximo, minimo], color=['green', 'red'])
            self.ax.set_title('Puntaje Máximo y Mínimo')
            self.ax.set_ylabel('Puntuación')

        elif tipo_grafico == 'Progreso de Puntajes':
            fechas = [p['fecha'] for p in self.puntajes]  # Suponiendo que cada puntaje tiene una fecha
            puntajes = [p['puntuacion'] for p in self.puntajes]
            self.ax.plot(fechas, puntajes, marker='o', linestyle='-', color='purple')
            self.ax.set_title('Progreso de Puntajes a lo Largo del Tiempo')
            self.ax.set_xlabel('Fecha')
            self.ax.set_ylabel('Puntuación')
            self.ax.tick_params(axis='x', rotation=45)  # Rotar etiquetas de fecha

        self.canvas.draw()  # Redibujar el gráfico

    def mostrar(self):
        self.root.mainloop()