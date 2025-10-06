import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def transformar_datos_visualizador(mtx_oper_mach, mtx_oper_tsk, vector_gen):
    """_summary_

    Args:
        mtx_oper_mach (list): Listas o vectores bidimensionales que contienen la relación de las operaciones con el consumo de tiempo por máquina. 
        mtx_oper_tsk (list): Lista unidimensional que contiene las tareas con sus operaciones para ser ejecutadas por el algoritmo 
        vector_gen (list): Es el vector solución (cromosoma) al cual se le van a obtener los datos. 

    Returns:
        _type_: _description_
    """
    # --- LÓGICA DE TIEMPO CORREGIDA ---
    num_tareas = len(mtx_oper_tsk)
    num_maquinas = mtx_oper_mach.shape[1]
    
    # "Relojes" que indican cuándo queda libre cada recurso.
    tiempo_maquinas = [0.0] * num_maquinas
    tiempo_tareas = [0.0] * num_tareas
    
    # Estructura de salida para los datos del gráfico
    arreglo_visualizador = [[] for _ in range(num_tareas)]

    # El resto de tu código para decodificar el vector_gen es correcto.
    # Lo he simplificado un poco para mayor claridad.
    idx_operacion_global = 0
    for i in range(num_tareas):  # Recorremos cada tarea
        for j in range(len(mtx_oper_tsk[i])):  # Recorremos cada operación de la tarea
            
            # Obtenemos los datos de la operación actual
            operacion_id = mtx_oper_tsk[i][j]
            maquina_asignada = vector_gen[idx_operacion_global]
            
            # Los índices para las matrices son base 0
            maquina_idx = maquina_asignada - 1
            operacion_idx = operacion_id - 1
            
            duracion = mtx_oper_mach[operacion_idx][maquina_idx]
            
            # --- CÁLCULO CLAVE DEL TIEMPO DE INICIO ---
            tiempo_maquina_libre = tiempo_maquinas[maquina_idx]
            tiempo_tarea_lista = tiempo_tareas[i]
            
            inicio = max(tiempo_maquina_libre, tiempo_tarea_lista)
            fin = inicio + duracion
            
            # --- ACTUALIZACIÓN DE LOS RELOJES ---
            tiempo_maquinas[maquina_idx] = fin
            tiempo_tareas[i] = fin
            
            # Agregamos el diccionario con los datos correctos para la gráfica
            arreglo_visualizador[i].append({
                'maquina': maquina_idx,  # Usamos índice base 0 para graficar
                'duracion': duracion,
                'inicio': inicio,
                'actividad_num': j + 1, # El número de operación dentro de la tarea
                'tarea_num': i + 1
            })
            
            print(f"T{i+1}-Op{j+1} (ID:{operacion_id}): Máq {maquina_asignada}, Inicia: {inicio:.2f}, Dura: {duracion:.2f}, Termina: {fin:.2f}")
            
            idx_operacion_global += 1

    return arreglo_visualizador


# -----------------------> FUNCION PARA GRAFICAR UN DIAGRAMA DE GANTT ---------------------------
def graficar_gantt(datos_gantt):
    """
    Grafica un diagrama de Gantt a partir de una estructura de datos pre-procesada.
    
    Args:
        datos_gantt (list): Una lista de listas, donde cada sublista representa una tarea
                             y contiene diccionarios para cada operación.
    """
    if not any(datos_gantt):
        print("No hay datos para graficar.")
        return

    # Detectar el número de máquinas automáticamente
    max_maquina_idx = 0
    for tarea in datos_gantt:
        for op in tarea:
            if op['maquina'] > max_maquina_idx:
                max_maquina_idx = op['maquina']
    num_maquinas = max_maquina_idx + 1
    maquinas_labels = [f'Máquina {i+1}' for i in range(num_maquinas)]

    # Calcular el makespan (tiempo final de la última operación)
    makespan = 0
    for tarea in datos_gantt:
        for op in tarea:
            if op['inicio'] + op['duracion'] > makespan:
                makespan = op['inicio'] + op['duracion']

    # Colores para cada tarea
    colores = plt.cm.get_cmap('tab20', len(datos_gantt))

    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(15, num_maquinas * 0.8 + 2))
    ax.set_xlim(0, makespan * 1.05)
    ax.set_ylim(-0.5, num_maquinas - 0.5)
    ax.set_yticks(range(num_maquinas))
    ax.set_yticklabels(maquinas_labels)
    ax.set_xlabel('Tiempo')
    ax.set_title('Diagrama de Gantt de la Planificación de Tareas')
    ax.grid(True, axis='x', linestyle=':', color='gray', alpha=0.5)

    # Invertir el eje Y para que la Máquina 1 esté arriba
    ax.invert_yaxis()

    # Dibujar cada operación como una barra en el gráfico
    for i, tarea in enumerate(datos_gantt):
        for op in tarea:
            rect = patches.Rectangle(
                (op['inicio'], op['maquina'] - 0.4),  # Posición (x, y)
                op['duracion'],                      # Ancho
                0.8,                                 # Alto
                facecolor=colores(i),
                edgecolor='black',
                linewidth=0.5
            )
            ax.add_patch(rect)
            
            # Etiqueta dentro de la barra: Tarea,Operación (ej. T1,O2)
            label = f"T{op['tarea_num']},O{op['actividad_num']}"
            ax.text(
                op['inicio'] + op['duracion'] / 2,
                op['maquina'],
                label,
                ha='center', va='center', color='white',
                fontsize=9, fontweight='bold'
            )

    # Línea vertical para marcar el makespan
    ax.axvline(x=makespan, color='r', linestyle='--', linewidth=2, label=f'Makespan: {makespan:.2f}')
    
    # Crear leyenda de colores para las tareas
    handles = [patches.Patch(color=colores(i), label=f'Tarea {i+1}') for i in range(len(datos_gantt))]
    ax.legend(handles=handles + [ax.get_lines()[0]], loc='upper right', fontsize='small')

    plt.tight_layout()
    plt.show()