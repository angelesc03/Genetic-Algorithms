# ##############################################################################
#                                  ALGORITMO GENÉTICO
# ############################################################################## 

# ---> Importar las bibliotecas necesarias 
import random 
import numpy as np 



# ************************* GENERACIÓN DE UNA POBLACIÓN ************************

# ---> Generación de una cadena aleatoria binaria 
def generar_cadena_binaria(longitud):
    """
    Genera un array de NumPy que contiene valores binarios (0 y 1) aleatorios.

    Parámetros:
    -----------
    longitud : int
        La longitud deseada para el array.

    Retorna:
    --------
    np.ndarray
        Un array de NumPy con valores de tipo entero de 8 bits (int8)
        que consiste en 0s y 1s.
    """
    if not isinstance(longitud, int) or longitud < 1:
        raise ValueError("La longitud debe ser un número entero positivo.")
    return np.random.randint(2, size=longitud, dtype=np.int8)



# ************************* EVALUACIÓN DE APTITUD  *****************************
def calcular_aptitud(poblacion, funcion_fitness_especifica, **kwargs):
    """
    Calcula la aptitud para cada cromosoma en la población usando
    una función de aptitud específica que se pasa como parámetro.

    Parámetros:
    -----------
    poblacion : list
        Una lista de cromosomas.
    funcion_fitness_especifica : function
        La función que se usará para calcular la aptitud.
    **kwargs : dict
        Argumentos adicionales necesarios para la función de aptitud específica.

    Retorna:
    --------
    list
        Una lista de los valores de aptitud calculados.
    """
    aptitudes = []
    for cromosoma in poblacion:
        aptitud = funcion_fitness_especifica(cromosoma, **kwargs)
        aptitudes.append(aptitud)
    return aptitudes

# *********************** SELECCIÒN DE CROMOSOMAS (PADRES) *********************

# *********************** OPERADORES DE CRUZA **********************************

# *********************** OPERADORES DE MUTACIÓN *******************************
