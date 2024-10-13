# Importa las funciones necesarias
from hashing import generate_hashes

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

# Solicitar string a hashear
hash_value = input(""" 
 |""" + blue + bold + """
 |""" + blue + bold + """
 └──""" + purple + """#""" + cyan + """ Ingresa una cadena para generar Hash: """)


# Opciones del menú
print(white + bold + """
      
Selecciona el método de hashing:
1. MD5
2. SHA-256
3. SHA3-256
""")



# Solicitar selección de hash
while True:
    try:
        selection = int(input(white + """Introduce el número correspondiente a tu opción: """))
        if selection in [1, 2, 3]:
            break
        else:
            print(red + "Opción inválida. Por favor elige 1, 2 o 3." + clear)
    except ValueError:
        print(red + "Por favor introduce un número válido." + clear)



print(yellow + bold + """      
Procesando . . . . . . . . . . . . . . . . . . . . . 
""")


# Llama a la función para generar los hashes
hashes = generate_hashes(hash_value)

print(lgreen + "================================================================================================================" + lgreen)

# Muestra el hash seleccionado
if selection == 1:
    print(lgreen + "Hash de tipo MD5 generado con éxito:    " + purple + hashes['MD5'])
elif selection == 2:
    print(lgreen + "Hash de tipo SHA-256 generado con éxito:    " + purple + hashes['SHA256'])
elif selection == 3:
    print(lgreen + "Hash de tipo SHA3-256 generado con éxito:    " + purple + hashes['SHA3-256'])

print(lgreen + "================================================================================================================" + lgreen)
