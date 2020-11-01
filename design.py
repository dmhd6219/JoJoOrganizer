# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(536, 324)
        mainWindow.setMinimumSize(QtCore.QSize(536, 324))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("jojo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        mainWindow.setStyleSheet("QWidget{\n"
"    background-color:rgb(34, 34, 34);\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: rgb(83, 83, 83);\n"
"    border-radius: 6.5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color:rgb(52, 52, 52)\n"
"}\n"
"\n"
"QTableWidget\n"
"{\n"
"background-color:rgb(255, 242, 189);\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QTableWidget QTableCornerButton::section\n"
"{\n"
"background-color:rgb(255, 242, 189);\n"
"border: 1px outset red;\n"
"}\n"
"\n"
"QHeaderView\n"
"{\n"
"background-color:  rgb(83, 83, 83);\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"background-color:  rgb(83, 83, 83);\n"
"color:rgb(255, 242, 189);\n"
"border:1px outset rgb(181, 172, 37);\n"
"border-radius: 3px;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addEvent = QtWidgets.QPushButton(self.centralwidget)
        self.addEvent.setMinimumSize(QtCore.QSize(191, 41))
        self.addEvent.setObjectName("addEvent")
        self.verticalLayout.addWidget(self.addEvent)
        self.deleteEvent = QtWidgets.QPushButton(self.centralwidget)
        self.deleteEvent.setMinimumSize(QtCore.QSize(191, 41))
        self.deleteEvent.setObjectName("deleteEvent")
        self.verticalLayout.addWidget(self.deleteEvent)
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setMinimumSize(QtCore.QSize(191, 41))
        self.settingsButton.setObjectName("settingsButton")
        self.verticalLayout.addWidget(self.settingsButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 536, 21))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "JoJo\'s Orginizer😎"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "Event"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "Date"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "Time"))
        self.addEvent.setText(_translate("mainWindow", "Добавить новое событие"))
        self.deleteEvent.setText(_translate("mainWindow", "Удалить выбранное событие"))
        self.settingsButton.setText(_translate("mainWindow", "Settings/Настройки"))
