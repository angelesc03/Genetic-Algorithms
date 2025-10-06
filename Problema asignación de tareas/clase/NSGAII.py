import numpy as np


#--------------------------- DOMINANCIA DE PARETO ------------------------------------

def dominancia_pareto(U, V, modo="minimize"):
    """
    Determina la relación de dominancia entre dos vectores U y V.
    
    Args:
    - U (list): Vector n-dimensional.
    - V (list): Vector n-dimensional (mismo tamaño que U).
    - modo (str): "minimize" o "maximize".
    
    Returns:
    - 1 si U domina a V.
    - 2 si V domina a U.
    - 3 si ninguno domina al otro.
    """
    if len(U) != len(V):
        raise ValueError("Los vectores U y V deben tener la misma longitud.")
    
    if modo not in ["minimize", "maximize"]:
        raise ValueError("El modo debe ser 'minimize' para minimización o 'maximize' para maximización.")
    
    if modo == "minimize":
        u_domina_v = all(u <= v for u, v in zip(U, V)) and any(u < v for u, v in zip(U, V))
        v_domina_u = all(v <= u for v, u in zip(V, U)) and any(v < u for v, u in zip(V, U))
    else:  
        u_domina_v = all(u >= v for u, v in zip(U, V)) and any(u > v for u, v in zip(U, V))
        v_domina_u = all(v >= u for v, u in zip(V, U)) and any(v > u for v, u in zip(V, U))
    
    if u_domina_v:
        return 1
    elif v_domina_u:
        return 2
    else:
        return 3


# ------------------------------  Fast-non-dominated sort -------------------------------------------
def fast_non_dominated_sort(vectores, modo="minimize"):
    """
    Ordena un conjunto de vectores de acuerdo a la dominancia de Pareto (NSGA-II).

    Args:
        vectores (list): Una lista de vectores de fitness.
        modo (str): "minimize" o "maximize".

    Returns:
        tuple: Una tupla con dos elementos:
               1. (list): La lista de frentes con los VECTORES de fitness.
               2. (list): La lista de frentes con los ÍNDICES originales de esos vectores.
    """
    n_vectores = len(vectores)
    
    soluciones_dominadas = [[] for _ in range(n_vectores)]
    contador_dominancia = [0] * n_vectores
    
    # --- Paso 1: Calcular S_p y n_p ---
    for i in range(n_vectores):
        for j in range(n_vectores):
            if i == j:
                continue
            
            relacion = dominancia_pareto(vectores[i], vectores[j], modo)
            
            if relacion == 1: # i domina a j
                soluciones_dominadas[i].append(j)
            elif relacion == 2: # j domina a i
                contador_dominancia[i] += 1
    
    # --- Paso 2: Identificar el primer frente (n_p = 0) ---
    # Esta variable ahora contendrá los frentes con los índices
    frentes_con_indices = [[]]
    for i in range(n_vectores):
        if contador_dominancia[i] == 0:
            frentes_con_indices[0].append(i)
            
    # --- Paso 3: Construir los frentes sucesivos ---
    k = 0
    while frentes_con_indices[k]:
        Q = []
        for i in frentes_con_indices[k]:
            for j in soluciones_dominadas[i]:
                contador_dominancia[j] -= 1
                if contador_dominancia[j] == 0:
                    Q.append(j)
        
        k += 1
        if Q:
            frentes_con_indices.append(Q)
        else:
            break
            
    # --- Paso 4: Formatear la salida para tener AMBOS resultados ---
    # 1. Crear la lista de frentes con los vectores (como en la versión original)
    frentes_con_vectores = []
    for frente_indices in frentes_con_indices:
        vectores_frente = [vectores[i] for i in frente_indices]
        frentes_con_vectores.append(vectores_frente)
        
    return frentes_con_vectores, frentes_con_indices

# ------------------------ CROWDING-DISTANCE ASSIGNMENT -------------------------------------
def crowding_distance(poblacion_soluciones):
    """
    Calcula la distancia de crowding para un conjunto de soluciones en un frente.
    Esta versión está corregida para evitar errores de índice.
    """
    # Convierte a lista de listas si son arrays de numpy, para consistencia
    poblacion_soluciones = [list(sol) for sol in poblacion_soluciones]

    l = len(poblacion_soluciones)
    if l <= 2:
        # Si hay 2 o menos soluciones, todas son extremos y su distancia es infinita
        return [10000] * l

    num_obj = len(poblacion_soluciones[0])
    distancias = [0.0 for _ in range(l)]

    for i in range(num_obj):
        # Ordenamos los índices de las soluciones según el objetivo 'i'
        indices_ordenados = sorted(range(l), key=lambda j: poblacion_soluciones[j][i])
        
        # Asignamos una distancia infinita a las soluciones extremas para este objetivo
        # Esto asegura que los puntos en los bordes del frente de Pareto sean preferidos
        distancias[indices_ordenados[0]] = 10000
        distancias[indices_ordenados[-1]] = 10000

        # Obtenemos los valores mínimo y máximo para normalizar
        f_min = poblacion_soluciones[indices_ordenados[0]][i]
        f_max = poblacion_soluciones[indices_ordenados[-1]][i]
        rango = f_max - f_min

        # Si el rango es cero, no se puede calcular la distancia para este objetivo
        if rango == 0:
            continue

        # Calculamos la distancia para las soluciones intermedias
        for j in range(1, l - 1):
            # Índice original del individuo actual en la lista ordenada
            idx_original = indices_ordenados[j]
            
            # Valor del objetivo del vecino anterior en la lista ordenada
            valor_anterior = poblacion_soluciones[indices_ordenados[j-1]][i]

            # Valor del objetivo del vecino siguiente en la lista ordenada
            valor_siguiente = poblacion_soluciones[indices_ordenados[j+1]][i]
            
            # Acumulamos la distancia normalizada
            distancias[idx_original] += (valor_siguiente - valor_anterior) / rango

    return distancias

# ------------------- SOBREVIVIENTES POR DISTANCIA DE CROWDING --------------------------------
def sobrevivientes_dist_crowding(vec_frente, n_sobrevivientes):
    """_summary_

    Args:
        vec_frente (list): Conjunto de vectores con los valores del fitness para cada objetivo dentro de frente de pareto correspondiente
                           para ajustar el tamaño de la población.
        n_sobrevivientes (int): Valor que indica cuáles soluciones sobrevivirán. 
    
    Returns:
        soluciones (list): Lista con los vectores de las soluciones que sobrevirián
        indices (list): Lista con los índices de las soluciones que sobrevivirán
    """
    #print(f"Iniciando el proceso de calcular la distancia de crowding")
    distancias_crowding = crowding_distance(vec_frente)
    #print(f"El proceso de calculo para la distancia de crowding terminó correctamente")
    #print(f"Las distancias de crowding para los vectores son: {distancias_crowding}")
    indices = sorted(range(len(distancias_crowding)), key=lambda i: distancias_crowding[i], reverse=True)[:n_sobrevivientes]
    soluciones = [vec_frente[i] for i in indices]

    return soluciones, indices

