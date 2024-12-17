import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk
import mysql.connector  # Asegúrate de tener mysql-connector-python instalado
from ui.stats_window import StatsWindow

class JuegoGestos:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id 
        self.root = tk.Tk()
        self.root.title("🎮 ¡Juego Mágico de Gestos! 🎯")
        self.root.geometry("1200x800")
        
        # Cargar y establecer la imagen de fondo
        self.background_photo = None
        try:
            background_image = Image.open("corazon.jpg")  # Reemplaza con tu imagen
            background_image = background_image.resize((1200, 800), Image.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(self.root, image=self.background_photo)
            background_label.image = self.background_photo
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.root.configure(bg='#a0dade')
        
        # Configuración de MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Variables del juego
        self.jugando = False
        self.cap = None
        self.instrucciones = [
            "¡Levanta el dedo pulgar! 👍",
            "¡Levanta el dedo índice! ☝️",
            "¡Levanta el dedo medio! 🖕",
            "¡Levanta el dedo meñique! ✋",
            "¡Cierra el puño! ✊",
            "¡Abre toda la mano! 🖐",
            "¡Haz el símbolo de la paz! ✌️",
            "¡Levanta el pulgar y el meñique! 🤙"
        ]
        self.instruccion_actual = ""
        self.tiempo_restante = 60
        self.puntuacion = 0
        
        self.crear_interfaz()
        
        # Inicializar pygame para los sonidos
        pygame.mixer.init()
        
        # Cargar sonidos
        try:
            pygame.mixer.music.load("sfx-magic2.mp3")
            self.sonido_correcto = pygame.mixer.Sound("sfx-victory2.wav")
        except:
            print("No se pudieron cargar los sonidos")

    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg='#de9fe0')
        self.frame_principal.pack(expand=True, fill='both', padx=10, pady=20)
        
        # Título
        titulo = tk.Label(self.frame_principal,
                         text="🌟 ¡Juego Mágico de Gestos! 🌟",
                         font=('Comic Sans MS', 15, 'bold'),
                         bg='#FF9ECD',
                         fg='#FFFFFF',
                         padx=15,
                         pady=3,
                         relief='raised',
                         borderwidth=3)
        titulo.pack(pady=5)
        
        # Frame para instrucciones
        frame_instrucciones = tk.Frame(self.frame_principal,
                                     bg='#FFC2E2',
                                     relief='ridge',
                                     borderwidth=5)
        frame_instrucciones.pack(pady=5, padx=10, fill='x')
        
        # Label para instrucciones
        self.lbl_instruccion = tk.Label(frame_instrucciones,
                                      text="¡Prepárate para jugar! 🎮",
                                      font=('Comic Sans MS', 18, 'bold'),
                                      bg='#FFC2E2',
                                      fg='#000000',
                                      padx=2,
                                      pady=9)
        self.lbl_instruccion.pack(fill='x')
        
        # Frame para estadísticas
        frame_stats = tk.Frame(self.frame_principal, bg='#FFE5F1')
        frame_stats.pack(pady=10)
        
        # Timer
        self.lbl_timer = tk.Label(frame_stats,
                                text="⏰ Tiempo: 60s",
                                font=('Comic Sans MS', 13, 'bold'),
                                bg='#FF85B3',
                                fg ='white',
                                padx=5,
                                pady=2,
                                relief='raised',
                                borderwidth=2)
        self.lbl_timer.pack(side=tk.LEFT, padx=5)
        
        # Puntuación
        self.lbl_puntuacion = tk.Label(frame_stats,
                                     text="🎯 Puntos: 0",
                                     font=('Comic Sans MS', 13, 'bold'),
                                     bg='#FF85B3',
                                     fg='white',
                                     padx=5,
                                     pady=2,
                                     relief='raised',
                                     borderwidth=2)
        self.lbl_puntuacion.pack(side=tk.LEFT, padx=5)
        
        # Botón de inicio
        self.btn_inicio = tk.Button(self.frame_principal,
                                  text="🎮 ¡Empezar a Jugar! 🎮",
                                  command=self.iniciar_juego,
                                  font=('Comic Sans MS', 12, 'bold'),
                                  bg='#7BF1A8',
                                  fg='#525050',
                                  padx=3,
                                  pady=2,
                                  relief='raised',
                                  borderwidth=3,
                                  cursor='hand2')
        self.btn_inicio.pack(pady=3)
        
        # Botón para ver estadísticas
        self.btn_estadisticas = tk.Button(self.frame_principal,
                                          text="📊 Ver Estadísticas",
                                          command=self.mostrar_estadisticas,
                                          font=('Comic Sans MS', 12, 'bold'),
                                          bg='#FF9ECD',
                                          fg='#000000',
                                          padx=3,
                                          pady=2,
                                          relief='raised',
                                          borderwidth=3,
                                          cursor='hand2')
        self.btn_estadisticas.pack(pady=3)
        
        # Frame para el video
        video_frame = tk.Frame(self.frame_principal,
                             bg='#FFC2E2',
                             relief='ridge',
                             borderwidth=8)
        video_frame.pack(expand=True, pady=10)
        
        self.lbl_video = tk.Label(video_frame, bg='black')
        self.lbl_video.pack(padx=5, pady=5)
        
        # Label para feedback
        self.lbl_feedback = tk.Label(self.frame_principal,
                                   text="",
                                   font=('Comic Sans MS', 18),
                                   bg='#FFE5F1',
                                   fg='#6B4423')
        self.lbl_feedback.pack(pady=5)

    def actualizar_timer(self):
        if self.jugando and self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.lbl_timer.config(text=f"⏰ Tiempo: {self.tiempo_restante}s")
        if self.tiempo_restante == 0:
            self.detener_juego()
        else:
            self.root.after(1000, self.actualizar_timer)

    def iniciar_juego(self):
        if not self.jugando:
            self.jugando = True
            self.tiempo_restante = 60
            self.puntuacion = 0
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "¡No se pudo encontrar la cámara! 😢")
                return
            self.btn_inicio.config(text="🛑 Detener Juego 🛑", bg='#FF6B6B')
            self.nueva_instruccion()
            self.actualizar_frame()
            self.actualizar_timer()
            try:
                pygame.mixer.music.play(-1)
            except:
                pass

    def detener_juego(self):
        self.jugando = False
        if self.cap is not None:
            self.cap.release()
            self.btn_inicio.config(text="🎮 ¡Empezar a Jugar! 🎮", bg='#46dbcf')
            self.lbl_instruccion.config(text="¡Juego terminado! 🎉")
            self.guardar_puntuacion()
            try:
                pygame.mixer.music.stop()
            except:
                pass
            messagebox.showinfo("🎉 ¡Fin del juego! 🎉", 
                              f"¡Felicitaciones! 🌟\n\nConseguiste {self.puntuacion} puntos\n\n¿Quieres intentar superarte? 😊")
            self.puntuacion = 0
            self.lbl_puntuacion.config(text="🎯 Puntos: 0")

    def guardar_puntuacion(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='gesture_game_db'
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO partidas (usuario_id, puntuacion) VALUES (%s, %s)", (self.usuario_id, self.puntuacion))
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def nueva_instruccion(self):
        self.instruccion_actual = random.choice(self.instrucciones)
        self.lbl_instruccion.config(text=self.instruccion_actual)
    
    def verificar_gesto(self, landmarks):
        dedos = []
        if landmarks[4].x > landmarks[3].x:
            dedos.append(1)
        else:
            dedos.append(0)
        
        for tip in range(8, 21, 4):
            if landmarks[tip].y < landmarks[tip - 2].y:
                dedos.append(1)
            else:
                dedos.append(0)
                
        if "pulgar" in self.instruccion_actual.lower() and not "meñique" in self.instruccion_actual.lower():
            return dedos == [1, 0, 0, 0, 0]
        elif "índice" in self.instruccion_actual.lower():
            return dedos == [0, 1, 0, 0, 0]
        elif "medio" in self.instruccion_actual.lower():
            return dedos == [0, 0, 1, 0, 0]
        elif "meñique" in self.instruccion_actual.lower() and not "pulgar" in self.instruccion_actual.lower():
            return dedos == [0, 0, 0, 0, 1]
        elif "puño" in self.instruccion_actual.lower():
            return dedos == [0, 0, 0, 0, 0]
        elif "abre" in self.instruccion_actual.lower():
            return dedos == [1, 1, 1, 1, 1]
        elif "paz" in self.instruccion_actual.lower():
            return dedos == [0, 1, 1, 0, 0]
        elif "pulgar" in self.instruccion_actual.lower() and "meñique" in self.instruccion_actual.lower():
            return dedos == [1, 0, 0, 0, 1]
        return False

    def actualizar_frame(self):
        if self.jugando:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(frame_rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame_rgb, hand_landmarks, 
                                                  self.mp_hands.HAND_CONNECTIONS)
                        
                        if self.verificar_gesto(hand_landmarks.landmark):
                            self.puntuacion += 1
                            self.lbl_puntuacion.config(text=f"🎯 Puntos: {self.puntuacion}")
                            try:
                                self.sonido_correcto.play()
                            except:
                                pass
                            self.nueva_instruccion()
                
                img = Image.fromarray(frame_rgb)
                display_width = 640
                ratio = display_width / img.width
                display_height = int(img.height * ratio)
                img = img.resize((display_width, display_height), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(image=img)
                self.lbl_video.config(image=self.photo)
                
                self.root.after(10, self.actualizar_frame)

    def mostrar_estadisticas(self):
        stats_window = StatsWindow(self.usuario_id)
        stats_window.mostrar()

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    juego = JuegoGestos(1)  # Cambia 1 por el ID del usuario correspondiente
    juego.iniciar()