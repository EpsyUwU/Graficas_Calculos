import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def seleccion_archivo():
    global datos
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    datos = pd.read_csv(archivo)
    seleccion_atributo.set(datos.columns[0])
    opcion_atributo["menu"].delete(0, "end")
    for column in datos.columns:
        opcion_atributo["menu"].add_command(label=column, command=lambda value=column: seleccion_atributo.set(value))


def graficas(*args):
    if datos is not None:

        for borrar in grafica_ventana.winfo_children():
            borrar.destroy()

        tipo_atributo = seleccion_atributo.get()
        tipo_grafica = seleccion_grafica.get()
        frecuencia = datos[tipo_atributo].value_counts()
        figura = plt.Figure(figsize=(10, 6))
        eje = figura.add_subplot(111)

        if tipo_grafica == "barra":
            frecuencia.plot(kind="bar", ax=eje)
        elif tipo_grafica == "histograma":
            frecuencia.plot(kind="hist", ax=eje)
        elif tipo_grafica == "pastel":
            frecuencia.plot(kind="pie", ax=eje)
        elif tipo_grafica == "poligono":
            frecuencia = datos[tipo_atributo].value_counts().sort_index()
            frecuencia.plot(kind="line", ax=eje)
        elif tipo_grafica == "ojiva":
            valores, base = np.histogram(datos[tipo_atributo], bins=10)
            acumulativo = np.cumsum(valores)
            eje.plot(base[:-1], acumulativo, 'ro-')
        else:
            print("No valido la grafica")

        figura = FigureCanvasTkAgg(figura, master=grafica_ventana)
        figura.get_tk_widget().pack()
        figura.draw()

        df = pd.dataframe(frecuencia, columns=['Valor'])

        num_clases = 4
        amplitud = (df['Valor'].max() - df['Valor'].min()) / num_clases

        intervalos = [df['Valor'].min() + i * amplitud for i in range(num_clases)]
        intervalos.append(df['Valor'].max())

        frecuencias = pd.cut(df['Valor'], bins=intervalos).value_counts().sort_index()

        tabla_frecuencia = pd.DataFrame({'Intervalo de Clase': frecuencias.index, 'Frecuencia': frecuencias.values})


ventana = tk.Tk()
ventana.title("Graficas y calculos")
ventana.geometry("1200x800")  # Establecer el tamaño de la ventana

grafica_ventana = tk.Frame(ventana)
grafica_ventana.pack(side="right", fill="y")

columna_botones = tk.Frame(ventana, bg="light gray", width=100)
columna_botones.pack(side="left", fill="y")

datos = None

boton_archivo = tk.Button(columna_botones, text="Selecciona tu archivo", command=seleccion_archivo)
boton_archivo.grid(row=0, pady=10)

seleccion_atributo = tk.StringVar(columna_botones)
opcion_atributo = tk.OptionMenu(columna_botones, seleccion_atributo, "")
opcion_atributo.grid(row=1, pady=10)

seleccion_grafica = tk.StringVar(columna_botones)
seleccion_grafica.set("barra")
opcion_grafica = tk.OptionMenu(columna_botones, seleccion_grafica, "barra", "histograma", "pastel", "poligono", "ojiva", command=graficas)
opcion_grafica.grid(row=3, pady=10)

seleccion_atributo.trace('w', graficas)
seleccion_grafica.trace('w', graficas)


ventana.mainloop()
