import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# 1. DEFINICIÓN DE UNIVERSOS DE DISCURSO Y VARIABLES LINGÜÍSTICAS
# ==============================================================================
# Entradas: Temperatura [0, 50] °C y Humedad [0, 100] %
# Salida: Velocidad del ventilador [0, 100] %
temperatura = ctrl.Antecedent(np.arange(0, 51, 1), 'temperatura')
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
ventilador = ctrl.Consequent(np.arange(0, 101, 1), 'ventilador', defuzzify_method='centroid')

# ==============================================================================
# 2. CONSTRUCCIÓN DE FUNCIONES DE PERTENENCIA
# ==============================================================================
# Temperatura (Trapezoidales en extremos, Triangular en el centro)
temperatura['fria'] = fuzz.trapmf(temperatura.universe, [0, 0, 15, 22])
temperatura['templada'] = fuzz.trimf(temperatura.universe, [18, 25, 32])
temperatura['caliente'] = fuzz.trapmf(temperatura.universe, [28, 35, 50, 50])

# Humedad (Triangulares)
humedad['baja'] = fuzz.trimf(humedad.universe, [0, 0, 50])
humedad['media'] = fuzz.trimf(humedad.universe, [25, 50, 75])
humedad['alta'] = fuzz.trimf(humedad.universe, [50, 100, 100])

# Velocidad del Ventilador (Salida)
ventilador['lenta'] = fuzz.trimf(ventilador.universe, [0, 0, 50])
ventilador['moderada'] = fuzz.trimf(ventilador.universe, [20, 50, 80])
ventilador['rapida'] = fuzz.trimf(ventilador.universe, [50, 100, 100])

# ==============================================================================
# 3. BASE DE REGLAS DIFUSAS (IF - THEN)
# ==============================================================================
regla1 = ctrl.Rule(temperatura['fria'] & humedad['baja'], ventilador['lenta'])
regla2 = ctrl.Rule(temperatura['fria'] & humedad['alta'], ventilador['moderada'])
regla3 = ctrl.Rule(temperatura['templada'] & humedad['media'], ventilador['moderada'])
regla4 = ctrl.Rule(temperatura['templada'] & humedad['alta'], ventilador['rapida'])
regla5 = ctrl.Rule(temperatura['caliente'] | humedad['alta'], ventilador['rapida'])
regla6 = ctrl.Rule(temperatura['caliente'] & humedad['baja'], ventilador['moderada'])

# ==============================================================================
# 4. CREACIÓN DEL SISTEMA DE CONTROL Y SIMULACIÓN MAMDANI
# ==============================================================================
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6])
simulacion = ctrl.ControlSystemSimulation(sistema_ctrl)

# Introducir valores medidos por sensores (Entradas Crisp)
temp_actual = 31.0  # °C (Parcialmente templada y caliente)
hum_actual = 65.0   # %  (Parcialmente media y alta)

simulacion.input['temperatura'] = temp_actual
simulacion.input['humedad'] = hum_actual

# Ejecutar inferencia y defuzzificación
simulacion.compute()
salida_ventilador = simulacion.output['ventilador']

print(f"Entradas -> Temperatura: {temp_actual}°C, Humedad: {hum_actual}%")
print(f"Salida Mamdani (Centroide) -> Velocidad Ventilador: {salida_ventilador:.2f}%")

# ==============================================================================
# 5. VISUALIZACIÓN DE RESULTADOS
# ==============================================================================
# Muestra el conjunto difuso agregado resultante y la línea vertical del centroide
ventilador.view(sim=simulacion)
plt.title(f"Inferencia Mamdani: Salida = {salida_ventilador:.2f}%")
plt.show()