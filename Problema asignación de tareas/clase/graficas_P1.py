import numpy as np
import matplotlib.pyplot as plt


## -----------> Función para graficar todos los frentes de pareto de una generación 
def graficar_frentes_pareto(datos_frentes, titulo='Frentes de Pareto', etiqueta_x='Función Objetivo 1 (F1)', etiqueta_y='Función Objetivo 2 (F2)'):
    """
    Grafica una lista de frentes de Pareto.

    Parámetros:
    -----------
    datos_frentes : list
        Una lista de listas, donde cada sublista representa un frente de Pareto.
        Cada frente contiene arrays de NumPy de la forma [x, y].
    
    titulo : str, opcional
        El título principal de la gráfica.
        
    etiqueta_x : str, opcional
        La etiqueta para el eje X.
        
    etiqueta_y : str, opcional
        La etiqueta para el eje Y.
    """
    # 1. Crear la figura y los ejes
    plt.figure(figsize=(10, 7))

    # 2. Iterar sobre cada frente de Pareto
    for i, frente in enumerate(datos_frentes):
        
        # Ordenar los puntos por el valor del eje x para una línea limpia
        frente_ordenado = sorted(frente, key=lambda p: p[0])
        
        # 3. Extraer las coordenadas X y Y
        x_coords = [punto[0] for punto in frente_ordenado]
        y_coords = [punto[1] for punto in frente_ordenado]
        
        # 4. Graficar los puntos y la línea que los une
        plt.plot(
            x_coords, 
            y_coords, 
            marker='o',
            linestyle='-',
            linewidth=0.8,
            label=f'Frente {i+1}'
        )

    # 5. Añadir detalles finales usando los parámetros de la función
    plt.title(titulo)
    plt.xlabel(etiqueta_x)
    plt.ylabel(etiqueta_y)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # 6. Mostrar la gráfica
    plt.show()


# ------------------------- Graficar los frentes de pareto para las primeras 3 generaciones 
def graficar_frentes_pareto_3_gen(datos_frentes, titulo='Frentes de Pareto primeras 3 generaciones', etiqueta_x='F1: Tiempo ', etiqueta_y='F2: Consumo energético'):
    """
    Grafica una lista de frentes de Pareto.

    Parámetros:
    -----------
    datos_frentes : list
        Una lista de listas, donde cada sublista representa un frente de Pareto.
        Cada frente contiene arrays de NumPy de la forma [x, y].
    
    titulo : str, opcional
        El título principal de la gráfica.
        
    etiqueta_x : str, opcional
        La etiqueta para el eje X.
        
    etiqueta_y : str, opcional
        La etiqueta para el eje Y.
    """
    # 1. Crear la figura y los ejes
    plt.figure(figsize=(10, 7))

    # 2. Iterar sobre cada frente de Pareto
    for i, frente in enumerate(datos_frentes):
        
        # Ordenar los puntos por el valor del eje x para una línea limpia
        frente_ordenado = sorted(frente, key=lambda p: p[0])
        
        # 3. Extraer las coordenadas X y Y
        x_coords = [punto[0] for punto in frente_ordenado]
        y_coords = [punto[1] for punto in frente_ordenado]
        
        # 4. Graficar los puntos y la línea que los une
        plt.plot(
            x_coords, 
            y_coords, 
            marker='o',
            linestyle='-',
            linewidth=1.5,
            label=f'Frente Pareto generación: {i+1}'
        )

    # 5. Añadir detalles finales usando los parámetros de la función
    plt.title(titulo)
    plt.xlabel(etiqueta_x)
    plt.ylabel(etiqueta_y)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # 6. Mostrar la gráfica
    plt.show()




