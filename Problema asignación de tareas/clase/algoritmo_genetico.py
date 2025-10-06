#########################################################################
#           FUNCIONES PARA EL ALGORITMO GENÉTICO 
#########################################################################



# PARTES DE UN ALGORITMO GENÉTICO 

##
# 1. INICIALIZACIÓN: Crear una población inicial de soluciones aleatorias 
# 2. EVALUACIÓN: Calcular la aptitud de cada individuo en la población utilizando la función objetivo 
# 3. SELECCIÓN:  Elegir a los individuos para su reproducción según su aptitud 
# 4. CRUZA: Combinar a los individuos para generar descendiente
# 5. MUTACIÓN: Introducir pequeñas modificaciones en los descendientes para mantener la diversidad genética
# 6. REEMPLAZO: Formar una nueva generación con los nuevos descendientes, reemplazo total o reemplazo parcial
# 7. REPETICIÓN: Continuar el proceso hasta que se cumpla el criterio de paro#
# #


# ---- Importación de bibliotecas 
import numpy as np 
import random
from NSGAII import *


# ---------------------- INICIALIZACIÓN ------------------
import random

def generar_cromosoma_random(n, limite_inferior=1, limite_superior=4):
    """
    Genera una lista de tamaño n con valores enteros aleatorios entre limite_inferior y limite_superior (inclusive).
    
    Parámetros:
        n (int): Tamaño de la lista.
        limite_inferior (int): Límite inferior del intervalo.
        limite_superior (int): Límite superior del intervalo.
    
    Retorna:
        list: Lista de n enteros aleatorios en el intervalo [limite_inferior, limite_superior].
    """
    if n < 0:
        return []  # Retorna lista vacía si n es negativo
    if limite_inferior > limite_superior:
        raise ValueError("El límite inferior no puede ser mayor que el límite superior")
    
    return [random.randint(limite_inferior, limite_superior) for _ in range(n)]



def generar_poblacion_inicial(tam_poblacion, len_cromosoma, mtx_op_t, mtx_op_e, l_tsk_oper):
    poblacion = [ ]
    for _ in range(0,tam_poblacion):
        cromosoma = generar_cromosoma_random(len_cromosoma)
        aptitud = evaluar_fitness(cromosoma, mtx_op_t, mtx_op_e, l_tsk_oper)
        X = [cromosoma, aptitud]
        poblacion.append(X)
    return poblacion


# ----------------------- EVALUACION -----------------------

def evaluar_fitness(vec_solucion, mtx_op_t, mtx_op_e, l_tsk_oper):
    """_summary_

    Args:
        vec_solucion (_type_): _description_
        mtx_op_t (_type_): _description_
        mtx_op_e (_type_): _description_
        l_tsk_oper (_type_): _description_

    Returns:
        numpy.ndarray: Un array de dos dimensiones. La primera representa el cálculo del makespan y el segundo 
        cálculo del consumo total de energía
    """

    num_tareas = len(l_tsk_oper)
    num_maquinas = len(mtx_op_t[0])
    tiemp_maquinas = [0.0] * num_maquinas  # Reloj de cada máquina
    tiemp_tareas = [0.0] * num_tareas      # Reloj de cada tarea

    energia_consumida = 0.0

    vec_solucion = np.array(vec_solucion)

    idx_op_maq = 0 # Obtiene la máquina del vector original
    for i in range(len(l_tsk_oper)): # Recorriendo cada tarea
        for j in range(len(l_tsk_oper[i])): # Recorriendo la operación J de la tarea I 
            maquina = vec_solucion[idx_op_maq]
            operacion = l_tsk_oper[i][j]
            
            energia_consumida += mtx_op_e[operacion-1][maquina-1] 
            duracion = mtx_op_t[operacion-1][maquina-1] # Obtener la duracion de la operacion en proceso 

            
            tiempo_fin_op_anterior = tiemp_tareas[i]
            tiempo_maquina_libre = tiemp_maquinas[maquina-1]
            
            # El tiempo de inicio es el MÁXIMO de los dos anteriores.
            tiempo_inicio = max(tiempo_fin_op_anterior, tiempo_maquina_libre)
            
            # El tiempo de fin de la operación actual
            tiempo_fin_actual = tiempo_inicio + duracion
            
           

            # --- CAMBIO 3: Actualizar los "relojes" ---
            # Actualizamos el reloj de la máquina y de la tarea con el tiempo de finalización.
            tiemp_maquinas[maquina-1] = tiempo_fin_actual
            tiemp_tareas[i] = tiempo_fin_actual
            
            idx_op_maq += 1

    # Cálculo Final del Makespan ---
    # El makespan es el tiempo en que la ÚLTIMA máquina termina.
    makespan = max(tiemp_maquinas)

    return np.array([makespan, energia_consumida])


