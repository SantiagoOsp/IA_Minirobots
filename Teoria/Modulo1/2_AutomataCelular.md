# 🤖 Automatas Celulares

Surgen en la decada de 1940 con John Von Neumann, que buscaba crear una maquina capaz de autoreplicarse (Creo un modelo matematico de esta)

*Tenian reglas complejas sobre una red rectangular* -> Conjunto de celulas que crecian, se reproducian y morian

Por definicion un **automata celular** -> *es un modelo matematico para un sistema dinamico compuesto por un conjunto de celdas o celulas que adquieren distintos estados o valores.* Los estados cambian en tiempos discretos y se puede modelar el comportamiento con una expresion que es sensible a los estados de las celular vecinas (***Regla de transicion local***)

## Elementos

- **Un espacio regular:** Puede ser una linea, espacio 2D o n-dimensional. Cada division homogenea es llamada celula
- **Conjunto de estados:** Es finito y cada celula toma un valor del conjunto de estados.
- **Configuracion inicial:** Valores iniciales de un estado a cada una de las celulas
- **Vecindades:** Define el conjunto de celulas que se consideran adyacentes, asi como posiciones relativas. Cuando el espacio es uniforme, la vecindad de cada celula es isomorfa (tiene el mismo aspecto)

![](./Images/Vecindades.jpg)

- **Funcion de transicion local:** Regla de evolucion del automata. Se calcula a partir del estado de la celula y su vecindad. Define su nuevo estado a partir de su estado anterior. (*Expresion algebraica o grupo de ecuaciones*)

![](./Images/FT_local.png)

Los automatas llamaron la atencion en los 70s cuando John Conway desarrollo el juego de la vida. Este juego demuestra que reglas simples desencadenan cosas caoticas y complejas.

Estos sistemas complejos son dinamicos, por lo cual su estado se puede determinar a partir del estado anterior y de sus interacciones con el ambiente. Por lo general son continuos y se pueden manipular de forma discreta (tanto temporal como espacialmente)

### Complejidad

Esta emerge a partir de la interaccion de las celulas que siguen reglas simples. En ingles, un automata es *automaton* y un grupo de automatas es *automata*. Por lo tanto, decimos que el termino ***Cellular Automata*** surge de un grupo de automatas elementales.

### Vecindad

*"Dime con quien andas y te dire quien eres"* -Refran popular

Este concepto es fundamental en los automatas y nos dice que el comportamiento de una celula en el tiempo viene dado por el comportamiento de esta y el de sus vecinas. Es el conjunto de vecinos de una celula que influye en su comportamiento. Tanto asi que pasa en nuestras casas, trabajos, clases, desplazamientos o reuniones. Hay reglas implicitas de las cuales no somos conscientes, que si bien no estan formalmente establecidas, definen nuestro comportamiento.

## Definicion FORMAL

Un automata celular D-dimensional (AC-D) es una secuencia $C_t$, definida por una 5-tupla, $(L,w,U,f,C_o)$ donde:

- $L$: es un reticulo
- $w$: es un alfabeto, que representa los estados de la celda
- $U=(u_1, u_2, ..., u_n)$ es una secuencia finita de elementos del reticulo
- $f:w^u \rightarrow w$ es la funcion de transicion o regla local
- $C_o : L \rightarrow w$ es alguna configuracion inicial

### Propiedades esenciales de un automata celular

1. Universo: Un reticulo o arreglo regular, tambien se le conoce como teselacion, donde cada *celula* tiene un estado discreto
2. Dinamico: Un comportamiento dinamico que describe la regla local
3. Homogeneidad: Todas las celulas se actualizan con la misma regla local
4. Paralelismo: El estado de todas las celulas se actualiza simultaneamente. La regla define el estado de cada celula central en el siguiente paso de tiempo, dependiendo de los estados de las celulas vecinas y de su propio estado
5. Localidad: Las reglas son locales por naturaleza

Para poder construir un automata se debe definir: la celula, el reticulo, la regla y la vecindad

#### 1. *La Celula*

Elemento basico, y se comporta como un automata de estado finito. Sus entradas son el estado de las celulas vecinas y el suyo propio; su salida, su nuevo estado.

> Clase de elemento que almacena estados. El numero de estados o conjunto de estados se representa por $\omega$. El caso mas simple $\omega={0,1}$

#### 2. *El reticulo*

