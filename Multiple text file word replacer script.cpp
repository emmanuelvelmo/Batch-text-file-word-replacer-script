#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<filesystem>
#include<algorithm>

// Reemplaza las expresiones exactas y sus versiones en mayúsculas en un archivo de texto
std::string f_reemplazar_texto(const std::string& ruta_archivo, const std::vector<std::string>& expresiones_val, const std::vector<std::string>& reemplazos_val)
{
    try {
        std::ifstream archivo_val(ruta_archivo);

        if (!archivo_val.is_open())
        {
            return "";
        }

        std::string contenido_val((std::istreambuf_iterator<char>(archivo_val)), std::istreambuf_iterator<char>());
        std::string contenido_modificado = contenido_val;

        // Bool para verificar si se realizó alguna modificación
        bool modificado_bool = false;

        // Reemplazar cada expresión y su versión en mayúsculas
        for (size_t i = 0; i < expresiones_val.size(); ++i)
        {
            const std::string& expr_val = expresiones_val[i];
            const std::string& repl_val = reemplazos_val[i];

            std::string expr_val_upper = expr_val;
            std::transform(expr_val_upper.begin(), expr_val_upper.end(), expr_val_upper.begin(), ::toupper);

            if (contenido_val.find(expr_val) != std::string::npos || contenido_val.find(expr_val_upper) != std::string::npos)
            {
                size_t pos = 0;

                while ((pos = contenido_modificado.find(expr_val, pos)) != std::string::npos)
                {
                    contenido_modificado.replace(pos, expr_val.length(), repl_val);

                    pos += repl_val.length();

                    modificado_bool = true;
                }

                pos = 0;

                while ((pos = contenido_modificado.find(expr_val_upper, pos)) != std::string::npos)
                {
                    std::string repl_val_upper = repl_val;
                    std::transform(repl_val_upper.begin(), repl_val_upper.end(), repl_val_upper.begin(), ::toupper);
                    contenido_modificado.replace(pos, expr_val_upper.length(), repl_val_upper);

                    pos += repl_val_upper.length();

                    modificado_bool = true;
                }
            }
        }

        // Devolver el contenido modificado solo si hubo cambios
        return modificado_bool ? contenido_modificado : "";
    }
    catch (const std::exception& e)
    {
        // Si ocurre un error al abrir o leer el archivo, simplemente lo ignoramos
        return "";
    }
}

// Recorre recursivamente un directorio y reemplaza las expresiones en archivos de texto
int f_buscar_reemplazar(const std::string& directorio_base, const std::vector<std::string>& expresiones_val, const std::vector<std::string>& reemplazos_val, const std::string& directorio_salida)
{
    // Contador de archivos modificados
    int contador_archivos = 0;

    for (const auto& entry : std::filesystem::recursive_directory_iterator(directorio_base))
    {
        if (entry.is_regular_file())
        {
            std::string ruta_completa = entry.path().string();

            // Intentar procesar el archivo como texto
            std::string contenido_modificado = f_reemplazar_texto(ruta_completa, expresiones_val, reemplazos_val);

            if (!contenido_modificado.empty())
            {
                // Crear la ruta de salida manteniendo la estructura de directorios
                std::string ruta_relativa = std::filesystem::relative(entry.path(), directorio_base).string();

                // Convertir las rutas a std::filesystem::path antes de usar el operador /
                std::filesystem::path subdirectorio_salida = std::filesystem::path(directorio_salida) / std::filesystem::path(ruta_relativa);

                // Crear subdirectorios si no existen
                std::filesystem::create_directories(subdirectorio_salida.parent_path());

                // Construir la ruta completa del archivo de salida
                std::filesystem::path ruta_archivo_salida = std::filesystem::path(directorio_salida) / std::filesystem::path(ruta_relativa);

                // Guardar el archivo modificado en la carpeta de salida
                std::ofstream archivo_salida(ruta_archivo_salida);

                if (archivo_salida.is_open())
                {
                    archivo_salida << contenido_modificado;

                    contador_archivos++;
                }
            }
        }
    }

    // Devolver el número de archivos modificados
    return contador_archivos;
}

// Generar un nombre de directorio único para evitar sobreescribir
std::string f_directorio_salida(const std::string& base_dir)
{
    int contador_val = 1;
    std::string directorio_salida = base_dir;

    while (std::filesystem::exists(directorio_salida))
    {
        directorio_salida = base_dir + " (" + std::to_string(contador_val) + ")";

        contador_val++;
    }

    return directorio_salida;
}

// Bucle infinito
int main()
{
    while (true)
    {
        // Solicitar el directorio de entrada
        std::string directorio_base;

        while (true)
        {
            std::cout << "Enter directory: ";
            std::getline(std::cin, directorio_base);

            if (std::filesystem::exists(directorio_base))
            {
                break;
            }

            std::cout << "Wrong directory\n";
        }

        // Solicitar el número de expresiones a modificar
        int num_expresiones_val;

        while (true)
        {
            std::cout << "Enter number of expressions to replace: ";
            std::cin >> num_expresiones_val;

            if (std::cin.good())
            {
                break;
            }

            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Wrong format\n";
        }

        // Limpiar el buffer de entrada
        std::cin.ignore();

        std::vector<std::string> expresiones_val;
        std::vector<std::string> reemplazos_val;

        // Solicitar cada expresión y su reemplazo
        for (int iter = 0; iter < num_expresiones_val; ++iter)
        {
            std::string expr_val, repl_val;
            std::cout << "Enter expression " << iter + 1 << ": ";
            std::getline(std::cin, expr_val);

            std::cout << "Replace '" << expr_val << "' with: ";
            std::getline(std::cin, repl_val);

            expresiones_val.push_back(expr_val);
            reemplazos_val.push_back(repl_val);
        }

        // Crear un directorio de salida único
        std::string directorio_salida = f_directorio_salida("Output files");
        std::filesystem::create_directory(directorio_salida);

        // Buscar y reemplazar en el directorio
        int contador_archivos = f_buscar_reemplazar(directorio_base, expresiones_val, reemplazos_val, directorio_salida);

        // Mostrar el número de archivos modificados
        std::cout << "------------------------------------\n";

        if (contador_archivos == 0)
        {
            std::cout << "No modified files\n";
        }
        else if (contador_archivos == 1)
        {
            std::cout << "1 modified file\n";
        }
        else
        {
            std::cout << contador_archivos << " modified files\n";
        }

        std::cout << "------------------------------------\n\n";
    }

    return 0;
}