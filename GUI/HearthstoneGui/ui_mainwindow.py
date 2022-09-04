# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QSpacerItem,
    QStatusBar, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(729, 591)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.enemyHero = QToolButton(self.centralwidget)
        self.enemyHero.setObjectName(u"enemyHero")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enemyHero.sizePolicy().hasHeightForWidth())
        self.enemyHero.setSizePolicy(sizePolicy)
        self.enemyHero.setCheckable(True)

        self.horizontalLayout.addWidget(self.enemyHero)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.enemyBoardLayout = QHBoxLayout()
        self.enemyBoardLayout.setObjectName(u"enemyBoardLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.enemyBoardLayout.addItem(self.horizontalSpacer_3)

        self.toolButton_17 = QToolButton(self.centralwidget)
        self.enemyBoard = QButtonGroup(MainWindow)
        self.enemyBoard.setObjectName(u"enemyBoard")
        self.enemyBoard.addButton(self.toolButton_17)
        self.toolButton_17.setObjectName(u"toolButton_17")
        sizePolicy.setHeightForWidth(self.toolButton_17.sizePolicy().hasHeightForWidth())
        self.toolButton_17.setSizePolicy(sizePolicy)
        self.toolButton_17.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_17)

        self.toolButton_16 = QToolButton(self.centralwidget)
        self.enemyBoard.addButton(self.toolButton_16)
        self.toolButton_16.setObjectName(u"toolButton_16")
        sizePolicy.setHeightForWidth(self.toolButton_16.sizePolicy().hasHeightForWidth())
        self.toolButton_16.setSizePolicy(sizePolicy)
        self.toolButton_16.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_16)

        self.toolButton_7 = QToolButton(self.centralwidget)
        self.enemyBoard.addButton(self.toolButton_7)
        self.toolButton_7.setObjectName(u"toolButton_7")
        sizePolicy.setHeightForWidth(self.toolButton_7.sizePolicy().hasHeightForWidth())
        self.toolButton_7.setSizePolicy(sizePolicy)
        self.toolButton_7.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_7)

        self.toolButton_26 = QToolButton(self.centralwidget)
        self.enemyBoard.addButton(self.toolButton_26)
        self.toolButton_26.setObjectName(u"toolButton_26")
        sizePolicy.setHeightForWidth(self.toolButton_26.sizePolicy().hasHeightForWidth())
        self.toolButton_26.setSizePolicy(sizePolicy)
        self.toolButton_26.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_26)

        self.toolButton_18 = QToolButton(self.centralwidget)
        self.enemyBoard.addButton(self.toolButton_18)
        self.toolButton_18.setObjectName(u"toolButton_18")
        sizePolicy.setHeightForWidth(self.toolButton_18.sizePolicy().hasHeightForWidth())
        self.toolButton_18.setSizePolicy(sizePolicy)
        self.toolButton_18.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_18)

        self.toolButton_6 = QToolButton(self.centralwidget)
        self.enemyBoard.addButton(self.toolButton_6)
        self.toolButton_6.setObjectName(u"toolButton_6")
        sizePolicy.setHeightForWidth(self.toolButton_6.sizePolicy().hasHeightForWidth())
        self.toolButton_6.setSizePolicy(sizePolicy)
        self.toolButton_6.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_6)

        self.toolButton_14 = QToolButton(self.centralwidget)
        self.enemyBoard.addButton(self.toolButton_14)
        self.toolButton_14.setObjectName(u"toolButton_14")
        sizePolicy.setHeightForWidth(self.toolButton_14.sizePolicy().hasHeightForWidth())
        self.toolButton_14.setSizePolicy(sizePolicy)
        self.toolButton_14.setCheckable(True)

        self.enemyBoardLayout.addWidget(self.toolButton_14)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.enemyBoardLayout.addItem(self.verticalSpacer_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.enemyBoardLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.enemyBoardLayout)

        self.allyBoardLayout = QHBoxLayout()
        self.allyBoardLayout.setObjectName(u"allyBoardLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.allyBoardLayout.addItem(self.horizontalSpacer_5)

        self.toolButton_20 = QToolButton(self.centralwidget)
        self.allyBoard = QButtonGroup(MainWindow)
        self.allyBoard.setObjectName(u"allyBoard")
        self.allyBoard.addButton(self.toolButton_20)
        self.toolButton_20.setObjectName(u"toolButton_20")
        sizePolicy.setHeightForWidth(self.toolButton_20.sizePolicy().hasHeightForWidth())
        self.toolButton_20.setSizePolicy(sizePolicy)
        self.toolButton_20.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_20)

        self.toolButton_21 = QToolButton(self.centralwidget)
        self.allyBoard.addButton(self.toolButton_21)
        self.toolButton_21.setObjectName(u"toolButton_21")
        sizePolicy.setHeightForWidth(self.toolButton_21.sizePolicy().hasHeightForWidth())
        self.toolButton_21.setSizePolicy(sizePolicy)
        self.toolButton_21.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_21)

        self.toolButton_22 = QToolButton(self.centralwidget)
        self.allyBoard.addButton(self.toolButton_22)
        self.toolButton_22.setObjectName(u"toolButton_22")
        sizePolicy.setHeightForWidth(self.toolButton_22.sizePolicy().hasHeightForWidth())
        self.toolButton_22.setSizePolicy(sizePolicy)
        self.toolButton_22.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_22)

        self.toolButton_15 = QToolButton(self.centralwidget)
        self.allyBoard.addButton(self.toolButton_15)
        self.toolButton_15.setObjectName(u"toolButton_15")
        sizePolicy.setHeightForWidth(self.toolButton_15.sizePolicy().hasHeightForWidth())
        self.toolButton_15.setSizePolicy(sizePolicy)
        self.toolButton_15.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_15)

        self.toolButton_13 = QToolButton(self.centralwidget)
        self.allyBoard.addButton(self.toolButton_13)
        self.toolButton_13.setObjectName(u"toolButton_13")
        sizePolicy.setHeightForWidth(self.toolButton_13.sizePolicy().hasHeightForWidth())
        self.toolButton_13.setSizePolicy(sizePolicy)
        self.toolButton_13.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_13)

        self.toolButton_23 = QToolButton(self.centralwidget)
        self.allyBoard.addButton(self.toolButton_23)
        self.toolButton_23.setObjectName(u"toolButton_23")
        sizePolicy.setHeightForWidth(self.toolButton_23.sizePolicy().hasHeightForWidth())
        self.toolButton_23.setSizePolicy(sizePolicy)
        self.toolButton_23.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_23)

        self.toolButton_19 = QToolButton(self.centralwidget)
        self.allyBoard.addButton(self.toolButton_19)
        self.toolButton_19.setObjectName(u"toolButton_19")
        sizePolicy.setHeightForWidth(self.toolButton_19.sizePolicy().hasHeightForWidth())
        self.toolButton_19.setSizePolicy(sizePolicy)
        self.toolButton_19.setCheckable(True)

        self.allyBoardLayout.addWidget(self.toolButton_19)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.allyBoardLayout.addItem(self.verticalSpacer_2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.allyBoardLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.allyBoardLayout)

        self.allyHandLayout = QHBoxLayout()
        self.allyHandLayout.setObjectName(u"allyHandLayout")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.allyHandLayout.addItem(self.horizontalSpacer_7)

        self.toolButton_4 = QToolButton(self.centralwidget)
        self.allyHand = QButtonGroup(MainWindow)
        self.allyHand.setObjectName(u"allyHand")
        self.allyHand.addButton(self.toolButton_4)
        self.toolButton_4.setObjectName(u"toolButton_4")
        sizePolicy.setHeightForWidth(self.toolButton_4.sizePolicy().hasHeightForWidth())
        self.toolButton_4.setSizePolicy(sizePolicy)
        self.toolButton_4.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_4)

        self.toolButton_5 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_5)
        self.toolButton_5.setObjectName(u"toolButton_5")
        sizePolicy.setHeightForWidth(self.toolButton_5.sizePolicy().hasHeightForWidth())
        self.toolButton_5.setSizePolicy(sizePolicy)
        self.toolButton_5.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_5)

        self.toolButton_10 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_10)
        self.toolButton_10.setObjectName(u"toolButton_10")
        sizePolicy.setHeightForWidth(self.toolButton_10.sizePolicy().hasHeightForWidth())
        self.toolButton_10.setSizePolicy(sizePolicy)
        self.toolButton_10.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_10)

        self.toolButton_11 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_11)
        self.toolButton_11.setObjectName(u"toolButton_11")
        sizePolicy.setHeightForWidth(self.toolButton_11.sizePolicy().hasHeightForWidth())
        self.toolButton_11.setSizePolicy(sizePolicy)
        self.toolButton_11.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_11)

        self.toolButton_12 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_12)
        self.toolButton_12.setObjectName(u"toolButton_12")
        sizePolicy.setHeightForWidth(self.toolButton_12.sizePolicy().hasHeightForWidth())
        self.toolButton_12.setSizePolicy(sizePolicy)
        self.toolButton_12.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_12)

        self.toolButton_9 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_9)
        self.toolButton_9.setObjectName(u"toolButton_9")
        sizePolicy.setHeightForWidth(self.toolButton_9.sizePolicy().hasHeightForWidth())
        self.toolButton_9.setSizePolicy(sizePolicy)
        self.toolButton_9.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_9)

        self.toolButton_8 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_8)
        self.toolButton_8.setObjectName(u"toolButton_8")
        sizePolicy.setHeightForWidth(self.toolButton_8.sizePolicy().hasHeightForWidth())
        self.toolButton_8.setSizePolicy(sizePolicy)
        self.toolButton_8.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_8)

        self.toolButton_3 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_3)
        self.toolButton_3.setObjectName(u"toolButton_3")
        sizePolicy.setHeightForWidth(self.toolButton_3.sizePolicy().hasHeightForWidth())
        self.toolButton_3.setSizePolicy(sizePolicy)
        self.toolButton_3.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_3)

        self.toolButton_2 = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton_2)
        self.toolButton_2.setObjectName(u"toolButton_2")
        sizePolicy.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy)
        self.toolButton_2.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton_2)

        self.toolButton = QToolButton(self.centralwidget)
        self.allyHand.addButton(self.toolButton)
        self.toolButton.setObjectName(u"toolButton")
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setCheckable(True)

        self.allyHandLayout.addWidget(self.toolButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.allyHandLayout.addItem(self.verticalSpacer)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.allyHandLayout.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.allyHandLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_9)

        self.allyHero = QToolButton(self.centralwidget)
        self.allyHero.setObjectName(u"allyHero")
        sizePolicy.setHeightForWidth(self.allyHero.sizePolicy().hasHeightForWidth())
        self.allyHero.setSizePolicy(sizePolicy)
        self.allyHero.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.allyHero)

        self.heroPower = QToolButton(self.centralwidget)
        self.heroPower.setObjectName(u"heroPower")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.heroPower.sizePolicy().hasHeightForWidth())
        self.heroPower.setSizePolicy(sizePolicy1)
        self.heroPower.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.heroPower)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 30, -1)
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.horizontalLayout_3.addWidget(self.statusLabel)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_12)

        self.endTurnButton = QToolButton(self.centralwidget)
        self.endTurnButton.setObjectName(u"endTurnButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.endTurnButton.sizePolicy().hasHeightForWidth())
        self.endTurnButton.setSizePolicy(sizePolicy2)
        self.endTurnButton.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.endTurnButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 729, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.enemyHero.setText(QCoreApplication.translate("MainWindow", u"EH", None))
        self.toolButton_17.setText(QCoreApplication.translate("MainWindow", u"E1", None))
        self.toolButton_16.setText(QCoreApplication.translate("MainWindow", u"E2", None))
        self.toolButton_7.setText(QCoreApplication.translate("MainWindow", u"E3", None))
        self.toolButton_26.setText(QCoreApplication.translate("MainWindow", u"E4", None))
        self.toolButton_18.setText(QCoreApplication.translate("MainWindow", u"E5", None))
        self.toolButton_6.setText(QCoreApplication.translate("MainWindow", u"E6", None))
        self.toolButton_14.setText(QCoreApplication.translate("MainWindow", u"E7", None))
        self.toolButton_20.setText(QCoreApplication.translate("MainWindow", u"A1", None))
        self.toolButton_21.setText(QCoreApplication.translate("MainWindow", u"A2", None))
        self.toolButton_22.setText(QCoreApplication.translate("MainWindow", u"A3", None))
        self.toolButton_15.setText(QCoreApplication.translate("MainWindow", u"A4", None))
        self.toolButton_13.setText(QCoreApplication.translate("MainWindow", u"A5", None))
        self.toolButton_23.setText(QCoreApplication.translate("MainWindow", u"A6", None))
        self.toolButton_19.setText(QCoreApplication.translate("MainWindow", u"A7", None))
        self.toolButton_4.setText(QCoreApplication.translate("MainWindow", u"C1", None))
        self.toolButton_5.setText(QCoreApplication.translate("MainWindow", u"C2", None))
        self.toolButton_10.setText(QCoreApplication.translate("MainWindow", u"C3", None))
        self.toolButton_11.setText(QCoreApplication.translate("MainWindow", u"C4", None))
        self.toolButton_12.setText(QCoreApplication.translate("MainWindow", u"C5", None))
        self.toolButton_9.setText(QCoreApplication.translate("MainWindow", u"C6", None))
        self.toolButton_8.setText(QCoreApplication.translate("MainWindow", u"C7", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"C8", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"C9", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"C10", None))
        self.allyHero.setText(QCoreApplication.translate("MainWindow", u"AH", None))
        self.heroPower.setText(QCoreApplication.translate("MainWindow", u"Power", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Data", None))
        self.endTurnButton.setText(QCoreApplication.translate("MainWindow", u"End turn", None))
    # retranslateUi

