# README
## Integrantes
- Sebastián Alejandro Gutiérrez Medina
- Juan Aurelio Juarez Ubaldo
- Luis Antonio Sánchez Montalvo
## Instrucciones
Para modificar el archivo, en el script Cuarto.py, podemos especificar el tamaño de la cuadricula
y la posicion de obstaculos, suciedad y la aspiradora. 
Es importante notar que aumentar la vision del robot, hara que sea mas ineficiente, ya que hay
mas configuraciones posibles con visiones mas amplias.
La simulacion pregunta en cada paso si deseas continuar, en caso de querer detenerse, ingresar "n"
para seguir, cualquier otra tecla
## Consideraciones
- El numero de largo y ancho es el número de losetas, en vez de los metros del cuarto:(
- La idea de que el depth en minmax fuera dinamico al principio, es que para generar la ruta mas corta
 usamos un bfs que nos dice la ruta mas corta para limpiar toda la suciedad visible y ese sera el numero de
 pasos que "veremos en el futuro" con minmax
- Ya que puede haber obstaculos moviles que no hagan posible realizar la ruta mas corta, en la funcion evaluar, tomamos en cuenta tambien la distancia mas corta, esto para que las configuraciones en las que la 
aspiradora se encuenta mas cerca de la suciedad sean las que tengan evaluacion mas alta
- Agregamos una funcion de agregar suciedad aleatoriamente
- Suponemos que tanto la aspiradora como el agente solo se mueven en 4 direcciones
- Una desventeja de no poder ver todo el cuarto, es que cuando no hay suciedad visible, solo
 nos movemos de manera aleatoria hasta encontrar suciedad
- Entre mas agentes haya en la vision de la aspiradora, sera mas ineficiente, ya que generamos todas las
 posibles combinaciones de movimientos de los agentes en conjunto
- Para expandir los arboles, tenemos 2 funciones de expandir, esto porque sabemos que solo tenemos 1 aspiradora, pero para cuando sea el turno de mover de los agentes, puede haber mas de uno y hay que calcular todos los movimientos posibles de cada uno
- Para la funcion de evaluar, los valores que sumamos y restamos fueron obtenidos a prueba y error,
 comparando ejecuciones con distintos valores
- En algunas ejecuciones notamos que aunque haya suciedad cerca la ignora:(