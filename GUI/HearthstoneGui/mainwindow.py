# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.allyHand.idClicked.connect(self.allyCardClicked)
        self.ui.allyBoard.idClicked.connect(self.allyBoardClicked)
        self.ui.enemyBoard.idClicked.connect(self.enemyBoardClicked)
        self.ui.enemyHero.clicked.connect(lambda: self.ui.statusLabel.setText('Enemy hero clicked'))
        self.ui.allyHero.clicked.connect(lambda: self.ui.statusLabel.setText('Ally hero clicked'))
    @QtCore.Slot()
    def enemyBoardClicked(self, id):
        self.ui.statusLabel.setText(f'Enemy board minion clicked {id}')

    @QtCore.Slot()
    def allyBoardClicked(self, id):
        self.ui.statusLabel.setText(f'Ally board minion clicked {id}')

    @QtCore.Slot()
    def allyCardClicked(self, id):
        self.ui.statusLabel.setText(f'Ally card clicked {id}')


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