Espacio donde se conforma el AC. El mas simple es el de una dimension ocn una configuracion cuadrada, *1D*. Los mas comunes son de 1D o 2D aunque ciertas aplicaciones trabajan 3D conocidos como teselación.

#### 3. *Las reglas*

Se usan para introducir la dinamica del sistema, en algunas aplicaciones son ecuaciones diferenciales

#### 4. *La vecindad*

Se establece dentro del reticulo (casi siempre son regulares). Se conforma en base al radio **r** (horizonte del automata)

---

En general el comportamiento del AC depende de sus condiciones iniciales y de su regla de comportamiento local. Cada regla se identifica con base en un numero entre 0 y 255

![](./Images/EjemAC.png)

---

## Vecindad de MOORE

Conjunto de las ocho celdas que rodean una celda central en un enrejado cuadrado bidimensional. 

![](./Images/Moore_neighborhood_with_cardinal_directions.svg.webp)

---

## Automatas celulares *PROBABILISTICOS*

Son aquellos que las reglas permiten un cambio de estado con base a una probabilidad, permitiendo movimientos aleatorios. Se usa en la difusion de un virus en un ambiente.

Suponga que tiene un AC 2D en un reticulo cuadrado de 10.000 celdas; y que $\omega = {Np, Ps, Cs, Cns, Ct, Pac}$ donde:

- Np = no hay nada en la celda
- Ps = personas sanas
- Cs = persona con Covid-19 sintomatica
- Cns = persona con Covid-19 asintomatica
- Ct = Persona con Covid-19 en cuarentena o cuidados medicos
- Pac = Persona curaca con anticuerpos
- M = Persona muerta, no aparece en el reticulo

Inicialmente el retículo se carga con 5000 Ps distribuidos uniformemente, con 5 Cs y 5 Cns también distribuidos aleatoriamente. Se usa la **vecindad de Moore**.

Reglas:

- Si Ps tiene n vecinos pasa con probabilidad 0.n a ser Cns con probabilidad 0.4; o Cs con probabilidad 0.7
- Cs después de 7 ciclos pasa a  Ct
- Cns después de 30 ciclos pasa a Pac
- Ct después de 20 ciclos con probabilidad 0.8 pasa a Pac o con probabilidad 0.2 pasa a M, que no se representa en el retículo

Una vez se han ejecutado estas reglas en paralelo, se desplaza cada celda a una celda Norte, Sur, Este u oeste con probabilidad 0.25, si la celda está vacía. En caso contrario, se debe llevar el número de ciclos para las celdas Cs, Cns y Ct, lo mismo que el conteo de M. En cada ciclo se debe llevar el conteo de cada tipo de celda. Con la simulación se busca responder las preguntas siguientes: ¿Después de cuantos ciclos se  estabiliza la población? ¿Cuantas celdas de cada estado quedan? ¿Cuántos muertos hubo?

---

### Aplicaciones de los automatas celulares

- Epidemiologia
- Antropologia
- Sociologia
- Criptografia
- Biologia
- Flujo vehicular
- Simulacion de fenomenos naturales
- En robotica: Aunque no se ha usado mucho, se puede ver potencial si se tiene un robot movil simple equipado con sensores de proximidad y dos motores pueden girar en ambos sentidos. En este caso el AC puede hacer que se eviten obstaculos que se le puedan ir presentando en el camino, eliminando colisiones

![](./Images/RoboticaAC.png)

- Estudios teoricos
- Otras aplicaciones: Entre otras aplicaciones trabajadas tenemos la simulacion del crecimiento del cancer, los modelos de uso de la tierra, los modelos de incendios forestales, modelos de reacciones quimicas, los patrones de pigmentacion de piel, crecimiento de conchas marinas y corales, comportamiento de colonias de microorganismos, modelo de simulacion de evacuaciones, entre otros.


### El problema inverso

Se conoce el comportamiento a nivel macro, a nivel del SCA y se desea encontrar las reglas que generan ese comportamiento.

#### Diagramas de Voronoi

Que pasa con la vecindad si la teselacion no es regular? Viendo los planos de una region y no encontramos una forma regular de universo como las definidas, para poder utilizar su potencialidad en este tipo de escenarios reales. Se usan diagramas de Voronoi

Tienen variedad de aplicaciones como:

- En graficas para generar texturas naturales, en simulacion de fracturas; en busqueda y optimizacion como planear rutas en zonas de influencia, en agricultura de precision en procesamiento de imagenes, en diseño de redes inalambricas

![](./Images/DiagramasVoronoi.png)