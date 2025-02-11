# Agente-Inteligente-Resolvedor-Laberinto
Agente inteligente entrenado mediante aprendizaje por refuerzo para resolver un laberinto dado.

# Funcionamiento
Se creó un agente inteligente que utiliza aprendizaje por refuerzo para la resolución de cualquier laberinto sobre el que esté entrenado.

Para el entrenamiento se utilizó el algoritmo Q-Learning, el cual halla la política óptima que maximiza la recompensa acumulada final. Para ello hace uso de una Q-Table, la cual es una tabla que almacena los valores de la recompensa acumulada esperada para cada par (estado, acción), donde el estado corresponde a una ubicación en el laberinto y acción al movimiento posible en el estado actual.

Para la creación de los laberintos se utilizó el algoritmo Deep First Search (Búsqueda en profundida), el cual genera laberintos mediante una exploración profunda desde un punto inicial. Comienza en una celda y explora una dirección hasta que no puede avanzar más, luego retrocede (backtracking) y prueba nuevas direcciones. Este proceso continúa hasta que se exploran todas las celdas posibles. Durante la creación del laberinto, el algoritmo marca las celdas visitadas y genera pasajes entre ellas, dejando algunas celdas aisladas como paredes, lo que asegura que el laberinto sea resoluble.
