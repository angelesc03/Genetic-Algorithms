import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import to_rgba

# Datos de ejemplo para el horario (schedule)
# Estructura: lista de tareas (jobs), cada tarea tiene una lista de actividades (operations)
# Cada actividad: {'maquina': indice (0 para M1, etc.), 'duracion': float/int, 'inicio': float/int, 'actividad_num': int}
# Las 'inicio' deben ser calculadas previamente por tu algoritmo de scheduling
#tareas = [
    # Tarea 1 con 3 actividades
#    [
#        {'maquina': 0, 'duracion': 2.2, 'inicio': 0.5, 'actividad_num': 1},  # T(1,1) en M1 de 0 a 2
#        {'maquina': 1, 'duracion': 3, 'inicio': 2, 'actividad_num': 2},  # T(2,1) en M2 de 2 a 5 (asumiendo secuencia)
#        {'maquina': 3, 'duracion': 1, 'inicio': 5, 'actividad_num': 3},  # T(3,1) en M1 de 5 a 6
#    ],
#    # Tarea 2 con 2 actividades
#    [
#        {'maquina': 1, 'duracion': 4, 'inicio': 0, 'actividad_num': 1},  # T(1,2) en M2 de 0 a 4
#        {'maquina': 4, 'duracion': 2, 'inicio': 6, 'actividad_num': 2},  # T(2,2) en M1 de 6 a 8 (después de T(3,1))
#    ],
#    # Tarea 3 con 1 actividad
#    [
#        {'maquina': 2, 'duracion': 2, 'inicio': 5, 'actividad_num': 1},  # T(1,3) en M2 de 5 a 7 (después de T(2,1), con idle de 4-5)
#    ],
#]


# ------> Prueba con el ejercicio propuesto 
tareas = [
    # Tarea 1 con 3 actividades 
    [ 
        {'maquina': 0, 'duracion': 5.2, 'inicio':0, 'actividad_num':1},
        {'maquina': 1, 'duracion': 7.8, 'inicio':5.2, 'actividad_num':2},
        {'maquina': 1, 'duracion': 5.5, 'inicio':13, 'actividad_num':3},  
    ],
    # Trabajo 2 con 2 actividades
    [
        {'maquina': 0, 'duracion': 3.1, 'inicio':5.2, 'actividad_num':1},
        {'maquina': 2, 'duracion': 6.2, 'inicio':0, 'actividad_num':2},
    ],
    # Trabajo 3 con 3 actividades
    [
        {'maquina': 0, 'duracion': 2.5, 'inicio':8.3, 'actividad_num':1},
        {'maquina': 2, 'duracion': 6.2, 'inicio':6.2, 'actividad_num':2},
        {'maquina': 2, 'duracion': 2.2, 'inicio':12.4, 'actividad_num':3}, 
    ],
    #Trabajo 4 con 1 actividad 
    [
        {'maquina': 1, 'duracion':3.1, 'inicio':18.5, 'actividad_num':1},
    ],
]


# Número de máquinas (detectado automáticamente del máximo índice de máquina)
num_maquinas = max(max(actividad['maquina'] for actividad in tarea) for tarea in tareas) + 1
maquinas = [f'Máquina {i+1}' for i in range(num_maquinas)]

# Calcular makespan (tiempo total máximo)
makespan = max(max(actividad['inicio'] + actividad['duracion'] for actividad in tarea) for tarea in tareas)

# Colores por tarea (cada tarea tiene un color único para todas sus actividades)
colores_tareas = plt.cm.tab10(np.linspace(0, 1, len(tareas)))

# Configurar la figura
fig, ax = plt.subplots(figsize=(12, num_maquinas * 1.5 + 1))  # Ajustar altura según número de máquinas
ax.set_ylim(0, num_maquinas)
ax.set_xlim(0, makespan + 1)
ax.set_yticks(np.arange(num_maquinas) + 0.5)
ax.set_yticklabels(maquinas)
ax.set_xlabel('Tiempo (unidades)')
ax.set_ylabel('Máquinas')
ax.set_title('Visualizador de Asignación de Tareas a Máquinas')
ax.grid(True, axis='x', linestyle='--', alpha=0.7)

# Graficar cada actividad como un rectángulo
for tarea_idx, tarea in enumerate(tareas):
    color = colores_tareas[tarea_idx]
    for actividad in tarea:
        # Dibujar barra (rectángulo)
        rect = patches.Rectangle(
            (actividad['inicio'], actividad['maquina']), 
            actividad['duracion'], 1, 
            linewidth=1, edgecolor='black', facecolor=color
        )
        ax.add_patch(rect)
        
        # Etiqueta en el centro: T(a,b) donde a=actividad_num, b=tarea_idx+1
        label = f'T({actividad["actividad_num"]},{tarea_idx+1})'
        ax.text(
            actividad['inicio'] + actividad['duracion']/2, 
            actividad['maquina'] + 0.5, 
            label, 
            ha='center', va='center', color='white', fontweight='bold'
        )

# Crear leyenda: un patch por tarea con color y nombre "Tarea b"
handles = []
for tarea_idx in range(len(tareas)):
    color = colores_tareas[tarea_idx]
    handles.append(patches.Patch(color=color, label=f'Tarea {tarea_idx+1}'))
ax.legend(handles=handles, loc='upper right', title='Leyenda de Tareas')

# Línea para makespan
ax.axvline(x=makespan, color='red', linestyle='--', label=f'Makespan: {makespan}')
ax.legend(handles=handles + [ax.get_lines()[-1]], loc='upper right', title='Leyenda')

# Ajustar márgenes
plt.tight_layout()
plt.show()