import pandas as pd
import random

# Definición de las columnas requeridas
columnas = [
    'fecha carga', 'Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico',
    'apellido', 'nombres', 'Tipo de documento', 'Número de documento',
    'Confirmar el número de documento', 'CUIL', 'Fecha de nacimiento', 'Edad',
    'Último estudio finalizado', 'Teléfono celular de referencia', 'Organismo',
    'Repartición / oficina', 'Partido de residencia', 'Curso en el que desea inscribirse', 'Cargo'
]

data = []

for i in range(100):
    nro_resp = 100000 + i
    dni = random.randint(20000000, 45000000)
    email = f"usuario_{i}@ejemplo.com"
    
    # Valores por defecto (Correctos)
    conf_email = email
    conf_dni = dni
    
    # Inyectar errores aleatorios
    error_type = random.choice(['ninguno', 'ninguno', 'ninguno', 'email_mismatch', 'dni_mismatch', 'duplicado'])
    
    if error_type == 'email_mismatch':
        conf_email = f"otro_email_{i}@test.com"
    elif error_type == 'dni_mismatch':
        conf_dni = dni + 1
        
    fila = [
        "2026-02-02T14:00:00", nro_resp, email, conf_email,
        f"Apellido_{i}", f"Nombre_{i}", "DNI", dni, conf_dni,
        f"20{dni}0", "1990-01-01", 36, "Universitario", "0221 123456",
        "Organismo Test", "Oficina Test", "La Plata", "Curso de IA", "Analista"
    ]
    
    data.append(fila)
    
    # Si es un duplicado, agregamos la misma fila otra vez
    if error_type == 'duplicado':
        data.append(fila)

# Crear DataFrame y guardar
df_test = pd.DataFrame(data, columns=columnas)
df_test.to_csv('data/datos_prueba_masivos.csv', sep=';', index=False, encoding='utf-8')

print(f"✅ Archivo generado con {len(df_test)} filas en 'data/datos_prueba_masivos.csv'")