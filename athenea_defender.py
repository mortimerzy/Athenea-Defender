# ATHENEA Defender – Final Version
# Created by Mortimer :)
# Supported by LUMINA

import sys
import os
import random
import socket
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QListWidget, QWidget
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation

# --------------------
# PyInstaller resource path
# --------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

# --------------------
# Main Window
# --------------------
class AtheneaDefender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATHENEA Defender")
        self.setFixedSize(900, 550)
        self.setWindowIcon(QIcon(resource_path("athenea.ico")))

        # --------------------
        # Load font
        # --------------------
        font_path = resource_path("Bauhaus93.ttf")
        QFont.insertSubstitution("Bauhaus 93", "Arial")
        self.main_font = QFont("Bauhaus 93", 12)
        self.setFont(self.main_font)

        # --------------------
        # Central widget
        # --------------------
        self.central = QWidget(self)
        self.setCentralWidget(self.central)
        self.central.setStyleSheet("""
            QWidget {
                background-color: #000000;
                color: white;
            }
            QPushButton {
                background-color: #ffffff;
                color: black;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
        """)

        # --------------------
        # Mascot
        # --------------------
        self.mascot = QLabel(self.central)
        self.mascot.setGeometry(20, 50, 200, 200)
        self.state = "idle"

        self.sprites = {
            "idle1": QPixmap(resource_path("athenea_idle1.png")),
            "idle2": QPixmap(resource_path("athenea_idle2.png")),
            "alert": QPixmap(resource_path("athenea_alert.png")),
            "sleep": QPixmap(resource_path("athenea_sleep.png"))
        }

        self.mascot.setPixmap(self.sprites["idle1"].scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Animation
        self.fade = QPropertyAnimation(self.mascot, b"windowOpacity")
        self.fade.setDuration(600)

        # --------------------
        # Speech bubble
        # --------------------
        self.speech = QLabel(self.central)
        self.speech.setGeometry(20, 260, 200, 60)
        self.speech.setAlignment(Qt.AlignCenter)
        self.speech.setWordWrap(True)
        self.speech.setStyleSheet("background-color: white; color: black; border-radius: 10px;")

        self.idle_phrases = [
            "¿Todo tranquilo hoy?",
            "ATHENEA vigilando.",
            "Sistema estable.",
            "Siempre atenta.",
            "¿Cómo te sientes hoy?"
        ]

        # --------------------
        # Lists
        # --------------------
        self.ip_list = QListWidget(self.central)
        self.ip_list.setGeometry(260, 60, 250, 180)

        self.process_list = QListWidget(self.central)
        self.process_list.setGeometry(540, 60, 320, 180)

        # --------------------
        # Buttons
        # --------------------
        self.scan_btn = QPushButton("Analizar", self.central)
        self.scan_btn.setGeometry(260, 260, 120, 40)
        self.scan_btn.clicked.connect(self.scan_system)

        self.isolate_btn = QPushButton("Aislar red", self.central)
        self.isolate_btn.setGeometry(400, 260, 120, 40)
        self.isolate_btn.clicked.connect(self.isolate_network)

        self.reconnect_btn = QPushButton("Reconectar", self.central)
        self.reconnect_btn.setGeometry(540, 260, 120, 40)
        self.reconnect_btn.clicked.connect(self.restore_network)

        # --------------------
        # Credits
        # --------------------
        self.credits = QLabel(
            "Created by Mortimer :)\nSupported by LUMINA",
            self.central
        )
        self.credits.setGeometry(20, 460, 300, 60)
        self.credits.setStyleSheet("color: #bbbbbb;")

        # --------------------
        # Timers
        # --------------------
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(60000)

        self.network_timer = QTimer()
        self.network_timer.timeout.connect(self.check_network)
        self.network_timer.start(5000)

        self.say_idle()

    # --------------------
    # Mascot behaviors
    # --------------------
    def blink(self):
        if self.state == "idle":
            self.mascot.setPixmap(self.sprites["idle2"].scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            QTimer.singleShot(300, lambda: self.mascot.setPixmap(self.sprites["idle1"].scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)))

    def say_idle(self):
        self.speech.setText(random.choice(self.idle_phrases))

    def set_state(self, state):
        self.state = state
        self.fade.stop()
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.start()

        if state == "idle":
            self.mascot.setPixmap(self.sprites["idle1"].scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.say_idle()
        elif state == "alert":
            self.mascot.setPixmap(self.sprites["alert"].scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.speech.setText("Preparada para actuar")
        elif state == "sleep":
            self.mascot.setPixmap(self.sprites["sleep"].scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.speech.setText("Z Z Z")

    # --------------------
    # System logic
    # --------------------
    def scan_system(self):
        self.ip_list.clear()
        self.process_list.clear()

        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.ip_list.addItem(ip)
        except:
            pass

        for proc in psutil.process_iter(['name']):
            self.process_list.addItem(proc.info['name'])

        self.set_state("idle")

    def isolate_network(self):
        os.system("ipconfig /release")
        self.set_state("sleep")

    def restore_network(self):
        os.system("ipconfig /renew")
        self.set_state("idle")

    def check_network(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            if self.state == "sleep":
                self.set_state("idle")
        except:
            self.set_state("sleep")


# --------------------
# Run
# --------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AtheneaDefender()
    window.show()
    sys.exit(app.exec_())