# ------------------------ FUNCION PARA GRAFICAR EL GRID DE PARETO --------------------------
def graficar_grid_pareto(lista_de_datos, lista_de_titulos, titulo_figura='Comparación de Frentes de Pareto'):
    """
    Grafica un grid de 2x2 con diferentes conjuntos de frentes de Pareto.

    Parámetros:
    -----------
    lista_de_datos : list
        Una lista que contiene 4 elementos. Cada elemento es un conjunto de datos 
        de frentes de Pareto (como el de los ejemplos anteriores).
    
    lista_de_titulos : list
        Una lista con 4 cadenas de texto, donde cada una es el título para 
        la gráfica correspondiente en el grid.
        
    titulo_figura : str, opcional
        El título principal que aparecerá en la parte superior de toda la ventana.
    """
    # Valida que se hayan proporcionado 4 conjuntos de datos y 4 títulos
    if len(lista_de_datos) != 4 or len(lista_de_titulos) != 4:
        print("Error: Debes proporcionar exactamente 4 conjuntos de datos y 4 títulos.")
        return

    # 1. Crear la figura y el grid de 2x2 de subplots (ejes)
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    
    # Añadir un título general a toda la figura
    fig.suptitle(titulo_figura, fontsize=16)

    # 2. Usar un bucle para poblar cada subplot del grid
    # Aplanamos los ejes (axs.flat) para iterar sobre ellos de forma sencilla (0, 1, 2, 3)
    for i, ax in enumerate(axs.flat):
        datos_actuales = lista_de_datos[i]
        titulo_actual = lista_de_titulos[i]
        
        # Iterar sobre cada frente en el conjunto de datos actual
        for j, frente in enumerate(datos_actuales):
            frente_ordenado = sorted(frente, key=lambda p: p[0])
            x_coords = [punto[0] for punto in frente_ordenado]
            y_coords = [punto[1] for punto in frente_ordenado]
            
            # Graficar en el 'ax' actual
            ax.plot(
                x_coords, 
                y_coords, 
                marker='o',
                linestyle='-',
                linewidth=0.8,
                label=f'Frente {j+1}'
            )
        
        # 3. Personalizar el subplot actual
        ax.set_title(titulo_actual)
        ax.set_xlabel('F1: Tiempo')
        ax.set_ylabel('F2: Consumo de energía')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

    # 4. Ajustar el espaciado para que no se solapen los títulos y mostrar
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # rect ajusta para el suptitle
    plt.show()


# ------------------- Grafica del frente de pareto para 1 generación ------------------------
def graficar_F_pareto_1_generacion(datos_frentes, i, etiqueta_x='F1: Tiempo', etiqueta_y='F2: Consumo energético'):
    """
    Grafica una lista de frentes de Pareto de una generación específica,
    resaltando el primer frente en rojo y el resto en gris.

    Parámetros:
    -----------
    datos_frentes : list
        Una lista de listas, donde cada sublista representa un frente de Pareto.
    
    i : int
        El número de la generación que se está graficando, para usarlo en el título.
        
    etiqueta_x : str, opcional
        La etiqueta para el eje X.
        
    etiqueta_y : str, opcional
        La etiqueta para el eje Y.
    """
    # 1. Crear la figura y los ejes
    plt.figure(figsize=(10, 7))
    
    # Construir el título dinámicamente con el número de generación
    titulo_grafica = f"Frente de pareto generación {i}"

    # 2. Iterar sobre cada frente de Pareto
    # Usamos 'idx' para el índice del bucle y evitar confusión con la 'i' de generación
    for idx, frente in enumerate(datos_frentes):
        
        # Ordenar los puntos por el valor del eje x para una línea limpia
        frente_ordenado = sorted(frente, key=lambda p: p[0])
        
        x_coords = [punto[0] for punto in frente_ordenado]
        y_coords = [punto[1] for punto in frente_ordenado]
        
        # 3. Lógica de colores y leyendas
        if idx == 0:
            # El primer frente se grafica en rojo
            color_frente = 'red'
            label_frente = 'Frente de pareto'
        else:
            # El resto de los frentes se grafican en gris
            color_frente = 'gray'
            # Para no saturar la leyenda, solo etiquetamos el primer "otro frente"
            label_frente = 'Otros Frentes' if idx == 1 else None

        # 4. Graficar los puntos y la línea que los une
        plt.plot(
            x_coords, 
            y_coords, 
            marker='o',
            markersize=4, # Tamaño de los marcadores
            linestyle='-',
            linewidth=0.9,
            color=color_frente,
            label=label_frente
        )

    # 5. Añadir detalles finales a la gráfica
    plt.title(titulo_grafica)
    plt.xlabel(etiqueta_x)
    plt.ylabel(etiqueta_y)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # 6. Mostrar la gráfica
    plt.show()



