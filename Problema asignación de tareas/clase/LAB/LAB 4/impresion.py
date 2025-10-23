from IPython.display import display, Math
import numpy as np

def mostrar_matriz_en_latex(matriz, columnas_resaltadas=None, color="blue"):
    """
    Muestra una matriz en formato LaTeX dentro de Jupyter Notebook, 
    resaltando opcionalmente varias columnas.

    Parámetros:
    -----------
    matriz : list[list] o np.ndarray
        Matriz de entrada (lista de listas o array de numpy).
    
    columnas_resaltadas : list[int] o None
        Lista de índices (basados en 0) de las columnas a resaltar. 
        Si es None o una lista vacía, no se resalta ninguna.
    
    color : str
        Color usado para resaltar las columnas (por defecto 'blue').
    """

    # Convertir a array de NumPy por comodidad
    matriz = np.array(matriz)

    # Asegurar que columnas_resaltadas sea lista o conjunto
    if columnas_resaltadas is None:
        columnas_resaltadas = set()
    else:
        columnas_resaltadas = set(columnas_resaltadas)  # más eficiente para búsquedas

    filas_latex = []
    for fila in matriz:
        celdas = []
        for j, elem in enumerate(fila):
            # Resaltar si la columna está en la lista
            if j in columnas_resaltadas:
                celda = f"\\textcolor{{{color}}}{{\\mathbf{{{elem}}}}}"
            else:
                celda = str(elem)
            celdas.append(celda)
        filas_latex.append(" & ".join(celdas))
    
    cuerpo = " \\\\ ".join(filas_latex)

    latex_code = (
        r"\begin{bmatrix}"
        + cuerpo +
        r"\end{bmatrix}"
    )

    display(Math(latex_code))