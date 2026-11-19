# Algoritmos Geneticos

Entre los diferentes enfoques para atacar el problema de la IA, se presenta el enfoque de vida (sistemas bioinspirados) como el proceso evolutivo. El algoritmo genetico es una serie de herramientas bioinspiradas entre las que se encuentran:

- Optimizacion por Colonia de Hormigas
- Recocido Simulado
- Inteligencia de Enjambre
- Busqueda Tabu
- Lobo gris (GWolf) y otras

Resolucion de problemas de optimizacion y de *alta complejidad computacional*.

## Introduccion a los algoritmos geneticos

Surgio apartir de la idea de querer mejorar algoritmos para la resolucion de problemas de ingenieria. La idea principal era evolucionar una poblacion de soluciones candidatas usando operadores inspirados en la variacion genetica y la seleccion natural. De aqui sale el Algoritmo Genetico **AG**

Es un algoritmo de optimizacion por busqueda estocastica (que no es predecible), basado en la seleccion natural. Trabaja muchas soluciones en forma paralela, que se conocen como cromosomas. Siempre se va a encontrar que un cromosoma es mejor para la resolucion de un problema que otros. Estos cromosomas (los mas aptos) se seleccionan como padres para la siguiente generacion.

El sistema se presenta como una funcion de aptitud que debe satisfacer una o varias condiciones.

## Algoritmo Genetico Simple **AGS**

Los algoritmos son bastante sencillos lo cual es lo mas atractivo de estos. Para tener mayor claridad de los conceptos tenemos:

| Conceptos de Biología | Conceptos en Algoritmos Genéticos        |
|------------------------|------------------------------------------|
| Biología              | Algoritmos Genéticos                     |
| Cromosoma             | Lista                                    |
| Gen                   | Elemento de la lista                     |
| Genotipo              | Solución codificada, cromosoma           |
| Fenotipo              | Solución decodificada                    |

Definiendo algunos parametros de los AGs

- **l:** Numero de genes del cromosoma (numero de bits o longitud del cromosoma)
- **k:** un gen cualquiera del cromosoma
- **K:** numero de cromosomas en la poblacion
- **M:** numero de generaciones del algoritmo
- **x:** valor que representa un cromosoma
- **f(x):** funcion de aptitud aplicada en el punto **x**

Para poder trabajar con el algoritmo se desarrollaron varios operadores, sin embargo los mas importantes y comunes son:

1. **Seleccion** Proceso en que ciertos cromosomas se llevan a la siguiente gen considerando su comportamiento con respecto a la funcion de aptitud *f*. Esta seleccion se hace con base en el valor *promedio de aptitud*. 
2. **Cruce** (simple) procede en dos pasos. Primero los cromosomas seleccionados como padres entran en el juego de apareamiento, mezclandose al azar. Segundo se efectua el cruce al azar de cada par de listas como sigue: seleccion con probabilidad uniforme, una posicion ***k***, entre 1 y la longitud **l** de la lista menos 1 -> [1, l-1].se crearon dos nuevas lista entre las posiciones ***k+1*** y *l* incluidas. Por ejemplo, considere las listas con *l=5* y los cromosomas A1 y A2 que se seleccionaron:

$$
A1 = 010111010 \\
A2 = 011110010
$$

suponiendo que *k=5* el cruce da dos nuevas cadenas A1' y A2' que son parte de la new gen:

$$
A1 = 010110010 \\
A2 = 011111010
$$

Se combinan informacion de cromosomas exitosos, para produccion de descendencia.

3. **Mutacion** operador genetico de segundo orden pues se aprovecha mas el intercambio de informacion. Este operador se aplica a los individuos con una probabilidad ***p_m*** generalmente baja. Aumenta la diversidad genetica de la población, posibilitando mejores soluciones.

## Flujo de un Algoritmo Genético

1. **Inicialización**
   - Se genera aleatoriamente la primera población.
   - Se crean **K cromosomas**, cada uno con **l bits** de longitud.

2. **Iteración (M generaciones o hasta condición de terminación)**
   i. **Decodificación**
      - Se obtiene el valor **x** a partir del cromosoma.
   
   ii. **Evaluación de aptitud**
      - Se calcula la aptitud **f(x)** de cada cromosoma.
      - Se obtiene la aptitud global de la población:  

\[
        F = \sum f(x)
        \]

      - Se calcula la probabilidad de selección de cada cromosoma:          

