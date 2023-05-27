import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandastable import Table
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import statistics


def seleccion_archivo():
    global datos
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    datos = pd.read_csv(archivo)
    seleccion_atributo.set(datos.columns[0])
    opcion_atributo["menu"].delete(0, "end")
    for column in datos.columns:
        opcion_atributo["menu"].add_command(label=column, command=lambda value=column: seleccion_atributo.set(value))
    actualizar_opciones_graficas()

def mostrar_resultados_categoricos():
    tipo_atributo = seleccion_atributo.get()
    datos_atributo = datos[tipo_atributo]

    label_resultados_agrupados.config(text="")
    label_resultados_no_agrupados.config(text="")
    # Verificar si los datos son categóricos


        # Calcular la moda utilizando el método mode() de pandas
    moda = datos_atributo.mode().iloc[0]

        # Calcular la media asignando un valor numérico a cada categoría única
    categorias_unicas = datos_atributo.unique()
    valores_numericos = range(len(categorias_unicas))
    datos_numericos = datos_atributo.replace(categorias_unicas, valores_numericos)
    media = datos_numericos.mean()

        # Crear una cadena con los resultados
    resultados = f"Media: {media}\nModa: {moda}"
        # Actualizar el contenido de la etiqueta
    label_resultados_categoricos.config(text=resultados)

def datos_agrupados():
    tipo_atributo = seleccion_atributo.get()
    datos_atributo = datos[tipo_atributo]
    tabla_frecuencias = calcular_tabla_frecuencias()

        # Calcular las marcas de clase y las frecuencias para cada intervalo de clase
    marcas_clase = tabla_frecuencias['Marca']
    frecuencias = tabla_frecuencias['Frec Abs']
    # Calcular la media utilizando las marcas de clase y las frecuencias
    media = sum(marcas_clase * frecuencias) / sum(frecuencias)

    # Calcular la mediana utilizando las marcas de clase y las frecuencias
    n = sum(frecuencias)
    cumfreq = frecuencias.cumsum()
    cfbin = cumfreq.searchsorted(n / 2)
    if n % 2 == 0:
        l1 = marcas_clase[cfbin - 1]
        l2 = marcas_clase[cfbin]
        mediana = (l1 + l2) / 2
    else:
        mediana = marcas_clase[cfbin]

        # Calcular la moda utilizando las marcas de clase y las frecuencias
    moda_index = frecuencias.idxmax()
    moda = marcas_clase[moda_index]

    if media < mediana < moda:
        sesgo = "Hacia la izquierda"
    elif media == mediana == moda:
        sesgo = "Simétrico"
    elif moda < mediana < media:
        sesgo = "Hacia la derecha"
    else:
        sesgo = "No definido"
    rango = datos_atributo.max() - datos_atributo.min()
    varianza = (((tabla_frecuencias['Frec Abs'] * tabla_frecuencias['Marca']) ** 2).sum() - len(
    datos_atributo) * media ** 2) / (len(datos_atributo) - 1)
    desviacion_estandar = np.sqrt(varianza)

    return media, mediana, moda, sesgo, rango, varianza, desviacion_estandar


def datos_no_agrupados(datos_conglomerados):

    tipo_atributo = seleccion_atributo.get()
    datos_atributo = datos[tipo_atributo]

    media = statistics.mean(datos_conglomerados)
    mediana = statistics.median(datos_conglomerados)
    moda = statistics.mode(datos_conglomerados)

    if media < mediana < moda:
        sesgo = "Hacia la izquierda"
    elif media == mediana == moda:
        sesgo = "Simétrico"
    elif moda < mediana < media:
        sesgo = "Hacia la derecha"
    else:
        sesgo = "No definido"
    rango = datos_atributo.max() - datos_atributo.min()
    varianza = ((datos_atributo - media) ** 2).sum() / len(datos_atributo)
    desviacion_estandar = np.sqrt(varianza)

    return media, mediana, moda, sesgo, rango, varianza, desviacion_estandar


def mostrar_resultados():
    label_resultados_categoricos.config(text="")

    media, mediana, moda, sesgo, rango, varianza, desviacion_estandar = datos_agrupados()

    resultados = f"Agrupados \n Media: {media}\nMediana: {mediana}\nModa: {moda}\nSesgo: {sesgo}\nRango: {rango}\nVarianza: {varianza}\nDesviación estándar: {desviacion_estandar}"
    label_resultados_agrupados.config(text=resultados)


def mostrar_resulatados_no_agrupado():
    tabla_frecuencias = calcular_tabla_frecuencias()

    label_resultados_categoricos.config(text="")
    datos_conglomerados = tabla_frecuencias['Marca']
    media, mediana, moda, sesgo, rango, varianza, desviacion_estandar = datos_no_agrupados(datos_conglomerados)

    resultados = f"No agrupados \n Media: {media}\nMediana: {mediana}\nModa: {moda}\nSesgo: {sesgo}\nRango: {rango}\nVarianza: {varianza}\nDesviación estándar: {desviacion_estandar}"
    label_resultados_no_agrupados.config(text=resultados)


