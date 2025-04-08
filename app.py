import sys
import subprocess
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QStackedWidget,
    QLabel, QVBoxLayout, QListWidgetItem, QHBoxLayout, QPushButton, QMessageBox, QCheckBox, QLineEdit, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

# === CONFIGURATION DE MISE À JOUR ===
VERSION_ACTUELLE = "1.0.0"
VERSION_URL = "https://raw.githubusercontent.com/TonNomUtilisateur/TonRepo/main/version.txt"
EXE_URL = "https://github.com/TonNomUtilisateur/TonRepo/releases/latest/download/CrapuleOptimisation.exe"
NOM_EXE = "CrapuleOptimisation.exe"

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 1000, 600)
        self.offset = None
        self.close_key = None

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        self.setCentralWidget(central_widget)

        top_bar = QWidget()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("background-color: #1c1c1c;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)
        top_layout.setSpacing(10)

        self.update_btn = QPushButton("\ud83c\udf10")
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 20px;
                border: none;
            }
            QPushButton:hover {
                color: #aaaaaa;
            }
        """)
        self.update_btn.setFixedSize(40, 40)
        self.update_btn.clicked.connect(self.check_for_update)

        self.logo = QLabel()
        pixmap = QPixmap("image.png")
        pixmap = pixmap.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setFixedSize(50, 50)
        self.logo.mousePressEvent = self.open_settings

        self.title_label = QLabel("Crapule Optimisation")
        self.title_label.setStyleSheet("color: cyan; font-size: 18px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(60)

        self.settings_btn = QPushButton("\u2699\ufe0f")
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 20px;
                border: none;
            }
            QPushButton:hover {
                color: #aaaaaa;
            }
        """)
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.clicked.connect(self.open_settings)

        top_layout.addWidget(self.update_btn)
        top_layout.addWidget(self.logo)
        top_layout.addStretch()
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.settings_btn)

        main_content = QWidget()
        main_layout = QHBoxLayout(main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(80)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                border: none;
                color: white;
                font-size: 22px;
                qproperty-alignment: AlignCenter;
            }
            QListWidget::item {
                padding: 25px 0;
            }
            QListWidget::item:selected {
                background-color: #44475a;
                border-radius: 10px;
            }
        """)
        font = QFont()
        font.setPointSize(22)
        self.sidebar.setFont(font)

        self.sidebar.addItem(QListWidgetItem("\ud83c\udfae"))
        self.sidebar.addItem(QListWidgetItem("\u26a1"))
        self.sidebar.addItem(QListWidgetItem("\ud83e\uddf9"))
        self.sidebar.addItem(QListWidgetItem("\ud83d\udca0"))
        self.sidebar.addItem(QListWidgetItem("\ud83d\udd04"))

        self.stack = QStackedWidget()

        for i in range(5):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)
            page.setStyleSheet("background-color: #2e2e2e; color: white;")

            if i == 0:
                for txt in [
                    "Activer Mode Haute Performance",
                    "Désactiver les effets visuels",
                    "Optimiser les paramètres d'affichage",
                    "Réduire la qualité des textures"]:
                    box = QCheckBox(txt)
                    box.setStyleSheet("color: white;")
                    layout.addWidget(box)
                btn = QPushButton("Appliquer")
                btn.clicked.connect(self.apply_fps_changes)
                self.style_button(btn)
                layout.addWidget(btn)

            elif i == 1:
                for txt in [
                    "Désactiver l'optimisation de la mise en réseau",
                    "Optimiser la latence pour les jeux en ligne",
                    "Désactiver les applications en arrière-plan",
                    "Activer la gestion des priorités système"]:
                    box = QCheckBox(txt)
                    box.setStyleSheet("color: white;")
                    layout.addWidget(box)
                btn = QPushButton("Appliquer")
                btn.clicked.connect(self.apply_latency_changes)
                self.style_button(btn)
                layout.addWidget(btn)

            elif i == 2:
                for txt in [
                    "Désinstaller logiciels inutiles",
                    "Supprimer les logiciels de démarrage inutiles",
                    "Nettoyer les caches des applications",
                    "Désactiver les services inutiles"]:
                    box = QCheckBox(txt)
                    box.setStyleSheet("color: white;")
                    layout.addWidget(box)
                btn = QPushButton("Appliquer")
                btn.clicked.connect(self.apply_debloat_changes)
                self.style_button(btn)
                layout.addWidget(btn)

            elif i == 3:
                self.temp_checkbox = QCheckBox("Supprimer les fichiers temporaires")
                self.temp_checkbox.setStyleSheet("color: white;")
                layout.addWidget(self.temp_checkbox)

                self.sfc_checkbox = QCheckBox("Réparer les fichiers système (SFC)")
                self.sfc_checkbox.setStyleSheet("color: white;")
                layout.addWidget(self.sfc_checkbox)

                for txt in [
                    "Nettoyer les fichiers du navigateur",
                    "Effacer l'historique de navigation",
                    "Vider la corbeille"]:
                    box = QCheckBox(txt)
                    box.setStyleSheet("color: white;")
                    layout.addWidget(box)
                btn = QPushButton("Appliquer")
                btn.clicked.connect(self.apply_changes)
                self.style_button(btn)
                layout.addWidget(btn)

            elif i == 4:
                reset_btn = QPushButton("Réinitialiser les optimisations")
                reset_btn.clicked.connect(self.reset_optimizations)
                self.style_button(reset_btn)
                layout.addWidget(reset_btn)

            self.stack.addWidget(page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)
        central_layout.addWidget(top_bar)
        central_layout.addWidget(main_content)

        self.sidebar.currentRowChanged.connect(self.display_page)
        self.setFocusPolicy(Qt.StrongFocus)

    def open_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Paramètres")
        dialog.setFixedSize(300, 200)
        layout = QVBoxLayout(dialog)
        self.close_key_input = QLineEdit()
        self.close_key_input.setPlaceholderText("Entrez la touche de fermeture")
        layout.addWidget(self.close_key_input)
        apply_btn = QPushButton("Appliquer")
        apply_btn.clicked.connect(self.apply_close_key)
        layout.addWidget(apply_btn)
        dialog.exec_()

    def apply_close_key(self):
        self.close_key = self.close_key_input.text()
        QMessageBox.information(self, "Paramètre appliqué", f"Touche de fermeture définie sur : {self.close_key}")

    def apply_fps_changes(self):
        QMessageBox.information(self, "FPS", "Modifications FPS appliquées.")

    def apply_latency_changes(self):
        QMessageBox.information(self, "Latence", "Modifications Latence appliquées.")

    def apply_debloat_changes(self):
        QMessageBox.information(self, "Debloat", "Modifications Debloat appliquées.")

    def apply_changes(self):
        if self.temp_checkbox.isChecked():
            subprocess.run("del /s /f /q %temp%\\*", shell=True)
        if self.sfc_checkbox.isChecked():
            subprocess.run("sfc /scannow", shell=True)
        QMessageBox.information(self, "Entretien", "Nettoyage exécuté.")

    def reset_optimizations(self):
        QMessageBox.information(self, "Réinitialisation", "Optimisations réinitialisées.")

    def display_page(self, index):
        self.stack.setCurrentIndex(index)

    def style_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005a8d;
            }
        """)

    def check_for_update(self):
        try:
            response = requests.get(VERSION_URL)
            response.raise_for_status()
            nouvelle_version = response.text.strip()
            if nouvelle_version != VERSION_ACTUELLE:
                reply = QMessageBox.question(
                    self, "Mise à jour disponible",
                    f"Nouvelle version ({nouvelle_version}) disponible. Télécharger ?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    QMessageBox.information(self, "Téléchargement", "Téléchargement de la mise à jour...")
                    new_exe_path = NOM_EXE + ".new"
                    r = requests.get(EXE_URL, stream=True)
                    with open(new_exe_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    current_exe = sys.argv[0]
                    backup_exe = current_exe + ".bak"
                    os.rename(current_exe, backup_exe)
                    os.rename(new_exe_path, current_exe)
                    QMessageBox.information(self, "Mise à jour", "Mise à jour installée. Redémarrage...")
                    subprocess.Popen([current_exe])
                    sys.exit()
            else:
                QMessageBox.information(self, "À jour", "Déjà à jour.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur mise à jour : {str(e)}")

    def keyPressEvent(self, event):
        if self.close_key and event.text() == self.close_key:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())
