import numpy as np
import skfuzzy as fuzz

def sistema_sugeno_orden1(temp, hum):
    """
    Implementación de un FIS Takagi-Sugeno-Kang (TSK) de Primer Orden.
    Consecuentes lineales: z_i = p_i * temp + q_i * hum + r_i
    """
    # 1. Fuzzificación de las entradas escalares
    u_temp = np.array([temp])
    u_hum = np.array([hum])
    
    mu_t_fria = fuzz.trapmf(u_temp, [0, 0, 15, 22])[0]
    mu_t_caliente = fuzz.trapmf(u_temp, [28, 35, 50, 50])[0]
    
    mu_h_baja = fuzz.trimf(u_hum, [0, 0, 50])[0]
    mu_h_alta = fuzz.trimf(u_hum, [50, 100, 100])[0]
    
    # 2. Evaluación de antecedentes (Fuerza de disparo w_i usando producto algebraico)
    w1 = mu_t_fria * mu_h_baja       # Regla 1: Fría AND Baja
    w2 = mu_t_fria * mu_h_alta       # Regla 2: Fría AND Alta
    w3 = mu_t_caliente * mu_h_baja   # Regla 3: Caliente AND Baja
    w4 = mu_t_caliente * mu_h_alta   # Regla 4: Caliente AND Alta
    
    # 3. Evaluación de consecuentes funcionales lineales (z_i = p*T + q*H + r)
    z1 = 0.5 * temp + 0.1 * hum + 5.0    # Baja potencia base
    z2 = 0.8 * temp + 0.3 * hum + 15.0   # Compensación por humedad
    z3 = 1.5 * temp + 0.2 * hum + 10.0   # Compensación por calor seco
    z4 = 2.0 * temp + 0.4 * hum + 20.0   # Máxima respuesta térmica
    
    # 4. Agregación por Promedio Ponderado (Sin integración de área)
    pesos = np.array([w1, w2, w3, w4])
    salidas = np.array([z1, z2, z3, z4])
    
    if np.sum(pesos) == 0:
        return 0.0  # Protección ante división por cero si no hay reglas activas
        
    salida_final = np.sum(pesos * salidas) / np.sum(pesos)
    return np.clip(salida_final, 0, 100)  # Saturación física al rango [0, 100]%

# Prueba con las mismas entradas del caso Mamdani
res_sugeno = sistema_sugeno_orden1(temp=31.0, hum=65.0)
print(f"Salida Sugeno Orden 1 -> Velocidad Ventilador: {res_sugeno:.2f}%")