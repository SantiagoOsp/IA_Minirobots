import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# 1. DEFINICIÓN DE VARIABLES Y UNIVERSOS
# ==============================================================================
temp = ctrl.Antecedent(np.arange(0, 101, 1), 'temp_actual')
error = ctrl.Antecedent(np.arange(-40, 41, 1), 'error_temp')
potencia = ctrl.Consequent(np.arange(0, 101, 1), 'potencia')

# ==============================================================================
# 2. FUNCIONES DE PERTENENCIA (5 NIVELES)
# ==============================================================================
# Temperatura Actual [0, 100] °C (Objetivo en 60 °C)
temp['muy_baja'] = fuzz.trapmf(temp.universe, [0, 0, 20, 35])
temp['baja']     = fuzz.trimf(temp.universe, [25, 42, 55])
temp['normal']   = fuzz.trimf(temp.universe, [50, 60, 70])
temp['alta']     = fuzz.trimf(temp.universe, [65, 78, 90])
temp['muy_alta'] = fuzz.trapmf(temp.universe, [82, 92, 100, 100])

# Error de Temperatura [-40, 40] °C (e = T_ref - T_actual)
error['muy_neg'] = fuzz.trapmf(error.universe, [-40, -40, -25, -12])
error['neg']     = fuzz.trimf(error.universe, [-20, -10, -2])
error['cero']    = fuzz.trimf(error.universe, [-5, 0, 5])
error['pos']     = fuzz.trimf(error.universe, [2, 10, 20])
error['muy_pos'] = fuzz.trapmf(error.universe, [12, 25, 40, 40])

# Potencia de Calefacción [0, 100] %
potencia['muy_baja'] = fuzz.trimf(potencia.universe, [0, 0, 20])
potencia['baja']     = fuzz.trimf(potencia.universe, [10, 25, 40])
potencia['normal']   = fuzz.trimf(potencia.universe, [30, 45, 60])
potencia['alta']     = fuzz.trimf(potencia.universe, [55, 75, 90])
potencia['muy_alta'] = fuzz.trimf(potencia.universe, [80, 100, 100])

# ==============================================================================
# 3. BASE DE REGLAS DE CONTROL
# ==============================================================================
reglas = [
    # Arranque en frío (Temperatura muy baja o baja con error positivo)
    ctrl.Rule(temp['muy_baja'] & error['muy_pos'], potencia['muy_alta']),
    ctrl.Rule(temp['muy_baja'] & error['pos'],     potencia['muy_alta']),
    ctrl.Rule(temp['baja']     & error['muy_pos'], potencia['muy_alta']),
    ctrl.Rule(temp['baja']     & error['pos'],     potencia['alta']),
    ctrl.Rule(temp['baja']     & error['cero'],    potencia['normal']),
    
    # Zona de operación normal alrededor de 60 °C
    ctrl.Rule(temp['normal']   & error['pos'],     potencia['alta']),
    ctrl.Rule(temp['normal']   & error['cero'],    potencia['normal']),
    ctrl.Rule(temp['normal']   & error['neg'],     potencia['baja']),
    
    # Sobrecalentamiento (Temperatura alta o muy alta)
    ctrl.Rule(temp['alta']     & error['cero'],    potencia['baja']),
    ctrl.Rule(temp['alta']     & error['neg'],     potencia['muy_baja']),
    ctrl.Rule(temp['alta']     & error['muy_neg'], potencia['muy_baja']),
    ctrl.Rule(temp['muy_alta'],                    potencia['muy_baja']),
    
    # Reglas de respaldo ante cambios de setpoint (ej. si T_ref cambia dinámicamente)
    ctrl.Rule(error['muy_pos'],                    potencia['muy_alta']),
    ctrl.Rule(error['muy_neg'],                    potencia['muy_baja'])
]

horno_ctrl = ctrl.ControlSystem(reglas)
horno_sim = ctrl.ControlSystemSimulation(horno_ctrl)

# ==============================================================================
# 4. EVALUACIÓN EN PUNTOS DE OPERACIÓN Y SIMULACIÓN DINÁMICA DE LA PLANTA
# ==============================================================================
casos_prueba = [
    (20.0, 40.0, "Arranque en frío (T=20°C, Ref=60°C)"),
    (52.0,  8.0, "Aproximación a consigna (T=52°C, Ref=60°C)"),
    (60.0,  0.0, "Estado estacionario (T=60°C, Ref=60°C)"),
    (68.0, -8.0, "Ligero sobreimpulso (T=68°C, Ref=60°C)"),
    (88.0,-28.0, "Sobrecalentamiento crítico (T=88°C, Ref=60°C)")
]

print("--- ANÁLISIS DE PUNTOS DE OPERACIÓN ---")
for t_val, e_val, desc in casos_prueba:
    horno_sim.input['temp_actual'] = t_val
    horno_sim.input['error_temp'] = e_val
    horno_sim.compute()
    print(f"{desc:45s} -> Potencia: {horno_sim.output['potencia']:6.2f}%")

# Simulación dinámica en el tiempo (Modelo térmico discreto de 1er orden)
# dT/dt = (Ganancia_calor * Potencia - Perdida_ambiente * (T - T_amb)) / Capacidad_termica
dt = 1.0          # Paso de tiempo (1 segundo)
pasos = 180       # 3 minutos de simulación
T_amb = 22.0      # Temperatura ambiente (°C)
T_ref = 60.0      # Consigna inicial (°C)

historial_T = [T_amb]
historial_P = []
historial_Ref = []

T_k = T_amb
for k in range(pasos):
    # En t = 100s cambiamos la consigna a 75°C para probar adaptabilidad
    if k == 100:
        T_ref = 75.0
        
    e_k = np.clip(T_ref - T_k, -40, 40)
    horno_sim.input['temp_actual'] = np.clip(T_k, 0, 100)
    horno_sim.input['error_temp'] = e_k
    horno_sim.compute()
    u_k = horno_sim.output['potencia']
    
    # Ecuación física de la planta térmica
    T_next = T_k + dt * (0.045 * u_k - 0.042 * (T_k - T_amb))
    
    historial_T.append(T_next)
    historial_P.append(u_k)
    historial_Ref.append(T_ref)
    T_k = T_next

# Gráfica de comportamiento dinámico
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax1.plot(historial_T[:-1], label='Temperatura Horno (°C)', color='crimson', linewidth=2)
ax1.plot(historial_Ref, '--', label='Consigna / Setpoint (°C)', color='black')
ax1.set_ylabel('Temperatura (°C)')
ax1.set_title('Respuesta Dinámica del Controlador Difuso de Temperatura')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(historial_P, label='Potencia Calefactora (%)', color='royalblue', linewidth=2)
ax2.set_ylabel('Potencia (%)')
ax2.set_xlabel('Tiempo (segundos)')
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()