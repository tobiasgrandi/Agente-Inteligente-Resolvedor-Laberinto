import random
import numpy as np
import matplotlib.pyplot as plt

def inicializar_laberinto(filas, columnas):
    # Crear una matriz de paredes (1) para el laberinto
    laberinto = np.ones((filas, columnas), dtype=int)
    return laberinto

def dfs_generar_camino(laberinto, x, y):
    # Movimientos posibles (arriba, abajo, izquierda, derecha) en pasos de 2
    movimientos = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    random.shuffle(movimientos)  # Mezclar para generar caminos aleatorios

    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < laberinto.shape[0] and 0 <= ny < laberinto.shape[1] and laberinto[nx, ny] == 1:
            laberinto[x + dx // 2, y + dy // 2] = 0  # Elimina pared intermedia
            laberinto[nx, ny] = 0  # Marca el nuevo camino
            dfs_generar_camino(laberinto, nx, ny)

def agregar_bifurcaciones(laberinto, probabilidad_bifurcacion):
    filas, columnas = laberinto.shape
    for x in range(1, filas - 1, 2):
        for y in range(1, columnas - 1, 2):
            if laberinto[x, y] == 0:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if random.random() < probabilidad_bifurcacion:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < filas and 0 <= ny < columnas and laberinto[nx, ny] == 1:
                            laberinto[nx, ny] = 0  # Crear apertura para una bifurcación

def generar_laberinto_dificil(filas, columnas):
    laberinto = inicializar_laberinto(filas, columnas)
    # Empezar DFS desde una esquina para crear largos caminos
    dfs_generar_camino(laberinto, 1, 1)
    # Añadir bifurcaciones para aumentar la dificultad
    agregar_bifurcaciones(laberinto, probabilidad_bifurcacion=0.1)

    # Definir puntos de inicio y meta
    laberinto[1, 1] = 2       # Inicio
    laberinto[filas - 2, columnas - 2] = 3  # Meta
    return laberinto

def plot_laberinto(laberinto):
    plt.imshow(laberinto, cmap="Set3")
    plt.xticks([]), plt.yticks([])  # Ocultar ejes para claridad
    plt.show()

# Generar y mostrar un laberinto desafiante con inicio y meta
filas, columnas = 23, 23  # Dimensiones impares para asegurar caminos
laberinto_dificil = generar_laberinto_dificil(filas, columnas)
plot_laberinto(laberinto_dificil)

# Configurar NumPy para que muestre la matriz completa
np.set_printoptions(threshold=np.inf)

# Mostrar la matriz del laberinto completa
print(laberinto_dificil.tolist())
