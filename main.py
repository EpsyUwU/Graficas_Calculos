import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def seleccion_archivo():
    global datos
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    print("Archivo seleccionado:", archivo)
    datos = pd.read_csv(archivo)


def graficar_columnas():
    if datos is not None:
        # Crear una figura y un eje
        figura, eje = plt.subplots()

        for columna in datos.columns:
            eje.plot(datos[columna], label=columna)

        eje.set_xlabel('Índice')
        eje.set_title('Gráfico de todas las columnas')
        eje.legend()

        # Crear el lienzo de la figura en Tkinter
        canvas = FigureCanvasTkAgg(figura, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    else:
        print("No se ha seleccionado ningún archivo.")

ventana = tk.Tk()
ventana.title("Graficas y calculos")
ventana.geometry("800x500")  # Establecer el tamaño de la ventana

columna_botones = tk.Frame(ventana, bg="light gray", width=100)
columna_botones.pack(side="left", fill="y")

datos = None

boton_archivo = tk.Button(columna_botones, text="Selecciona tu archivo", command=seleccion_archivo)
boton_archivo.grid(row=0, pady=10)

boton_graficar = tk.Button(columna_botones, text="Graficar todas las columnas", command=graficar_columnas)
boton_graficar.grid(row=1, pady=10)

ventana.mainloop()









