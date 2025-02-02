import os

def reemplazar_texto_en_archivo(ruta_archivo, expresiones_val, reemplazos_val):
    # Reemplaza las expresiones exactas y sus versiones en mayúsculas en un archivo de texto.
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo_val:
            contenido_val = archivo_val.read()

        contenido_modificado = contenido_val
        modificado_flag = False  # Bandera para verificar si se realizó alguna modificación

        # Reemplazar cada expresión y su versión en mayúsculas
        for expr_val, repl_val in zip(expresiones_val, reemplazos_val):
            if expr_val in contenido_val or expr_val.upper() in contenido_val:
                contenido_modificado = contenido_modificado.replace(expr_val, repl_val)
                contenido_modificado = contenido_modificado.replace(expr_val.upper(), repl_val.upper())
                modificado_flag = True  # Se realizó al menos una modificación

        return contenido_modificado if modificado_flag else None  # Devolver el contenido modificado solo si hubo cambios

    except (UnicodeDecodeError, PermissionError, IOError):
        # Si ocurre un error al abrir o leer el archivo, simplemente lo ignoramos
        return None

def buscar_y_reemplazar_en_directorio(directorio_base, expresiones_val, reemplazos_val, directorio_salida):
    # Recorre recursivamente un directorio y reemplaza las expresiones en archivos de texto.
    contador_archivos = 0  # Contador de archivos modificados
    for directorio_actual, _, archivos_val in os.walk(directorio_base):
        for archivo_val in archivos_val:
            ruta_completa = os.path.join(directorio_actual, archivo_val)
            # Intentar procesar el archivo como texto
            contenido_modificado = reemplazar_texto_en_archivo(ruta_completa, expresiones_val, reemplazos_val)
            if contenido_modificado is not None:
                # Crear la ruta de salida manteniendo la estructura de directorios
                ruta_relativa = os.path.relpath(directorio_actual, directorio_base)
                subdirectorio_salida = os.path.join(directorio_salida, ruta_relativa)
                os.makedirs(subdirectorio_salida, exist_ok=True)  # Crear subdirectorios si no existen
                ruta_archivo_salida = os.path.join(subdirectorio_salida, archivo_val)
                # Guardar el archivo modificado en la carpeta de salida
                with open(ruta_archivo_salida, 'w', encoding='utf-8') as archivo_salida:
                    archivo_salida.write(contenido_modificado)
                # Incrementar el contador de archivos modificados
                contador_archivos += 1

    return contador_archivos  # Devolver el número de archivos modificados

def obtener_directorio_salida_unico(base_dir):
    # Generar un nombre de directorio único para evitar sobreescribir
    contador_val = 1
    directorio_salida = base_dir
    while os.path.exists(directorio_salida):
        directorio_salida = f"{base_dir} ({contador_val})"
        contador_val += 1
    return directorio_salida

def main():
    # Bucle infinito
    while True:
        # Solicitar el directorio de entrada
        while True:
            directorio_base = input("Enter directory: ")
            if os.path.exists(directorio_base):
                break
            print("Wrong directory")

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
        directorio_salida = obtener_directorio_salida_unico("Output files")
        os.makedirs(directorio_salida, exist_ok=True)

        # Buscar y reemplazar en el directorio
        contador_archivos = buscar_y_reemplazar_en_directorio(directorio_base, expresiones_val, reemplazos_val, directorio_salida)

        # Mostrar el número de archivos modificados
        print("------------------------------------")
        if contador_archivos == 0:
            print("No modified files")
        else:
            print(f"{contador_archivos} Files modified")
        print("------------------------------------\n")

if __name__ == "__main__":
    main()