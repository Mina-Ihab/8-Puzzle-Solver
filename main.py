from gui.main_menu import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication()

main_window = MainWindow()

main_window.show()

app.exec()