def actualizar_opciones_graficas(*args):
    tipo_atributo = seleccion_atributo.get()
    tipo_dato = datos[tipo_atributo].dtype
    opcion_grafica["menu"].delete(0, "end")

    if np.issubdtype(tipo_dato, np.number):
        opciones = ["pastel 2", "histograma", "poligono", "ojiva"]
    else:
        opciones = ["barra", "pastel"]
    for opcion in opciones:
        opcion_grafica["menu"].add_command(label=opcion, command=lambda value=opcion: seleccion_grafica.set(value))

    if np.issubdtype(tipo_dato, np.number):
        mostrar_resultados()
        mostrar_resulatados_no_agrupado()
    else:
        mostrar_resultados_categoricos()

    seleccion_grafica.set(opciones[0])
    mostrar_tabla_frecuencias()
    graficas()


def calcular_tabla_frecuencias():
    tipo_atributo = seleccion_atributo.get()
    datos_atributo = datos[tipo_atributo]

    minimo = datos_atributo.min()
    maximo = datos_atributo.max()
    rango = maximo - minimo
    numero_clase = int(1 + 3.3 * np.log10(len(datos_atributo)))
    intervalo = rango / numero_clase
    limites = np.arange(minimo, maximo + intervalo, intervalo)

    tabla_frecuencias = pd.DataFrame(columns=["Lim inf", "Lim sup", "Marca", "Frec Abs", "Frec Rel"])
    for i in range(numero_clase):
        lim_inf = limites[i]
        lim_sup = limites[i + 1]
        frecuencia_absoluta = ((datos_atributo >= lim_inf) & (datos_atributo < lim_sup)).sum()
        marca_clase = (lim_inf + lim_sup) / 2
        frecuencia_relativa = frecuencia_absoluta / len(datos_atributo)
        tabla_frecuencias.loc[i] = [round(lim_inf), round(lim_sup), round(marca_clase), round(frecuencia_absoluta),
                                    round(frecuencia_relativa, 2)]
    return tabla_frecuencias



def calcular_tabla_frecuencia_cualitativa():
    tipo_atributo = seleccion_atributo.get()
    datos_atributo = datos[tipo_atributo]

    frecuencia_absoluta = datos_atributo.value_counts()
    frecuencia_relativa = frecuencia_absoluta / len(datos_atributo)

    tabla_frecuencias = pd.DataFrame({"Categoría": frecuencia_absoluta.index,
                                      "Frec Abs": frecuencia_absoluta.values,
                                      'Frec Rel': frecuencia_relativa.values})
    return tabla_frecuencias


def mostrar_tabla_frecuencias():
    global ventana_tabla
    if datos is not None:
        tipo_atributo = seleccion_atributo.get()
        datos_atributo = datos[tipo_atributo]

        if np.issubdtype(datos_atributo.dtype, np.number):
            tabla_frecuencias = calcular_tabla_frecuencias()
        else:
            tabla_frecuencias = calcular_tabla_frecuencia_cualitativa()

        ventana_tabla.destroy()
        ventana_tabla = tk.Frame(ventana)
        ventana_tabla.pack(side="left", fill="y")
        tabla = Table(ventana_tabla, dataframe=tabla_frecuencias)
        tabla.show()

def exportar_csv():
    if datos is not None:
        tipo_atributo = seleccion_atributo.get()
        datos_atributo = datos[tipo_atributo]

        if np.issubdtype(datos_atributo.dtype, np.number):
            tabla_frecuencias = calcular_tabla_frecuencias()
        else:
            tabla_frecuencias = calcular_tabla_frecuencia_cualitativa()

        archivo = filedialog.asksaveasfilename(filetypes=[("Archivos CSV", "*.csv")])
        if not archivo.endswith('.csv'):
            archivo += '.csv'
        tabla_frecuencias.to_csv(archivo, index=False)


def exportar_grafica():
    # Muestra una ventana de diálogo para seleccionar el archivo de destino
    archivo = filedialog.asksaveasfilename(
        filetypes=[("Archivos PNG", "*.png"), ("Archivos PDF", "*.pdf"), ("Archivos SVG", "*.svg")])

    # Guarda la imagen de la gráfica en el archivo seleccionado
    figura.figure.savefig(archivo)


