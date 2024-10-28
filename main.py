import hashlib
import os
import subprocess
from tkinter import Tk, filedialog

# Colores utilizados en el terminal
red = '\033[31m'
yellow = '\033[93m'
lgreen = '\033[92m'
clear = '\033[0m'
bold = '\033[01m'
blue = '\033[94m'
purple = '\033[95m'
white = '\033[97m'

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
Tk().withdraw()  # Retirar ventana de tkinter, ya que no es necesaria.
file_path = filedialog.askopenfilename()

# Comprobar si se ha seleccionado un archivo
if not file_path:
    print(red + "No se seleccionó ningún archivo. Saliendo del programa." + clear)
    exit()

# Mostrar la ruta del archivo seleccionado
print(lgreen + f"Archivo seleccionado: {file_path}" + clear)

# Obtener solo el nombre del archivo para el tsr
file_name = os.path.basename(file_path)
tsr_file_name = f"{file_name}.tsr"

# Opciones del menú de hashing
print(white + bold + """
      
Selecciona el método de hashing:
1. SHA-1
2. SHA-224
3. SHA-256
4. SHA-384
5. SHA-512
""")

# Solicitar selección de hash
while True:
    try:
        selection = int(input(white + "Introduce el número correspondiente a tu opción: "))
        if selection in [1, 2, 3, 4, 5]:
            break
        else:
            print(red + "Opción inválida. Por favor elige entre 1 y 5." + clear)
    except ValueError:
        print(red + "Por favor introduce un número válido." + clear)

print(yellow + bold + "Procesando el hash . . ." + clear)

# Diccionario de algoritmos de hashing compatibles con FreeTSA
algorithms = {1: "sha1", 2: "sha224", 3: "sha256", 4: "sha384", 5: "sha512"}

# Generar el hash del archivo seleccionado usando file_digest
with open(file_path, "rb") as file:
    digest = hashlib.file_digest(file, algorithms[selection])

# Mostrar el resultado del hash
hash_type = ["SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512"][selection - 1]
print(lgreen + "================================================================================================================" + lgreen)
print(lgreen + f"Hash de tipo {hash_type} generado con éxito:    " + purple + digest.hexdigest())
print(lgreen + "================================================================================================================" + lgreen)

# Crear archivo de solicitud de sellado de tiempo (TSQ)
tsq_file_name = f"{file_name}.tsq"
subprocess.run(
    ["openssl", "ts", "-query", "-data", file_path, f"-{algorithms[selection]}", "-no_nonce", "-out", tsq_file_name]
)

# Enviar la solicitud a FreeTSA para obtener el sello de tiempo (TSR)
print(yellow + bold + "Enviando solicitud de sellado de tiempo a FreeTSA..." + clear)
subprocess.run(
    ["curl", "-H", "Content-Type: application/timestamp-query", "--data-binary", f"@{tsq_file_name}", "https://freetsa.org/tsr", "-o", tsr_file_name]
)

print(lgreen + f"Sello de tiempo generado con éxito y guardado en: {tsr_file_name}" + clear)


