# Importa las funciones necesarias
import hashlib
from tkinter import Tk, filedialog

# Colores utilizados en el terminal
red = '\033[31m'
yellow = '\033[93m'
lgreen = '\033[92m'
clear = '\033[0m'
bold = '\033[01m'
cyan = '\033[96m'
purple = '\033[95m'
white = '\033[97m'
blue = '\033[94m'

# Banner de la herramienta
print(blue + bold + """
================================================================================================================""" + white + bold + """

██████╗ ███████╗██████╗ ███████╗███████╗    ██████╗ ███████╗                                           
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔════╝                                           
██████╔╝█████╗  ██║  ██║█████╗  ███████╗    ██║  ██║█████╗                                             
██╔══██╗██╔══╝  ██║  ██║██╔══╝  ╚════██║    ██║  ██║██╔══╝                                             
██║  ██║███████╗██████╔╝███████╗███████║    ██████╔╝███████╗                                           
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝╚══════╝    ╚═════╝ ╚══════╝                                           
                                                                                                       
 ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗   ██╗████████╗ █████╗ ██████╗  ██████╗ ██████╗  █████╗ ███████╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║   ██║╚══██╔══╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝
██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║   ██║   ███████║██║  ██║██║   ██║██████╔╝███████║███████╗
██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║   ██║   ██║   ██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║╚════██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ╚██████╔╝   ██║   ██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║███████║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
""" + blue + bold + """
================================================================================================================""")

# Mostrar mensaje antes de abrir el explorador de archivos
print(white + bold + "Por favor, elija el archivo a hashear...")

# Configuración para abrir el explorador de archivos (Tk necesaria para funcionalidad de filedialog)
Tk().withdraw() # Retirar ventana de tkinter, ya que no es necesaria.
file_path = filedialog.askopenfilename()

# Comprobar si se ha seleccionado un archivo
if not file_path:
    print(red + "No se seleccionó ningún archivo. Saliendo del programa." + clear)
    exit()

# Mostrar la ruta del archivo seleccionado
print(lgreen + f"Archivo seleccionado: {file_path}" + clear)

# Opciones del menú de hashing
print(white + bold + """
      
Selecciona el método de hashing:
1. MD5
2. SHA-256
3. SHA3-256
""")

# Solicitar selección de hash
while True:
    try:
        selection = int(input(white + "Introduce el número correspondiente a tu opción: "))
        if selection in [1, 2, 3]:
            break
        else:
            print(red + "Opción inválida. Por favor elige 1, 2 o 3." + clear)
    except ValueError:
        print(red + "Por favor introduce un número válido." + clear)

print(yellow + bold + "Procesando . . . . . . . . . . . . . . . . . . . . ." + clear)

# Diccionario de algoritmos de hashing
algorithms = {1: "md5", 2: "sha256", 3: "sha3_256"}

# Generar el hash del archivo seleccionado
with open(file_path, "rb") as file:
    digest = hashlib.file_digest(file, algorithms[selection])

# Mostrar el resultado del hash
hash_type = ["MD5", "SHA-256", "SHA3-256"][selection - 1]
print(lgreen + "================================================================================================================" + lgreen)
print(lgreen + f"Hash de tipo {hash_type} generado con éxito:    " + purple + digest.hexdigest())
print(lgreen + "================================================================================================================" + lgreen)

