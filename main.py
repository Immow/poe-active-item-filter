import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget,
                             QSystemTrayIcon, QMenu, QPushButton, QHeaderView)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

class PoEFilterManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PoE Active Hider")
        self.resize(500, 400)

        # 1. Main Table Setup
        self.table = QTableWidget(0, 2) # 0 rows, 2 columns
        self.table.setHorizontalHeaderLabels(["Item Base", "Date Hidden"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 2. Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        btn_remove = QPushButton("Remove Selected Item")
        btn_remove.clicked.connect(self.remove_item)
        layout.addWidget(btn_remove)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 3. System Tray Setup
        self.tray_icon = QSystemTrayIcon(self)
        # For this demo, we'll use a standard theme icon
        self.tray_icon.setIcon(QIcon.fromTheme("visibility-off"))

        tray_menu = QMenu()
        show_action = QAction("Show Manager", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Add some dummy data to see how it looks
        self.add_item_to_table("Glass Shank", "2026-03-05")
        self.add_item_to_table("Rusted Sword", "2026-03-05")

    def add_item_to_table(self, name, date):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(date))

    def remove_item(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    # Minimize to tray instead of closing
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "PoE Active Hider",
            "App is still running in the tray.",
            QSystemTrayIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep tray alive when window is hidden

    window = PoEFilterManager()
    window.show()
    sys.exit(app.exec())