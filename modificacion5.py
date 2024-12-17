import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk

class JuegoGestos:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 ¡Juego Mágico de Gestos! 🎯")
        self.root.geometry("1200x800")
        
        # Cargar y establecer la imagen de fondo
        self.background_photo = None  # Atributo para almacenar la imagen
        try:
            # Carga tu imagen de fondo aquí
            background_image = Image.open("corazon.jpg")  # Reemplaza con tu imagen
            background_image = background_image.resize((1200, 800), Image.LANCZOS)  # Ajusta el tamaño
            self.background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(self.root, image=self.background_photo)
            background_label.image = self.background_photo  # Mantener una referencia
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            # Cambiar el color de fondo a un color que combine con la imagen
            self.root.configure(bg='#a0dade')
        
        # Configuración de MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Variables del juego con emojis
        self.jugando = False
        self.cap = None
        self.instrucciones = [
            "¡Levanta el dedo pulgar! 👍",
            "¡Levanta el dedo índice! ☝️",
            "¡Levanta el dedo medio! 🖕",
            "¡Levanta el dedo meñique!",
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
        # Frame principal con diseño infantil
        self.frame_principal = tk.Frame(self.root, bg='#de9fe0')
        self.frame_principal.pack(expand=True, fill='both', padx=10, pady=20)
        
        # Título grande y colorido
        titulo = tk.Label(self.frame_principal,
                         text="🌟 ¡Juego Mágico de Gestos! 🌟",
                         font=('Comic Sans MS', 16, 'bold'),
                         bg='#FF9ECD',
                         fg='#FFFFFF',
                         padx=15,
                         pady=3,
                         relief='raised',
                         borderwidth=3)
        titulo.pack(pady=5)
        
        # Frame para instrucciones con borde decorativo
        frame_instrucciones = tk.Frame(self.frame_principal,
                                     bg='#FFC2E2',
                                     relief='ridge',
                                     borderwidth=5)
        frame_instrucciones.pack(pady=5, padx=10, fill='x')
        
        # Label para instrucciones grande y llamativo
        self.lbl_instruccion = tk.Label(frame_instrucciones,
                                      text="¡Prepárate para jugar! 🎮",
                                      font=('Comic Sans MS', 20, 'bold'),
                                      bg='#FFC2E2',
                                      fg='#000000',
                                      padx=5,
                                      pady=10)
        self.lbl_instruccion.pack(fill='x')
        
        # Frame para estadísticas del juego
        frame_stats = tk.Frame(self.frame_principal, bg='#FFE5F1')
        frame_stats.pack(pady=10)
        
        # Timer con diseño infantil
        self.lbl_timer = tk.Label(frame_stats,
                                text="⏰ Tiempo: 60s",
                                font=('Comic Sans MS', 14, 'bold'),
                                bg='#FF85B3',
                                fg='white',
                                padx=5,
                                pady=2,
                                relief='raised',
                                borderwidth=2)
        self.lbl_timer.pack(side=tk.LEFT, padx=5)
        
        # Puntuación con diseño infantil
        self.lbl_puntuacion = tk.Label(frame_stats,
                                     text="🎯 Puntos: 0",
                                     font=('Comic Sans MS', 14, 'bold'),
                                     bg='#FF85B3',
                                     fg='white',
                                     padx=5,
                                     pady=2,
                                     relief='raised',
                                     borderwidth=2)
        self.lbl_puntuacion.pack(side=tk.LEFT, padx=5)
        
        # Botón de inicio grande y colorido
        self.btn_inicio = tk.Button(self.frame_principal,
                                  text="🎮 ¡Empezar a Jugar! 🎮",
                                  command=self.iniciar_juego,
                                  font=('Comic Sans MS', 14, 'bold'),
                                  bg='#7BF1A8',
                                  fg='#525050',
                                  padx=5,
                                  pady=2,
                                  relief='raised',
                                  borderwidth=3,
                                  cursor='hand2')
        self.btn_inicio.pack(pady=5)
        
        # Frame para el video con borde decorativo
        video_frame = tk.Frame(self.frame_principal,
                             bg='#FFC2E2',
                             relief='ridge',
                             borderwidth=8)
        video_frame.pack(expand=True, pady=10)
        
        self.lbl_video = tk.Label(video_frame, bg='black')
        self.lbl_video.pack(padx=5, pady=5)
        
        # Label para feedback con estilo infantil
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
        else:
            self.detener_juego()

    def detener_juego(self):
        self.jugando = False
        if self.cap is not None:
            self.cap.release()
        self.btn_inicio.config(text="🎮 ¡Empezar a Jugar! 🎮", bg='#46dbcf')
        self.lbl_instruccion.config(text="¡Juego terminado! 🎉")
        try:
            pygame.mixer.music.stop()
        except:
            pass
        messagebox.showinfo("🎉 ¡Fin del juego! 🎉", 
                          f"¡Felicitaciones! 🌟\n\nConseguiste {self.puntuacion} puntos\n\n¿Quieres intentar superarte? 😊")
        self.puntuacion = 0
        self.lbl_puntuacion.config(text="🎯 Puntos: 0")

    def nueva_instruccion(self):
        self.instruccion_actual = random.choice(self.instrucciones)
        self.lbl_instruccion.config(text=self.instruccion_actual)
        
    def verificar_gesto(self, landmarks):
        dedos = []
        # Verificar pulgar (basado en la posición x)
        if landmarks[4].x > landmarks[3].x:
            dedos.append(1)
        else:
            dedos.append(0)
        
        # Verificar los otros dedos (basado en la posición y)
        for tip in range(8, 21, 4):
            if landmarks[tip].y < landmarks[tip - 2].y:
                dedos.append(1)
            else:
                dedos.append(0)
                
        # Verificar el gesto actual
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
                # Voltear el frame horizontalmente para efecto espejo
                frame = cv2.flip(frame, 1)
                
                # Convertir el frame a RGB para MediaPipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(frame_rgb)
                
                # Dibujar los landmarks de las manos
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame_rgb, hand_landmarks, 
                                                  self.mp_hands.HAND_CONNECTIONS)
                        
                        # Verificar el gesto y actualizar puntuación
                        if self.verificar_gesto(hand_landmarks.landmark):
                            self.puntuacion += 1
                            self.lbl_puntuacion.config(text=f"🎯 Puntos: {self.puntuacion}")
                            try:
                                self.sonido_correcto.play()
                            except:
                                pass
                            self.nueva_instruccion()
                
                # Convertir el frame a formato PIL
                img = Image.fromarray(frame_rgb)
                
                # Redimensionar manteniendo la proporción
                display_width = 640  # Puedes ajustar este valor
                ratio = display_width / img.width
                display_height = int(img.height * ratio)
                img = img.resize((display_width, display_height), Image.LANCZOS)
                
                # Convertir a formato PhotoImage
                self.photo = ImageTk.PhotoImage(image=img)
                self.lbl_video.config(image=self.photo)
                
                # Programar la siguiente actualización
                self.root.after(10, self.actualizar_frame)

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    juego = JuegoGestos()
    juego.iniciar()