import hashlib
import os
import time
import subprocess
from openpyxl import Workbook

# Definir la carpeta donde se guardarán los archivos generados (.tsq y .tsr) y crearla si no existe
generated_files_folder = "generatedtestfiles"
os.makedirs(generated_files_folder, exist_ok=True)

def measure_hash_and_timestamp(file_path, hash_type, file_type):
    # Crear nombres únicos para los archivos TSQ y TSR usando el tipo de hash y el tipo de archivo
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    tsq_file_name = os.path.join(generated_files_folder, f"{hash_type}_{file_type}_{base_name}.tsq")
    tsr_file_name = os.path.join(generated_files_folder, f"{hash_type}_{file_type}_{base_name}.tsr")

    # Calcular el hash del archivo
    with open(file_path, "rb") as file:
        digest = hashlib.file_digest(file, hash_type)
    hash_time = digest.hexdigest()  # Guardar el hash en formato hexadecimal para los resultados
    
    # Crear el archivo TSQ para el sellado de tiempo
    start_hash_time = time.time()  # Iniciar el temporizador para medir el tiempo del hashing
    subprocess.run(
        ["openssl", "ts", "-query", "-data", file_path, f"-{hash_type}", "-no_nonce", "-out", tsq_file_name]
    )
    hash_duration = time.time() - start_hash_time  # Tiempo total del cálculo de hash

    # Generar el archivo TSR enviando la solicitud a FreeTSA
    start_ts_time = time.time()  # Iniciar el temporizador para medir el tiempo de timestamping
    subprocess.run(
        ["curl", "-H", "Content-Type: application/timestamp-query", "--data-binary", f"@{tsq_file_name}", 
         "https://freetsa.org/tsr", "-o", tsr_file_name]
    )
    timestamp_duration = time.time() - start_ts_time  # Tiempo total de generación del TSR

    return hash_time, hash_duration, timestamp_duration

def log_to_excel(results, file_name="results.xlsx"):
    # Crear un nuevo archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Hash and Timestamp Results"

    # Definir encabezados para las columnas
    headers = ["Tipo de Archivo", "Tamaño (MB)", "Método Hash", "Digest Hash", "Tiempo de Hash (s)", "Tiempo de Timestamp (s)"]
    ws.append(headers)

    # Escribir los resultados en el Excel
    for result in results:
        ws.append(result)

    wb.save(file_name)  # Guardar el archivo Excel en el directorio del proyecto

def run_tests(folder_path, hash_algorithms):
    results = []  # Lista para almacenar los resultados
    
    for hash_algo in hash_algorithms:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = os.path.basename(root)  # El nombre de la carpeta indica el tipo de archivo
                
                # Parsear el tamaño del archivo desde su nombre (e.g., "5.mp4" -> 5 MB)
                try:
                    file_size = float(os.path.splitext(file)[0])
                except ValueError:
                    print(f"Omitiendo {file} - no se pudo extraer el tamaño desde el nombre.")
                    continue

                # Ejecutar las pruebas de hashing y timestamping
                hash_digest, hash_duration, timestamp_duration = measure_hash_and_timestamp(file_path, hash_algo, file_type)
                results.append([file_type, file_size, hash_algo.upper(), hash_digest, hash_duration, timestamp_duration])
    
    # Guardar los resultados en un archivo Excel en el directorio del proyecto
    log_to_excel(results, file_name="results.xlsx")
    print("Resultados de la prueba guardados en results.xlsx en el directorio del proyecto.")

# Ejemplo de uso
folder_path = "C:/Users/villa/Desktop/testingfiles"  # Reemplaza con la ruta de la carpeta principal que contiene las subcarpetas de cada tipo de archivo
hash_algorithms = ["sha1", "sha224", "sha256", "sha384", "sha512"]  # Tipos de hash soportados por tu GUI
run_tests(folder_path, hash_algorithms)