def graficas(*args):
    global figura
    if datos is not None:
        for borrar in grafica_ventana.winfo_children():
            borrar.destroy()

        tipo_atributo = seleccion_atributo.get()
        tipo_grafica = seleccion_grafica.get()
        datos_atributo = datos[tipo_atributo]
        frecuencia_absoluta = datos_atributo.value_counts()
        frecuencia_relativa = frecuencia_absoluta / len(datos_atributo)

        if np.issubdtype(datos_atributo.dtype, np.number):
            opciones_validas = ["pastel 2", "histograma", "poligono", "ojiva"]
        else:
            opciones_validas = ["barra", "pastel"]

        if tipo_grafica not in opciones_validas:
            return

        if tipo_grafica == "barra":

            figura = plt.Figure(figsize=(9,5))
            eje = figura.add_subplot(111)

            tabla_frecuencias = calcular_tabla_frecuencia_cualitativa()
            eje.bar(tabla_frecuencias['Categoría'], tabla_frecuencias['Frec Abs'])
            eje.set_xticklabels(tabla_frecuencias['Categoría'], rotation=45)

            eje.set_xlabel('Frecuencia')
            eje.set_ylabel('Valores')
            eje.set_title('Gráfica de barras')

        elif tipo_grafica == "pastel":

            figura = plt.Figure(figsize=(8, 6))
            eje = figura.add_subplot(111)
            eje.pie(frecuencia_relativa.values, labels=frecuencia_relativa.index, autopct='%1.1f%%')
            eje.set_title('Gráfica de pastel')
            eje.axis("equal")

        elif tipo_grafica == "poligono":
            figura = plt.Figure(figsize=(8, 6), dpi=100)
            eje = figura.add_subplot(111)

            tabla_frecuencias = calcular_tabla_frecuencias()
            x = [tabla_frecuencias['Lim inf'].min()] + list(tabla_frecuencias['Marca']) + [
                tabla_frecuencias['Lim sup'].max()]
            y = [0] + list(tabla_frecuencias['Frec Abs']) + [0]
            eje.plot(x, y, '-o')

            eje.set_xlabel('Marca de clase')
            eje.set_ylabel('Frecuencia')
            eje.set_title('Polígono de frecuencias')
        elif tipo_grafica == "histograma":
            figura = plt.Figure(figsize=(8, 6), dpi=100)
            eje = figura.add_subplot(111)

            tabla_frecuencias = calcular_tabla_frecuencias()
            eje.bar(tabla_frecuencias['Marca'], tabla_frecuencias['Frec Abs'],
                    width=tabla_frecuencias['Lim sup'][0] - tabla_frecuencias['Lim inf'][0])

            eje.set_xlabel('Valores')
            eje.set_ylabel('Frecuencia')
            eje.set_title('Histograma')
        elif tipo_grafica == "ojiva":
            figura = plt.Figure(figsize=(8, 6), dpi=100)
            eje = figura.add_subplot(111)

            tabla_frecuencias = calcular_tabla_frecuencias()
            frecuencia_relativa_acumulada = tabla_frecuencias['Frec Rel'].cumsum()
            eje.plot(tabla_frecuencias['Marca'], frecuencia_relativa_acumulada, '-o')

            eje.set_xlabel('Valores')
            eje.set_ylabel('Frecuencia Relativa Acumulada')
            eje.set_title('Ojiva')

        elif tipo_grafica == "pastel 2":
            figura = plt.Figure(figsize=(8, 6), dpi=100)
            eje = figura.add_subplot(111)

            tabla_frecuencias = calcular_tabla_frecuencias()
            eje.pie(tabla_frecuencias['Frec Abs'], labels=tabla_frecuencias['Marca'], autopct='%1.1f%%')

            eje.set_title('Gráfica de pastel')
            eje.axis("equal")

        else:
            print("No valido la grafica")

        figura = FigureCanvasTkAgg(figura, master=grafica_ventana)
        figura.get_tk_widget().pack()
        figura.draw()


ventana = tk.Tk()
ventana.title("Gráficas y cálculos")
ventana.state("zoomed")

columna_botones = tk.Frame(ventana, bg="light gray", width=100)
columna_botones.pack(side="left", fill="y")

grafica_ventana = tk.Frame(ventana)
grafica_ventana.pack(side="top", fill="both", expand=True)

ventana_tabla = tk.Frame(ventana)
ventana_tabla.pack(side="bottom", fill="x")

datos = None
figura = None

boton_archivo = tk.Button(columna_botones, text="Selecciona tu archivo", command=seleccion_archivo)
boton_archivo.grid(row=0, pady=10)

seleccion_atributo = tk.StringVar(columna_botones)
opcion_atributo = tk.OptionMenu(columna_botones, seleccion_atributo, "")
opcion_atributo.grid(row=1, pady=10)

seleccion_grafica = tk.StringVar(columna_botones)
seleccion_grafica.set("barra")

opcion_grafica = tk.OptionMenu(columna_botones, seleccion_grafica, "barra", "histograma", "pastel", "poligono", "ojiva","pastel 2", command=graficas)
opcion_grafica.grid(row=3, pady=10)

boton_exportar_csv = tk.Button(columna_botones, text="Exportar CSV", command=exportar_csv)
boton_exportar_csv.grid(row=4, pady=10)

label_resultados_agrupados = tk.Label(ventana)
label_resultados_agrupados.pack(side="right", fill="x")

label_resultados_no_agrupados = tk.Label(ventana)
label_resultados_no_agrupados.pack(side="right", fill="x")

label_resultados_categoricos = tk.Label(ventana)
label_resultados_categoricos.pack(side="right", fill="x")

seleccion_atributo.trace('w', actualizar_opciones_graficas)
seleccion_atributo.trace('w', graficas)
seleccion_grafica.trace('w', graficas)


ventana.mainloop()
