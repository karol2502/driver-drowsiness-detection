import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Signal, QCoreApplication

from appState import AppState

class MainMenuWidget(QtWidgets.QWidget):
    changed_state = Signal(AppState)

    def __init__(self):
        super().__init__()

        # Create layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create buttons
        self.detection = QtWidgets.QPushButton("Detection")
        self.detection.clicked.connect(lambda: self.change_state(AppState.Detection))

        self.settings = QtWidgets.QPushButton("Settings")
        self.settings.clicked.connect(lambda: self.change_state(AppState.Settings))

        self.statistics = QtWidgets.QPushButton("Statistics")
        self.statistics.clicked.connect(lambda: self.change_state(AppState.Statistics))

        self.exit = QtWidgets.QPushButton("Exit")
        self.exit.clicked.connect(sys.exit)

        # Add buttons to layout
        self.layout.addWidget(self.detection)
        #self.layout.addWidget(self.settings)
        #self.layout.addWidget(self.statistics)
        self.layout.addWidget(self.exit)

    def change_state(self, state):
        self.changed_state.emit(state)