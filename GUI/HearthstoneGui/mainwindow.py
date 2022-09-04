# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from fireplace.exceptions import GameOver

from GamePlayer import _setup_game
from ui_mainwindow import Ui_MainWindow
from GameCommunication import *
from fireplace import cards


class MainWindow(QMainWindow):
    def __init__(self, game):
        QMainWindow.__init__(self)
        self.game = game
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.firstClick = None

        self.ui.allyHand.setExclusive(False)
        self.ui.allyBoard.setExclusive(False)
        self.ui.enemyBoard.setExclusive(False)
        self.ui.allyHand.idToggled.connect(lambda clickedId, checked: self.applyClick(0, -clickedId-2) if checked else None)
        self.ui.allyBoard.idToggled.connect(lambda clickedId, checked: self.applyClick(3, -clickedId-2) if checked else None)
        self.ui.enemyBoard.idToggled.connect(lambda clickedId, checked: self.applyClick(5, -clickedId-2) if checked else None)
        self.ui.enemyHero.toggled.connect(lambda checked: self.applyClick(4, 0) if checked else None)
        self.ui.allyHero.toggled.connect(lambda checked: self.applyClick(2, 0) if checked else None)
        self.ui.heroPower.toggled.connect(lambda checked: self.applyClick(1, 0) if checked else None)
        self.ui.endTurnButton.toggled.connect(lambda checked: self.applyClick(6, 0) if checked else None)
        self.refresh()

    def fillHandData(self, id, obj):
        try:
            self.ui.allyHand.buttons()[id].setText(
                f'Name: {obj.data.name}\n'
                f'Cost: {obj.cost}\n'
                f'Hp: {obj.health}\n'
                f'Atk: {obj.atk}\n'
            )
            return
        except:
            pass
        try:
            self.ui.allyHand.buttons()[id].setText(
                f'Name: {obj.data.name}\n'
                f'Cost: {obj.cost}\n'
            )
            return
        except:
            pass
        return

    def fillBoardData(self, id, obj, ally):
        if ally:
            self.ui.allyBoard.buttons()[id].setText(
                f'Name: {obj.data.name}\n'
                f'Cost: {obj.cost}\n'
                f'Hp: {obj.health}\n'
                f'Atk: {obj.atk}\n'
            )
        else:
            self.ui.enemyBoard.buttons()[id].setText(
                f'Name: {obj.data.name}\n'
                f'Cost: {obj.cost}\n'
                f'Hp: {obj.health}\n'
                f'Atk: {obj.atk}\n'
            )
        return

    def updateHeroes(self, allyobj, enemyobj):
        self.ui.allyHero.setText(
            f'Name: {allyobj.data.name}\n'
            f'Hp: {allyobj.health}\n'
            f'Atk: {allyobj.atk}\n'
            f'Mana: {allyobj.game.current_player.mana}\n'
        )
        self.ui.enemyHero.setText(
            f'Name: {enemyobj.data.name}\n'
            f'Hp: {enemyobj.health}\n'
            f'Atk: {enemyobj.atk}\n'
            f'Mana: {allyobj.game.current_player.opponent.mana}\n'
        )
        return

    def refresh(self):
        player = self.game.current_player
        enemy = player.opponent
        for i in range(10):
            if i < len(player.hand):
                self.fillHandData(i, player.hand[i])
                self.ui.allyHand.buttons()[i].show()
            else:
                self.ui.allyHand.buttons()[i].hide()
        for i in range(7):
            if i < len(player.field):
                self.fillBoardData(i, player.field[i], True)
                self.ui.allyBoard.buttons()[i].show()
            else:
                self.ui.allyBoard.buttons()[i].hide()
        for i in range(7):
            if i < len(enemy.field):
                self.fillBoardData(i, enemy.field[i], False)
                self.ui.enemyBoard.buttons()[i].show()
            else:
                self.ui.enemyBoard.buttons()[i].hide()
        self.updateHeroes(player.characters[0], enemy.characters[0])

    def doMove(self, action):
        try:
            playTurnSparse(self.game, action)
        except GameOver:
            QMessageBox.warning(self, 'Game', 'Game Finished!')
        except Exception:
            pass

    def getAction(self, firstClick, secondClick):
        action = 0
        if firstClick[0] == 0 or firstClick[0] == 1:
            action = firstClick[0]*170+firstClick[1]*17
            if secondClick[0] == 2:
                return action
            elif secondClick[0] == 3:
                return action + 1 + secondClick[1]
            elif secondClick[0] == 4:
                return action + 8
            elif secondClick[0] == 5:
                return action + 9 + secondClick[1]
        elif firstClick[0] == 2:
            action = 187
        else:
            action = 195+8*firstClick[1]

        if secondClick[0] == 4:
            return action
        elif secondClick[0] == 5:
            return action + 1 + secondClick[1]

    def getLegalActionsForCard(self, type, id):
        action = 0
        width = 8
        if type == 0 or type == 1:
            action = type*170+id*17
            width = 17
        elif type == 2:
            action = 187
        else:
            action = 195+8*id
        return [(action <= a < (action + width)) for a in checkValidActionsSparse(self.game)]




    def isNoTargetCard(self, type, id):
        validActions = checkValidActionsSparse(self.game)
        return (type*170+id*17+16) in validActions

    def uncheckAll(self):
        self.firstClick = None
        for i in (self.ui.allyHand.buttons()+self.ui.allyBoard.buttons()+self.ui.enemyBoard.buttons()):
            i.setChecked(False)
        self.ui.enemyHero.setChecked(False)
        self.ui.allyHero.setChecked(False)
        self.ui.heroPower.setChecked(False)
        self.ui.endTurnButton.setChecked(False)


    def applyClick(self, type, id):
        print(f'Type: {type} id: {id}')
        if type == 6:
            current_player = self.game.current_player
            try:
                playTurnSparse(self.game, 251)
                while self.game.current_player != current_player:
                    playTurn(self.game, np.random.rand(252))
            except GameOver:
                QMessageBox.warning(self, 'Game', 'Game Finished!')
            self.uncheckAll()
            return self.refresh()

        if not self.getLegalActionsForCard(type, id):
            self.uncheckAll()
            return
        if not self.firstClick and (type == 4 or type == 5):
            self.uncheckAll()
            return
        if self.firstClick and (type == 0 or type == 1 or type == 2 or type == 3):
            self.uncheckAll()
            return
        if self.isNoTargetCard(type, id):
            self.doMove(type*170+id*17+16)
            self.uncheckAll()
        if self.firstClick:
            self.doMove(self.getAction(self.firstClick, [type, id]))
            self.uncheckAll()
        else:
            self.firstClick = [type, id]
        self.refresh()



if __name__ == "__main__":
    app = QApplication([])
    cards.db.initialize()
    game = _setup_game(None)
    window = MainWindow(game)
    window.show()
    sys.exit(app.exec_())
