#Del Ángel Mercado Jorge Rafael
#Martínez Ríos Evelyn Yanet

import customtkinter as ctk
import threading
import random
import time

#Configuración de la interfaz gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#Configuración del buffer y estados
BUFFER_SIZE = 20
buffer = [None] * BUFFER_SIZE
producer_index = 0
consumer_index = 0
mutex = threading.Lock()

#Configuración de la ventana principal
app = ctk.CTk()
app.title("Productor-Consumidor")
app.geometry("800x200")

#Estado del productor y consumidor
producer_state = ctk.StringVar(value="Dormido")
consumer_state = ctk.StringVar(value="Dormido")

#Configuración de frames del buffer
buffer_frames = []
for i in range(BUFFER_SIZE):
    frame = ctk.CTkFrame(app, width=30, height=30, border_width=1)
    frame.grid(row=0, column=i, padx=5, pady=5)
    buffer_frames.append(frame)
    label = ctk.CTkLabel(app, text=str(i+1), font=("Arial", 12, 'bold'))
    label.grid(row=1, column=i, padx=5, pady=0)

p_label = ctk.CTkLabel(app, text="    Productor    ", text_color="white", fg_color="#355070", font=("Arial", 14, 'bold'))
p_label.grid(row=2, column=0, columnspan=12, pady=15)

c_label = ctk.CTkLabel(app, text="  Consumidor  ", text_color="white", fg_color="#d65780", font=("Arial", 14, 'bold'))
c_label.grid(row=3, column=0, columnspan=12, pady=0)

#Etiquetas de estado
producer_label = ctk.CTkLabel(app, textvariable=producer_state, text_color="white", font=("Arial", 12, 'bold'))
producer_label.grid(row=2, column=0, columnspan=20, pady=10)

consumer_label = ctk.CTkLabel(app, textvariable=consumer_state, text_color="white", font=("Arial", 12, 'bold'))
consumer_label.grid(row=3, column=0, columnspan=20, pady=10)

#Función para actualizar el estado de un espacio en el buffer
def update_buffer_display():
    for i in range(BUFFER_SIZE):
        if buffer[i] is not None:
            buffer_frames[i].configure(fg_color="green")  # Espacio lleno
        else:
            buffer_frames[i].configure(fg_color="gray")  # Espacio vacío

#Función del productor
def producer():
    global producer_index
    while True:
        producer_state.set("Dormido")
        time.sleep(random.uniform(1, 3))  # Tiempo aleatorio de espera
        producer_state.set("Intentando producir")
        
        #Bloqueo de mutex para sincronización
        with mutex:
            if buffer[producer_index] is None:
                items_to_produce = random.randint(3, 6)
                producer_state.set(f"Produciendo {items_to_produce} elementos")

                for _ in range(items_to_produce):
                    if buffer[producer_index] is None:
                        buffer[producer_index] = "X"  #Añadimos un producto
                        update_buffer_display()
                        producer_index = (producer_index + 1) % BUFFER_SIZE
                        time.sleep(0.5)  #Control visual de la producción
                    else:
                        break
            else:
                producer_state.set("Esperando espacio")

#Función del consumidor
def consumer():
    global consumer_index
    while True:
        consumer_state.set("Dormido")
        time.sleep(random.uniform(1, 3))  #Tiempo aleatorio de espera
        consumer_state.set("Intentando consumir")
        
        # Bloqueo de mutex para sincronización
        with mutex:
            if buffer[consumer_index] is not None:
                items_to_consume = random.randint(3, 6)
                consumer_state.set(f"Consumiendo {items_to_consume} elementos")

                for _ in range(items_to_consume):
                    if buffer[consumer_index] is not None:
                        buffer[consumer_index] = None  #Quitamos un producto
                        update_buffer_display()
                        consumer_index = (consumer_index + 1) % BUFFER_SIZE
                        time.sleep(0.5)  #Control visual del consumo
                    else:
                        break
            else:
                consumer_state.set("Esperando producto")

#Hilos para el productor y consumidor
producer_thread = threading.Thread(target=producer, daemon=True)
consumer_thread = threading.Thread(target=consumer, daemon=True)
producer_thread.start()
consumer_thread.start()

#Configuración para cerrar el programa con la tecla "Esc"
def on_keypress(event):
    if event.keysym == "Escape":
        app.destroy()

app.bind("<Escape>", on_keypress)
app.mainloop()