# ----------------------- SELECCIÓN -----------------------

def seleccion_por_torneo(poblacion, k, modo_optimizacion="minimize"):
    """
    Selecciona padres mediante torneo, usando dominancia de Pareto.

    Args:
        poblacion (list): La población actual. Formato: [[cromosoma], [fit1, fit2]].
        k (int): El tamaño del torneo.
        modo_optimizacion (str): "minimize" o "maximize", para la función de dominancia.

    Returns:
        list: Una lista con los ÍNDICES de los individuos seleccionados como padres.
    """
    padres_seleccionados = []
    num_selecciones = len(poblacion)
    
    # Realizar un torneo por cada padre que necesitemos
    for _ in range(num_selecciones):
        
        # 1. Seleccionar k competidores al azar
        indices_participantes = random.sample(range(len(poblacion)), k)
        
        # 2. Encontrar las soluciones no dominadas DENTRO del grupo de competidores
        indices_no_dominados = []
        
        for idx_A in indices_participantes:
            es_dominado = False
            fitness_A = poblacion[idx_A][1]
            
            for idx_B in indices_participantes:
                if idx_A == idx_B:
                    continue
                
                fitness_B = poblacion[idx_B][1]
                
                # Comprobar si el individuo B domina al individuo A
                if dominancia_pareto(fitness_B, fitness_A, modo_optimizacion) == 1:
                    es_dominado = True
                    break # Si A es dominado por alguien, ya no puede ser ganador.
            
            # Si después de todas las comparaciones nadie dominó a A, es un ganador potencial.
            if not es_dominado:
                indices_no_dominados.append(idx_A)
        
        # 3. Elegir un ganador de entre los no dominados
        if indices_no_dominados:
            # Si hay uno o más no dominados, se elige uno al azar.
            indice_ganador = random.choice(indices_no_dominados)
        else:
            # Caso raro: si todos se dominan mutuamente (no debería pasar con Pareto)
            # o si k=1, simplemente elegimos uno al azar del grupo original.
            indice_ganador = random.choice(indices_participantes)
            
        padres_seleccionados.append(indice_ganador)
        
    # 4. Asegurarse de que el número de padres sea par
    if len(padres_seleccionados) % 2 != 0:
        padres_seleccionados.append(random.choice(range(len(poblacion))))
        
    return padres_seleccionados



# --------------------------------------- CRUZA ---------------------------------------------------
def cruza_n_puntos(p1, p2, n_puntos):
    """
    Realiza una cruza de n puntos entre dos padres (p1 y p2) para generar dos hijos.

    En una cruza de n puntos, se eligen n posiciones de corte al azar dentro de la longitud
    de los padres (excluyendo los extremos), y se alternan segmentos entre ambos padres 
    para generar los hijos.

    Parameters
    ----------
    p1 : list
        Primer padre, representado como una lista de genes.
    p2 : list
        Segundo padre, también una lista de la misma longitud que p1.
    n_puntos : int
        Número de puntos de cruce. Debe ser menor que la longitud de los padres.

    Returns
    -------
    h1 : list
        Primer hijo, resultado de la cruza.
    h2 : list
        Segundo hijo, resultado de la cruza.

    Raises
    ------
    ValueError
        Si los padres no tienen la misma longitud o si `n_puntos` no es válido.
    """
    if len(p1) != len(p2):
        raise ValueError("Los padres deben tener la misma longitud.")
    if n_puntos < 1 or n_puntos >= len(p1):
        raise ValueError("El número de puntos de cruce debe ser entre 1 y len(p1) - 1.")

    # -- Elección de puntos de cruza sin considerar los extremos
    puntos = sorted(random.sample(range(1, len(p1)), n_puntos))

    # Agregar los extremos para facilitar la división por segmentos
    puntos = [0] + puntos + [len(p1)]

    h1, h2 = [], []

    # Alternar segmentos entre padres
    for i in range(len(puntos) - 1):
        inicio = puntos[i]
        fin = puntos[i + 1]
        if i % 2 == 0:
            h1 += p1[inicio:fin]
            h2 += p2[inicio:fin]
        else:
            h1 += p2[inicio:fin]
            h2 += p1[inicio:fin]

    return h1, h2


