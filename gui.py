import sys
import hashlib
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QHBoxLayout, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt

class DocuSeguro(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.hashed_files = {}
        self.load_existing_files()

    def initUI(self):
        # Configuración de la ventana
        self.setWindowTitle("DocuSeguro")
        self.setFixedSize(1200, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #0e0e0f;
                color: #e1e1e1;
                font-family: Arial, sans-serif;
            }
            QLabel, QComboBox {
                font-size: 18px;
                padding: 5px;
            }
            QPushButton {
                background-color: #0070f3;
                border: none;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QFrame {
                background-color: #1a1a1b;
                padding: 5px;
            }
        """)

        # Diseño principal
        main_layout = QHBoxLayout()

        # Barra lateral para Mis Archivos
        self.sidebar = QFrame()
        sidebar_layout = QVBoxLayout()

        # Botón para volver al inicio (ícono de + blanco)
        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon("plus-icon.png"))  # Asegúrate de tener un icono blanco
        self.home_button.setStyleSheet("background-color: #28a745;")  # Verde
        self.home_button.setToolTip("Volver al inicio")
        self.home_button.clicked.connect(self.go_home)
        sidebar_layout.addWidget(self.home_button)

        self.works_list = QListWidget()
        font = QFont()
        font.setPointSize(13)  # Increase the font size here
        self.works_list.setFont(font)
        self.works_list.currentItemChanged.connect(self.show_hash_info)

        sidebar_layout.addWidget(QLabel("Mis Archivos"))
        sidebar_layout.addWidget(self.works_list)

        self.sidebar.setLayout(sidebar_layout)
        self.sidebar.setFixedWidth(300)
        main_layout.addWidget(self.sidebar)

        # Área de contenido principal
        self.content_area = QFrame()
        content_layout = QVBoxLayout()

        # Botón de selección de archivo
        self.select_file_button = QPushButton("Seleccione un archivo:")
        self.select_file_button.clicked.connect(self.select_file)
        content_layout.addWidget(self.select_file_button)

        # Selección del método de hashing
        self.hash_label = QLabel("Seleccione el algoritmo de Hashing a usar:")
        content_layout.addWidget(self.hash_label)

        self.hash_combo = QComboBox()
        self.hash_combo.addItems(["SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512"])
        content_layout.addWidget(self.hash_combo)

        # Mostrar la ruta del archivo seleccionado
        self.file_info_label = QLabel("Archivo no seleccionado.")
        content_layout.addWidget(self.file_info_label)

        # Mostrar el resultado del hash (oculto inicialmente)
        self.hash_result_label = QLabel("")
        content_layout.addWidget(self.hash_result_label)
        self.hash_result_label.hide()

        # Botón del icono de ojo para alternar la visibilidad del hash (oculto inicialmente)
        self.eye_button = QPushButton("👁️")
        self.eye_button.clicked.connect(self.toggle_hash_visibility)
        self.eye_button.setEnabled(False)
        self.eye_button.hide()
        content_layout.addWidget(self.eye_button)

        # Botón para ejecutar el hash
        self.run_button = QPushButton("Cifrar y Sellar")
        self.run_button.clicked.connect(self.generate_hash)
        content_layout.addWidget(self.run_button)

        self.content_area.setLayout(content_layout)
        main_layout.addWidget(self.content_area)

        # Establecer el diseño principal en la ventana
        self.setLayout(main_layout)

    def load_existing_files(self):
        # Cargar archivos desde carpetas que comienzan con "f_"
        for folder in os.listdir('.'):
            if folder.startswith('f_') and os.path.isdir(folder):
                info_file = os.path.join(folder, "filename_info.txt")
                if os.path.exists(info_file):
                    with open(info_file, "r") as f:
                        lines = f.readlines()
                        if len(lines) >= 3:
                            file_name = lines[0].strip().split(": ")[1]
                            file_name_no_ext = os.path.splitext(file_name)[0]
                            hash_method = lines[1].strip().split(": ")[1]
                            hash_value = lines[2].strip().split(": ")[1]
                            self.hashed_files[file_name_no_ext] = (hash_value, hash_method)
                            self.update_sidebar(file_name_no_ext, hash_value)
                        else:
                            print(f"El archivo {info_file} no tiene suficientes líneas.")

    def go_home(self):
        self.works_list.clearSelection()  # Deselect any selected file
        self.run_button.show()
        self.eye_button.show()
        self.hash_label.show()
        self.hash_combo.show()
        self.select_file_button.show()

        self.file_info_label.setText("Archivo no seleccionado.")  # Reset file selection
        self.hash_result_label.hide()  # Hide hash result
        self.eye_button.hide()  # Hide eye button

    def select_file(self):
        self.hash_result_label.hide()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo")
        if file_path:
            self.file_path = file_path
            self.file_info_label.setText(f"Archivo: {os.path.basename(file_path)}")
        else:
            self.file_path = None
            self.file_info_label.setText("Archivo no seleccionado.")

    def generate_hash(self):
        if not self.file_path:
            self.hash_result_label.setText("Por favor, seleccione un archivo")
            return

        hash_type = self.hash_combo.currentText().lower().replace("-", "")
        
        # Usar hashlib.file_digest para calcular el hash directamente
        with open(self.file_path, "rb") as file:
            digest = hashlib.file_digest(file, hash_type)

        # Crear una carpeta para almacenar los resultados
        file_name = os.path.basename(self.file_path)
        file_name_no_ext = os.path.splitext(file_name)[0]
        folder_name = f"f_{file_name_no_ext}"
        os.makedirs(folder_name, exist_ok=True)

        # Crear archivo de solicitud de sellado de tiempo (TSQ)
        tsq_file_name = os.path.join(folder_name, f"{file_name}.tsq")
        subprocess.run(
            ["openssl", "ts", "-query", "-data", self.file_path, f"-{hash_type}", "-no_nonce", "-out", tsq_file_name]
        )
        
        # Generar TSR y guardarlo en la misma carpeta
        tsr_file_name = os.path.join(folder_name, f"{file_name}.tsr")
        subprocess.run(
            ["curl", "-H", "Content-Type: application/timestamp-query", "--data-binary", f"@{tsq_file_name}", "https://freetsa.org/tsr", "-o", tsr_file_name]
        )

        # Guardar información del hash
        info_file = os.path.join(folder_name, "filename_info.txt")
        with open(info_file, "w") as f:
            f.write(f"File Name: {file_name}\n")
            f.write(f"Hash Method: {self.hash_combo.currentText()}\n")
            f.write(f"Hash: {digest.hexdigest()}\n")

        # Almacenar el hash para la barra lateral
        self.hashed_files[file_name_no_ext] = (digest.hexdigest(), self.hash_combo.currentText())
        self.update_sidebar(file_name_no_ext, digest.hexdigest())

        # Mostrar resultado
        self.hash_result_label.setText("Archivo Cifrado y Sellado Exitosamente.")
        self.hash_result_label.hide()  # Ocultar resultado hasta que se seleccione
        self.eye_button.setEnabled(True)
        self.eye_button.hide()  # Ocultar botón de ojo hasta que se seleccione


    def update_sidebar(self, file_name_no_ext, hash_value):
        item = QListWidgetItem(file_name_no_ext)
        item.setData(Qt.ItemDataRole.UserRole, hash_value)  # Almacenar el valor del hash en el ítem
        self.works_list.addItem(item)

    def show_hash_info(self, current):
        self.run_button.hide()
        self.eye_button.hide()
        self.hash_label.hide()
        self.hash_combo.hide()
        self.select_file_button.hide()
        if current:
            file_name = current.text()
            hash_value, method = self.hashed_files[file_name]
            self.file_info_label.setText(f"Archivo: {file_name} \nMétodo: {method}\n")  # Muestra el hash como "●"
            self.hash_result_label.show()  # Mostrar resultado del hash
            self.eye_button.setEnabled(True)  # Habilitar botón de ojo para este ítem
            self.eye_button.show()  # Mostrar botón de ojo
        else:
            self.file_info_label.setText("Archivo no seleccionado.")  # Reset info label when no item selected
            self.hash_result_label.hide()  # Ocultar resultado cuando no se selecciona ningún ítem
            self.eye_button.setEnabled(False)
            self.eye_button.hide()  # Ocultar botón de ojo

    def toggle_hash_visibility(self):
        if self.eye_button.text() == "👁️":  # Si el ojo está cerrado
            self.eye_button.setText("👁️‍🗨️")  # Cambia a ojo abierto
            current_item = self.works_list.currentItem()
            if current_item:
                file_name = current_item.text()
                hash_value, _ = self.hashed_files[file_name]
                self.hash_result_label.setText(f"Hash: {hash_value}")  # Muestra el hash real
        else:  # Si el ojo está abierto
            self.eye_button.setText("👁️")  # Cambia a ojo cerrado
            current_item = self.works_list.currentItem()
            if current_item:
                file_name = current_item.text()
                hash_value, _ = self.hashed_files[file_name]
                self.hash_result_label.setText(f"Hash: {'●' * len(hash_value)}")  # Muestra el hash como "●"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = DocuSeguro()
    dashboard.show()
    sys.exit(app.exec())


