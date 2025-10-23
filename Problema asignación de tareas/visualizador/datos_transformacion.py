#####################################################################################################
#       datos_transformación.py 
#       Código que contiene las funciones para poder transformar la estructura del vector de salida    
#           del algoritmo genético en un formato de listas-diccionarios para pasar como argumento  
#           al visualizador de tareas
#####################################################################################################


import numpy as np
import re

# ---> Funcion para cargar los datos y devolverlos como un array de numpy 

def cargar_matriz_operaciones_maquina(archivo):
    """
    Devuelve en una matriz numpy los datos que 
    relacionan las operaciones con las máquinas\n 
    Filas = Operacion_1, Operacion_2,...,Operacion_N\n
    Columnas = Maquina_1, Maquina_2, ..., Maquina_N \n.

    Parámetros:
    -----------
    archivo : str
        Cadena con la dirección de la ruta en donde están los datos.

    Retorna:
    --------
    np.ndarray
        Un array de NumPy con valores que relacionan operaciones-maquinas
    """
    with open(archivo, 'r') as f:
        lineas = f.readlines()
        
    datos = []
    for linea in lineas:
        valores = linea.strip().split(',')
        fila = [float(val.strip().replace(',', '.')) for val in valores]
        datos.append(fila)
    
    matriz = np.array(datos)
    return matriz


# ---> Funcion para cargar los datos de cada una de las operaciones por tarea 
def cargar_matriz_oepraciones_tareas(archivo):
    """
    Devuelve en una lista de listas con los datos que 
    relacionan las operaciones con las tareas\n 
    Filas = Tarea_1, Tarea_2,...,Tarea_N\n
    Columnas = Operacion_1, Operacion_2, ..., Operacion_M \n.

    Parámetros:
    -----------
    archivo : str
        Cadena con la dirección de la ruta en donde están los datos.

    Retorna:
    --------
    lst
        Una lista de listas con los valores tareas-operaciones
    """
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    filas = []
    
    for linea in lineas:
        # Limpiar la línea: quitar espacios, llaves y el "Tn ="
        linea = linea.strip().replace('{', '').replace('}', '')
        # Extraer los "On" (e.g., O1, O2) usando regex
        valores = re.findall(r'O(\d+)', linea)
        # Convertir a enteros y agregar como fila
        fila = [int(val) for val in valores]
        filas.append(fila)
    
    # Retornar la lista de listas
    return filas




##############################################################
# Supóngase el vector de prueba 
# [1,2,2,1,3,1,3,3,2]

# Los datos a obtener son:
# --> Máquina en la que
#
#
#


def transformar_datos_visualizador(mtx_oper_mach, mtx_oper_tsk, vector_gen):
    # Genearando la lista general que contendrá todos los datos
    arreglo_visualizador = [[] for i in range(len(mtx_oper_mach))]

    # LLenando cada una de las listas con los valores
    for tarea in mtx_oper_tsk:
        for operacion in tarea:
            
