import os

# Lista de codificaciones a probar (en orden de prioridad)
codificaciones_txt = ['utf-8', 'latin-1', 'utf-16', 'cp1252']

# Reemplaza las expresiones exactas y sus versiones en mayúsculas en un archivo de texto
def f_reemplazar_texto(ruta_archivo, expresiones_val, reemplazos_val):
    # Intenta decodificar en cada formato
    for codificacion_iter in codificaciones_txt:
        try:
            with open(ruta_archivo, 'r', encoding = codificacion_iter) as archivo_val:
                contenido_val = archivo_val.read()
    
            contenido_modificado = contenido_val
            
            # Bool para verificar si se realizó alguna modificación
            modificado_bool = False
    
            # Reemplazar cada expresión y su versión en mayúsculas
            for expr_val, repl_val in zip(expresiones_val, reemplazos_val):
                if expr_val in contenido_val or expr_val.upper() in contenido_val:
                    contenido_modificado = contenido_modificado.replace(expr_val, repl_val)
                    contenido_modificado = contenido_modificado.replace(expr_val.upper(), repl_val.upper())
                    
                    # Se realizó al menos una modificación
                    modificado_bool = True
    
            # Devolver el contenido modificado solo si hubo cambios
            return contenido_modificado if modificado_bool else None
        except (UnicodeDecodeError, PermissionError, IOError):
            # Si ocurre un error al abrir o leer el archivo, simplemente lo ignoramos
            return None

# Recorre recursivamente un directorio y reemplaza las expresiones en archivos de texto
def f_buscar_reemplazar(directorio_base, expresiones_val, reemplazos_val, directorio_salida):
    # Contador de archivos modificados
    contador_archivos = 0
    
    # Recorre recursivamente todos los subdirectorios del directorio base
    for directorio_actual, _, archivos_val in os.walk(directorio_base):
        # Itera sobre cada archivo encontrado en el directorio actual
        for archivo_val in archivos_val:
            ruta_completa = os.path.join(directorio_actual, archivo_val)
            
            # Intentar procesar el archivo como texto
            contenido_modificado = f_reemplazar_texto(ruta_completa, expresiones_val, reemplazos_val)
            
            if contenido_modificado is not None:
                # Crear la ruta de salida manteniendo la estructura de directorios
                subdirectorio_salida = os.path.join(directorio_salida, os.path.relpath(directorio_actual, directorio_base))
                
                # Crear subdirectorios si no existen
                os.makedirs(subdirectorio_salida, exist_ok = True)
                ruta_archivo_salida = os.path.join(subdirectorio_salida, archivo_val)

                # Intenta decodificar en cada formato
                for codificacion_iter in codificaciones_txt:
                    # Guardar el archivo modificado en la carpeta de salida
                    with open(ruta_archivo_salida, 'w', encoding = codificacion_iter) as archivo_salida:
                        archivo_salida.write(contenido_modificado)
                
                    # Incrementar el contador de archivos modificados
                    contador_archivos += 1
                    
                    break

    # Devolver el número de archivos modificados
    return contador_archivos

# Generar un nombre de directorio único para evitar sobreescribir
def f_directorio_salida(base_dir):
    contador_val = 1
    directorio_salida = base_dir
    
    # Actualizar el nombre de la carpeta de salida hasta alcanzar el nombre único
    while os.path.exists(directorio_salida):
        directorio_salida = f"{base_dir} ({contador_val})"
        
        contador_val += 1
    
    return directorio_salida

# Bucle principal del programa
while True:
    # Solicitar el directorio de entrada
    while True:
        directorio_base = input("Enter directory: ").strip('"\'')

        # Verificar si el directorio existe
        if os.path.exists(directorio_base):
            break
        
        print("Wrong directory\n")

    # Solicitar el número de expresiones a modificar
    while True:
        try:
            num_expresiones_val = int(input("Enter number of expressions to replace: "))
            
            break
        except ValueError:
            print("Wrong format")

    expresiones_val = []
    reemplazos_val = []

    # Solicitar cada expresión y su reemplazo
    for iter in range(num_expresiones_val):
        expr_val = input(f"Enter expression {iter + 1}: ")
        repl_val = input(f"Replace '{expr_val}' with: ")
        
        expresiones_val.append(expr_val)
        reemplazos_val.append(repl_val)

    # Crear un directorio de salida único
    directorio_salida = f_directorio_salida("Output files")
    os.makedirs(directorio_salida, exist_ok = True)

    # Buscar y reemplazar en el directorio
    contador_archivos = f_buscar_reemplazar(directorio_base, expresiones_val, reemplazos_val, directorio_salida)

    # Mostrar el número de archivos modificados
    print("------------------------------------")
    
    if contador_archivos == 0:
        print("No modified files")
    elif contador_archivos == 1:
        print("1 modified file")
    else:
        print(f"{contador_archivos} modified files")
    
    print("------------------------------------\n")