def crearHijos(pobl_padres, idx_padres, pCruza, nPtosCruza, mtx_op_t, mtx_op_e, l_tsks):
    """_summary_

    Args:
        pobl_padres (list): Conjunto origial de padres el cual tiene el formato [[cromosoma], [f1, f2]]
        idx_padres (list): Indice de los individuos que se cruzaran resultado del proceso de selección.
        pCruza (int): Porcentaje de cruza
        nPtosCruza (int): Numero de puntos para hacer la recombinación de cromosomas
        mtx_op_t (list): matriz con la relación de operaciones-tiempo 
        mtx_op_e (list): matriz con la relación de operaciones-energía
        l_tsks (list): lista con las tareas que se realizan

    Returns:
        hijos: list
              Lista con los hijos creados en el mismo formato que los padres
    """
    tam_poblacion = len(idx_padres)
    hijos = [ ]
    j = 0
    while j < tam_poblacion:
        idx_p1 = idx_padres[j]
        idx_p2 = idx_padres[j+1]
        if random.uniform(0,1) <= pCruza:
            p1 = pobl_padres[idx_p1][0]
            p2 = pobl_padres[idx_p2][0]

            h1_crom, h2_crom = cruza_n_puntos(p1, p2, nPtosCruza)
            H1 = [h1_crom, evaluar_fitness(h1_crom, mtx_op_t, mtx_op_e, l_tsks)]
            H2 = [h2_crom, evaluar_fitness(h2_crom, mtx_op_t, mtx_op_e, l_tsks)]
            hijos.append(H1)
            hijos.append(H2)
        j += 2
    return hijos

# ------------------------------------- MUTACION --------------------------------------
def mutar_poblacion_por_desplazamiento(poblacion_hijos, porc_muta, mtx_op_t, mtx_op_e, l_tsks):
    """
    Aplica la mutación por desplazamiento a una población de hijos.

    Args:
        poblacion_hijos (list): La población de hijos a mutar.
                                Formato: [[cromosoma], [fit1, fit2]].
        porc_muta (float): El porcentaje de mutación (ej. 0.05 para 5%).

    Returns:
        list: La misma lista de la población de hijos, con las mutaciones aplicadas.
    """
    counter = 0
    for hijo in poblacion_hijos:
        if random.uniform(0, 1) <= porc_muta:
            counter += 1
            
            cromosoma = hijo[0]
            n = len(cromosoma)

            # 1. Se selecciona un segmento S entre dos índices aleatorios i y j
            if n > 1:
                inicio, fin = sorted(random.sample(range(n), 2))
                segmento = cromosoma[inicio : fin + 1]
                
                # 2. Eliminar el segmento del cromosoma
                # Se crea una lista temporal con los elementos restantes
                resto_cromosoma = cromosoma[:inicio] + cromosoma[fin + 1:]
                
                # 3. Seleccionar una nueva posición k para la inserción
                # La nueva posición puede ser desde el inicio (0) hasta el final
                nueva_pos = random.randint(0, len(resto_cromosoma))
                
                # 4. Insertar el segmento S en la posición k
                cromosoma_mutado = resto_cromosoma[:nueva_pos] + segmento + resto_cromosoma[nueva_pos:]
                
                # Se actualiza el cromosoma del hijo con su versión mutada
                hijo[0] = cromosoma_mutado
                hijo[1] = evaluar_fitness(hijo[0], mtx_op_t, mtx_op_e, l_tsks)
    return poblacion_hijos



# ------------------------------- REEMPLAZO ---------------------------
def nueva_poblacion(poblacion_combinada, tam_poblacion):

    nueva_poblacion = [ ]
    poblacion_comb_fitness = [ ]
    contador_poblacion = 0
    idx_frente_corte = 0
    for i in range(len(poblacion_combinada)):
        poblacion_comb_fitness.append(poblacion_combinada[i][1])
    
    # Obtener los diferenes frentes de pareto
    frentes_P, frentes_P_idxs = fast_non_dominated_sort(poblacion_comb_fitness, "minimize")

    for frente in frentes_P_idxs:
        if contador_poblacion + len(frente) <= tam_poblacion:
            for j in frente:
                nueva_poblacion.append(poblacion_combinada[j])
            contador_poblacion = contador_poblacion + len(frente)
            idx_frente_corte += 1
        else:  # ---> Aplicar el criterio de la distancia de crowding
            idx_frente_corte # El frente que ya no se sumó
            # ---> Aplicando distancia de crowding:
            #print(f"Se le está pasando a la función: {frentes_P[idx_frente_corte]}")
            vec_crowding, vec_crowding_idxs= sobrevivientes_dist_crowding(frentes_P[idx_frente_corte], tam_poblacion-contador_poblacion)
            for indice in vec_crowding_idxs:
                indice_real = frentes_P_idxs[idx_frente_corte][indice]
                #print(f"El valor de índice real es: {indice_real}")
                #print(f"Se intenta--> nuevapoblacion.append(poblacion_combinada[{indice_real}])")
                nueva_poblacion.append(poblacion_combinada[indice_real])
            break
    #print(f"Se completo la seleccion, el tamaño de la población nueva es : {len(nueva_poblacion)}")
    return nueva_poblacion, frentes_P, vec_crowding, idx_frente_corte+1