# --------------- GRAFICAS PARA GRAFICAR LA DISTANCIA DE CROWDING ----------------------------------
def graficar_distancia_crowding(
    todos_los_frentes, 
    indice_frente_crowding, 
    soluciones_elegidas, 
    etiqueta_x='F1: Tiempo', 
    etiqueta_y='F2: Consumo energético'
):
    """
    Crea una visualización de 1x2 para el proceso de selección por distancia de crowding en NSGA-II.

    Parámetros:
    -----------
    todos_los_frentes : list
        La lista completa de frentes de Pareto.
    
    indice_frente_crowding : int
        El índice del frente específico que se está analizando con crowding distance.
        
    soluciones_elegidas : list
        Una lista de puntos (np.array([x, y])) que son las soluciones seleccionadas
        del frente de crowding.
        
    etiqueta_x : str, opcional
        La etiqueta para el eje X.
        
    etiqueta_y : str, opcional
        La etiqueta para el eje Y.
    """
    # 1. Crear la figura y el grid de 1x2 (1 fila, 2 columnas)
    fig, axs = plt.subplots(1, 2, figsize=(20, 8))

    # --- DIBUJAR LA BASE EN AMBAS GRÁFICAS ---
    # Iteramos sobre todos los frentes para dibujarlos como fondo en ambas gráficas.
    for idx, frente in enumerate(todos_los_frentes):
        
        frente_ordenado = sorted(frente, key=lambda p: p[0])
        x_coords = [punto[0] for punto in frente_ordenado]
        y_coords = [punto[1] for punto in frente_ordenado]
        
        # Estilo condicional: diferente para el frente de crowding y para los demás
        if idx == indice_frente_crowding:
            # Estilo para el frente que se está analizando
            color = 'cyan'
            linewidth = 2.5
            markersize = 7
            label = 'Frente en Análisis'
            zorder = 2 # Dibuja este frente por encima de los grises
        else:
            # Estilo para los frentes de fondo (contexto)
            color = 'gray'
            linewidth = 1.0
            markersize = 5
            label = 'Otros Frentes' if idx == 0 else None # Etiqueta solo una vez
            zorder = 1 # Dibuja estos frentes por debajo

        # Dibujar en la primera gráfica (izquierda)
        axs[0].plot(x_coords, y_coords, marker='o', linestyle='-', color=color, 
                    linewidth=linewidth, markersize=markersize, label=label, zorder=zorder)
        
        # Dibujar lo mismo en la segunda gráfica (derecha)
        axs[1].plot(x_coords, y_coords, marker='o', linestyle='-', color=color, 
                    linewidth=linewidth, markersize=markersize, label=label, zorder=zorder)

    # --- RESALTAR LAS SOLUCIONES ELEGIDAS (SOLO EN LA SEGUNDA GRÁFICA) ---
    if soluciones_elegidas:
        x_elegidos = [p[0] for p in soluciones_elegidas]
        y_elegidos = [p[1] for p in soluciones_elegidas]
        
        # Usamos scatter para mayor control sobre el tamaño y apariencia de los puntos
        axs[1].scatter(x_elegidos, y_elegidos, 
                       color='darkblue', 
                       s=150,  # 's' es para el tamaño del marcador
                       label='Soluciones Elegidas',
                       zorder=3, # Dibuja estos puntos encima de todo
                       edgecolors='white') # Borde blanco para resaltar

    # --- CONFIGURACIÓN FINAL DE CADA GRÁFICA ---
    # Títulos
    axs[0].set_title('Frente para Estimador de Densidad (Distancia de Crowding)', fontsize=14)
    axs[1].set_title('Soluciones Elegidas por Distancia de Crowding', fontsize=14)

    # Aplicar etiquetas, leyendas y grid a ambas gráficas
    for ax in axs:
        ax.set_xlabel(etiqueta_x)
        ax.set_ylabel(etiqueta_y)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()