\[
        p(x) = \frac{f(x)}{F}
        \]

   iii. **Selección**
      - Se seleccionan cromosomas como padres según su probabilidad **p(x)**.
      - La selección se hace **sin reemplazo** (un cromosoma puede ser elegido varias veces).
      - Se mantiene el mismo tamaño de población.

   iv. **Cruzamiento**
      - Se escoge un par de cromosomas padres.
      - Se cruzan en un punto aleatorio (probabilidad uniforme).
      - Se generan dos hijos.

   v. **Mutación**
      - Con probabilidad **pm**, se sustituye un gen:
        - 1 → 0  
        - 0 → 1
      - Se obtiene la nueva población.

   vi. **Reemplazo**
      - La población actual se sustituye por la nueva.
      - Se disminuye en 1 el conteo de generaciones.

   vii. **Repetición**
      - Regresa al paso 2.

El ejemplo que tenemos en este caso para un algoritmo genetico se ve reflejado en el archivo de excel [EjercicioAlgGeneticos](../Practica/EjercicioAlgGeneticos.xlsm)

## 🧬 Codificacion de las rutinas basicas de un Algoritmo Genetico

El código implementa un **Algoritmo Genético clásico**, que es una técnica inspirada en la evolución biológica para resolver problemas de optimización. La idea es simular cómo una población de soluciones evoluciona generación tras generación hasta encontrar la mejor respuesta posible.

### 🔹 Flujo general
1. **Inicialización:** Se crea una población inicial de cromosomas (cadenas de bits) de manera aleatoria.
2. **Evaluación:** Cada cromosoma se decodifica y se evalúa con una función de aptitud, que mide qué tan buena es la solución.
3. **Selección:** Se eligen los cromosomas más aptos como padres, con mayor probabilidad de ser seleccionados si su aptitud es alta.
4. **Cruce:** Los padres se combinan en un punto aleatorio para generar hijos, mezclando información genética.
5. **Mutación:** Algunos bits cambian aleatoriamente (0 ↔ 1) para introducir variabilidad y evitar estancamiento.
6. **Reemplazo:** La nueva población sustituye a la anterior y el proceso se repite hasta completar el número de generaciones.

### 🔹 Funciones principales
- **`genera(l, K)`**: crea la población inicial con \(K\) cromosomas de longitud \(l\).
- **`eval_apt(pob, l, ecuacion)`**: evalúa la aptitud de cada cromosoma y calcula su probabilidad de selección.
- **`evalua(crom, l, ecuacion)`**: decodifica un cromosoma y lo evalúa con la función objetivo.
- **`ecuacion(x)`**: define la función matemática que se quiere optimizar.
- **`decodifica(crom, l)`**: convierte el cromosoma binario en un valor real dentro de un rango definido.
- **`seleccion(pob, probab)`**: elige los cromosomas más aptos como padres.
- **`cruce(pob_nueva)`**: combina pares de cromosomas en un punto aleatorio para generar hijos.
- **`mutacion(hijos, p_mut, l)`**: altera bits de los cromosomas con baja probabilidad para mantener diversidad genética.
- **`Alg_Genetico(...)`**: función principal que coordina todo el proceso evolutivo durante \(M\) generaciones.

El desarrollo de este se ve en el archivo [ejemAG](../Practica/ejemAG.py) hecho en python.

---

## Problemas tipo NP y NP-Completos

### Tipo P

Es un algoritmo cuyo tiempo de ejecucion esta dado por un polinomio que es funcion del tamaño de los datos de entrada. Un problema pertenece a la clase **P** si el numero de pasos requeridos para hallar su solucion, es decir, su tiempo de ejecucion, esta limitado o puede definirse por un polinomio.

> Este tipo de problemas evita preocupaciones en cuanto al modelo de la maquina

### Tipo NP

Son intratables en el sentido de que no se ha encontrado una solucion real y eficiente para el problema -> datos de entrada **n** grande.

En este caso el tiempo para hallar una solucion puede tener crecimiento exponencial o mayor con **n**. Estos problemas son no deterministicos, **NP**, si se puede resolver en tiempo polinomial en una maquina de Turing no deterministica **MTN** (Esta es una maquina que puede tomar muchos caminos computacionales simultaneos)

### Tipo NP Completos

Los problemas conocidos se caracterizan porque se pueden reducir a uno. Es decir, dados dos problemas NP, X y Y existe un algoritmo de tiempo polinomial que redefine un problema de tipo X como un problema de tipo Y y visceversa.
