import pygame
import time
from clases import Laberinto, Agente, QLearningAgente, Metrica


ALTO, ANCHO = 800, 800


LABERINTO = Laberinto()

AGENTE = Agente(1,1)

Q_LEARNING = QLearningAgente(len(LABERINTO.estructura), len(LABERINTO.estructura[0]))

CLOCK = pygame.time.Clock()

METRICA = Metrica()

EPOCHS = 10000

def mostrar():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    ventana.fill((255,255,255))
    LABERINTO.dibujar(ventana)
    AGENTE.dibujar(ventana)
    pygame.display.flip()
    CLOCK.tick(5)


def entrenar(): #Entrenar al agente en el laberinto
    for epoch in range(EPOCHS):
        AGENTE.x, AGENTE.y = 1, 1
        total_recompensa = 0
        pared = 0
        inicio = time.time()
        while True:

            if epoch >= EPOCHS - 2: # Mostrar los últimos 2 entrenamientos
                mostrar()

            estado = (AGENTE.y, AGENTE.x)
            accion = Q_LEARNING.elegir_accion(estado)

            AGENTE.mover(accion)
            nuevo_estado = (AGENTE.y, AGENTE.x)

            check = time.time()

            if check - inicio >= 15 and epoch < 49:
                print(f"Agente en: ({AGENTE.x}, {AGENTE.y}) realizando acción: {accion}")


            recompensa = Q_LEARNING.calcular_recompensa(LABERINTO.estructura[AGENTE.y][AGENTE.x]) 
            total_recompensa += recompensa

            if recompensa == 10: #Ganaste
                fin = time.time()
                METRICA.agregar_tiempo(epoch, fin-inicio)
                METRICA.agregar_pared(epoch, pared)
                print(f'\n************ Epoch: {epoch + 1}. Tiempo de ejecución(s): {fin - inicio}. Pared: {pared} ********************\n')
                break
            elif recompensa == -100: #Pared
                pared += 1
                AGENTE.y, AGENTE.x = estado #Actualizar a estado anterior

            Q_LEARNING.actualizar_q(estado, accion, recompensa, nuevo_estado)


        Q_LEARNING.reducir_exploracion()
    Q_LEARNING.guardar_tabla()
    METRICA.plot()

def ejecutar(): #Ejecutar el agente en el laberinto
    estado_actual = AGENTE.y, AGENTE.x
    meta = (21,21)
    pasos = 0
    max_pasos = 100
    Q_LEARNING.set_explotacion_pura()
    
    while estado_actual != meta and pasos <= max_pasos:
        accion_optima = Q_LEARNING.elegir_accion(estado_actual)
        AGENTE.mover(accion_optima)

        if LABERINTO.estructura[AGENTE.y][AGENTE.x] == 1:
            AGENTE.x = estado_actual[1]
            AGENTE.y = estado_actual[0]
        else:
            estado_actual = AGENTE.y, AGENTE.x

        pasos += 1

        mostrar()


#Intercambiar entrenar() y ejecutar() según se requiera

entrenar()

#ejecutar()
