import numpy as np
import pandas as pd
import pygame
import random
import matplotlib.pyplot as plt
import pickle
from estructura import ESTRUCTURA



class Dibujar:
    def __init__(self, ventana):
        self.ventana = ventana
        self.tam_celda = 35
        
        self.color_camino = (255,255,255)
        self.color_pared = (0,45,0)
        self.color_inicio = (0,255,0)
        self.color_meta = (255,0,0)
        self.color_agente = (0,0,255)

        self.camino = 0
        self.pared = 1
        self.inicio = 2
        self.meta = 3

    def dibujar_laberinto(self, estructura):
        for fila in range(len(estructura)):
            for col in range(len(estructura[fila])):
                x,y = col * self.tam_celda, fila * self.tam_celda
                match estructura[fila][col]:
                    case self.camino:
                        color = self.color_camino
                    case self.pared:
                        color = self.color_pared
                    case self.inicio:
                        color = self.color_inicio
                    case self.meta:
                        color = self.color_meta
                pygame.draw.rect(self.ventana, color, (x, y, self.tam_celda, self.tam_celda))

    def dibujar_agente(self, x, y):
        x, y = x * self.tam_celda, y * self.tam_celda
        pygame.draw.rect(self.ventana, self.color_agente, (x, y, self.tam_celda, self.tam_celda))


class Laberinto:

    def __init__(self):
        self.estructura = ESTRUCTURA

    def dibujar(self, ventana):
        dib = Dibujar(ventana)
        dib.dibujar_laberinto(self.estructura)


class Agente:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dibujar(self, ventana):
        dib = Dibujar(ventana)
        dib.dibujar_agente(self.x, self.y)

    def mover(self, direccion):
        match direccion:
            case 'arriba':
                self.y -= 1
            case 'abajo':
                self.y += 1
            case 'izquierda':
                self.x -=1
            case 'derecha':
                self.x += 1


class QLearningAgente:
    def __init__(self, filas_tabla, columnas_tabla):
        self.q_table = np.zeros((filas_tabla, columnas_tabla, 4))
        self.alpha = 0.1
        self.gamma = 0.7
        self.epsilon = 1.0
        self.recompensas = {'0': -1, #Camino
                            '1': -100, #Pared
                            '2': -1, #Inicio
                            '3': 10} #Meta

    def elegir_accion(self, estado):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        else:
            return ['arriba', 'abajo', 'izquierda', 'derecha'][np.argmax(self.q_table[estado])]
        
    def actualizar_q(self, estado, accion, recompensa, nuevo_estado):
        index_accion = ['arriba', 'abajo', 'izquierda', 'derecha'].index(accion)

        self.q_table[estado][index_accion] += self.alpha * (recompensa + self.gamma * np.max(self.q_table[nuevo_estado]) - self.q_table[estado][index_accion])

    def reducir_exploracion(self):
        if self.epsilon > 0.1:
            self.epsilon *= 0.9

    def calcular_recompensa(self, estado_siguiente):
        return self.recompensas[f'{estado_siguiente}']
    
    def guardar_tabla(self):
        with open('qtable.pkl', 'wb') as file:
            pickle.dump(self.q_table, file)

    def leer_tabla(self):
        with open('qtable.pkl', 'rb') as file:
            self.q_table = pickle.load(file)

    def set_explotacion_pura(self):
        self.leer_tabla()
        self.epsilon = 0


class Metrica:
    def __init__(self):
        self.tiempo = pd.DataFrame(columns=['Epoch', 'Tiempo'])
        self.pared = pd.DataFrame(columns=['Epoch', 'Pared'])

    def agregar_tiempo(self, epoch, tiempo):
        nuevo_dato = pd.DataFrame({'Epoch': [epoch], 'Tiempo': [tiempo]})
        self.tiempo = pd.concat([self.tiempo, nuevo_dato], ignore_index=True)

    def agregar_pared(self, epoch, pared):
        nuevo_dato = pd.DataFrame({'Epoch': [epoch], 'Pared': [pared]})
        self.pared = pd.concat([self.pared, nuevo_dato], ignore_index=True)

    def plot(self):

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))

        # Gráfico de 'Tiempo'
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Tiempo', color='tab:blue')
        ax1.plot(self.tiempo['Epoch'], self.tiempo['Tiempo'], color='tab:blue', label='Tiempo')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.set_title('Tiempo por Epoch')

        # Gráfico de 'Pared'
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Pared', color='tab:red')
        ax2.plot(self.pared['Epoch'], self.pared['Pared'], color='tab:red', label='Pared')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        ax2.set_title('Pared por Epoch')

        # Ajustar el layout para evitar solapamientos
        fig.tight_layout()

        # Mostrar la figura con ambos gráficos
        plt.show()
