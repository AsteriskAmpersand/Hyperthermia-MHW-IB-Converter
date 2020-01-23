# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\IBProjects\ArmorPorts\LabComparison\IBConverter\3OptionDialogue.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(377, 98)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = QtWidgets.QLabel(Dialog)
        self.text.setMinimumSize(QtCore.QSize(160, 30))
        self.text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text.setWordWrap(True)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hollowPressed = QtWidgets.QPushButton(Dialog)
        self.hollowPressed.setObjectName("hollowPressed")
        self.horizontalLayout.addWidget(self.hollowPressed)
        self.hairPressed = QtWidgets.QPushButton(Dialog)
        self.hairPressed.setObjectName("hairPressed")
        self.horizontalLayout.addWidget(self.hairPressed)
        self.matchPressed = QtWidgets.QPushButton(Dialog)
        self.matchPressed.setObjectName("matchPressed")
        self.horizontalLayout.addWidget(self.matchPressed)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.text.setText(_translate("Dialog", "TextLabel"))
        self.hollowPressed.setText(_translate("Dialog", "No Player Head"))
        self.hairPressed.setText(_translate("Dialog", "Unmodified Player Head"))
        self.matchPressed.setText(_translate("Dialog", "Search for Match"))

