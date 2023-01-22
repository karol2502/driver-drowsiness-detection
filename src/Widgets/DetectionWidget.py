from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Signal, QThread
from Detection.eyesDetection import EyesDetection

from appState import AppState

class DetectionWidget(QtWidgets.QWidget):
    changed_state = Signal(AppState)

    def __init__(self):
        super().__init__()

        # Create layout
        self.layout = QtWidgets.QVBoxLayout(self)

        self.eyes_detection = EyesDetection()

        self.thread = QThread()
        self.eyes_detection.moveToThread(self.thread)
        self.thread.started.connect(self.eyes_detection.detecting)

        # Create buttons
        self.start = QtWidgets.QPushButton("Start")
        self.start.clicked.connect(self.startDetecting)

        self.stop = QtWidgets.QPushButton("Stop")
        self.stop.clicked.connect(self.stopDetecting)

        self.go_back = QtWidgets.QPushButton("Go back")
        self.go_back.clicked.connect(self.exitDetection)

        # Add buttons to layout
        self.layout.addWidget(self.start)
        self.layout.addWidget(self.stop)
        self.layout.addWidget(self.go_back)


    def exitDetection(self, event):
        self.changed_state.emit(AppState.MainMenu)

    def startDetecting(self):
        self.eyes_detection.change_detecting_state()
        self.thread.start()

    def stopDetecting(self):
        self.eyes_detection.change_detecting_state()
        self.thread.exit()