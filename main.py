import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
import os


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("des.ui", self)
        self.map_zoom = 8
        self.delte = 0.1
        self.map_ll = [37.621202, 55.753544]
        self.map_l = "map"
        self.api_server = "https://static-maps.yandex.ru/1.x/"
        self.flag = False
        self.refresh_map()
        self.pushButton.clicked.connect(self.set_map)
        self.pushButton_2.clicked.connect(self.set_sat)
        self.pushButton_3.clicked.connect(self.set_gibrid)
        self.pushButton_4.clicked.connect(self.search)

    def keyPressEvent(self, event):
        ## Другие кнопки кроме цифр не работают!!!!
        if event.key() == Qt.Key.Key_PageUp and self.map_zoom <= 20:
            self.map_zoom += 1
        if event.key() == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if event.key() == Qt.Key.Key_1:
            self.map_ll[0] -= self.delte
        if event.key() == Qt.Key.Key_2:
            self.map_ll[0] += self.delte
        if event.key() == Qt.Key.Key_3:
            self.map_ll[1] += self.delte
        if event.key() == Qt.Key.Key_4:
            self.map_ll[1] -= self.delte
        self.refresh_map()

    def search(self):
        pass

    def set_sat(self):
        self.map_l = "sat"
        self.refresh_map()

    def set_map(self):
        self.map_l = "map"
        self.refresh_map()

    def set_gibrid(self):
        self.map_l = "sat,skl"
        self.refresh_map()


    def refresh_map(self):
            map_params = {
                "ll": ','.join(map(str, self.map_ll)),
                "l": self.map_l,
                "z": self.map_zoom
            }
            response = requests.get(self.api_server, params=map_params)
            if not response:
                print("Ошибка выполнения запроса")
                print("Http статус", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.LabelText.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

