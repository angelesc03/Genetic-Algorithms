# ----------------- IMPORTACIÓN DE LIBRERÍAS NECESARIAS ----------------------
import numpy as np 
import random 
from impresion import *



def cruza_n_puntos_poliploides(padre1, padre2, n_puntos):
    """
    Realiza una cruza de n puntos entre dos padres poliploides para generar dos hijos poliploides.
    
    Parameters
    ----------
    padre1 : list of lists
        Primer padre poliploide, representado como lista de cromosomas (cada cromosoma es una lista).
    padre2 : list of lists
        Segundo padre poliploide, misma estructura que padre1.
    n_puntos : int
        Número de puntos de cruce. Debe ser menor que la longitud de los cromosomas.
    
    Returns
    -------
    hijo1 : list of lists
        Primer hijo poliploide.
    hijo2 : list of lists
        Segundo hijo poliploide.
    
    Raises
    ------
    ValueError
        Si los padres no tienen la misma estructura o si n_puntos no es válido.
    """
    padre1, padre2 = list(padre1), list(padre2)
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener el mismo número de cromosomas")
    
    longitud_cromosoma = len(padre1[0])
    for i in range(len(padre1)):
        if len(padre1[i]) != longitud_cromosoma or len(padre2[i]) != longitud_cromosoma:
            raise ValueError("Todos los cromosomas deben tener la misma longitud")
    
    if n_puntos < 1 or n_puntos >= longitud_cromosoma:
        raise ValueError(f"n_puntos debe estar entre 1 y {longitud_cromosoma - 1}")
    
    puntos_cruza = sorted(random.sample(range(1, longitud_cromosoma), n_puntos))
    
    # Agregar extremos para facilitar el procesamiento
    puntos = [0] + puntos_cruza + [longitud_cromosoma]
    
    # Inicializar hijos como listas vacías de cromosomas
    hijo1 = [[] for _ in range(len(padre1))]
    hijo2 = [[] for _ in range(len(padre2))]
    
    # Se realiza la cruza entre segmentos a nivel de columnas
    for segmento in range(len(puntos) - 1):
        inicio = puntos[segmento]
        fin = puntos[segmento + 1]
        
        if segmento % 2 == 0:
            for cromosoma in range(len(padre1)):
                hijo1[cromosoma].extend(padre1[cromosoma][inicio:fin])
                hijo2[cromosoma].extend(padre2[cromosoma][inicio:fin])
        else:
            for cromosoma in range(len(padre1)):
                hijo1[cromosoma].extend(padre2[cromosoma][inicio:fin])
                hijo2[cromosoma].extend(padre1[cromosoma][inicio:fin])
    
    print("PADRE 1 --->")
    mostrar_matriz_en_latex(padre1, [])
    print("PADRE 2 --->")
    mostrar_matriz_en_latex(padre2, [])
    print("HIJO 1 --->")
    mostrar_matriz_en_latex(hijo1, [])
    print("HIJO 2 --->")
    mostrar_matriz_en_latex(hijo2, [ ])
    return np.array(hijo1), np.array(hijo2)



# -----------------> Funcion para cruzar por fila 
def cruza_n_puntos_por_fila(padre1, padre2, n_puntos):
    """
    Realiza una cruza de n puntos por FILA entre dos padres poliploides.
    Cada cromosoma se cruza independientemente con puntos de corte diferentes.
    
    Parameters
    ----------
    padre1 : list of lists
        Primer padre poliploide.
    padre2 : list of lists  
        Segundo padre poliploide.
    n_puntos : int
        Número de puntos de cruce por cromosoma.
    
    Returns
    -------
    hijo1 : list of lists
        Primer hijo poliploide.
    hijo2 : list of lists
        Segundo hijo poliploide.
    """
    
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener el mismo número de cromosomas")
    
    longitud_cromosoma = len(padre1[0])
    for i in range(len(padre1)):
        if len(padre1[i]) != longitud_cromosoma or len(padre2[i]) != longitud_cromosoma:
            raise ValueError("Todos los cromosomas deben tener la misma longitud")
    
    if n_puntos < 1 or n_puntos >= longitud_cromosoma:
        raise ValueError(f"n_puntos debe estar entre 1 y {longitud_cromosoma - 1}")
    
    # Inicializar hijos
    hijo1 = [[] for _ in range(len(padre1))]
    hijo2 = [[] for _ in range(len(padre2))]
    
    # Cruza INDEPENDIENTE para cada cromosoma (fila)
    for cromosoma_idx in range(len(padre1)):
        # Elegir puntos de corte DIFERENTES para cada cromosoma
        puntos_cruza = sorted(random.sample(range(1, longitud_cromosoma), n_puntos))
        puntos = [0] + puntos_cruza + [longitud_cromosoma]
        
        h1_temp, h2_temp = [], []
        
        # Realizar cruza para este cromosoma específico
        for segmento in range(len(puntos) - 1):
            inicio = puntos[segmento]
            fin = puntos[segmento + 1]
            
            if segmento % 2 == 0:
                h1_temp.extend(padre1[cromosoma_idx][inicio:fin])
                h2_temp.extend(padre2[cromosoma_idx][inicio:fin])
            else:
                h1_temp.extend(padre2[cromosoma_idx][inicio:fin])
                h2_temp.extend(padre1[cromosoma_idx][inicio:fin])
        
        hijo1[cromosoma_idx] = h1_temp
        hijo2[cromosoma_idx] = h2_temp
    
    return hijo1, hijo2