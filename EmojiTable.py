# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/emojitable.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(337, 194)
        self.emojitable = QtWidgets.QTableWidget(Form)
        self.emojitable.setGeometry(QtCore.QRect(0, 0, 336, 192))
        self.emojitable.setMinimumSize(QtCore.QSize(256, 0))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.emojitable.setFont(font)
        self.emojitable.setRowCount(50)
        self.emojitable.setColumnCount(8)
        self.emojitable.setObjectName("emojitable")
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(0, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(1, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(2, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(3, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(4, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(5, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(6, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(7, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(8, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.emojitable.setItem(9, 7, item)
        self.emojitable.horizontalHeader().setVisible(False)
        self.emojitable.horizontalHeader().setCascadingSectionResizes(False)
        self.emojitable.horizontalHeader().setDefaultSectionSize(40)
        self.emojitable.horizontalHeader().setHighlightSections(False)
        self.emojitable.horizontalHeader().setMinimumSectionSize(20)
        self.emojitable.verticalHeader().setVisible(False)
        self.emojitable.verticalHeader().setDefaultSectionSize(40)
        self.emojitable.verticalHeader().setHighlightSections(False)
        self.emojitable.verticalHeader().setMinimumSectionSize(40)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.emojitable.verticalHeaderItem(0)
        item.setText(_translate("Form", "New Row"))
        item = self.emojitable.verticalHeaderItem(1)
        item.setText(_translate("Form", "New Row"))
        item = self.emojitable.verticalHeaderItem(2)
        item.setText(_translate("Form", "New Row"))
        item = self.emojitable.verticalHeaderItem(3)
        item.setText(_translate("Form", "New Row"))
        item = self.emojitable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "New Column"))
        item = self.emojitable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "New Column"))
        item = self.emojitable.horizontalHeaderItem(2)
        item.setText(_translate("Form", "New Column"))
        item = self.emojitable.horizontalHeaderItem(3)
        item.setText(_translate("Form", "New Column"))
        __sortingEnabled = self.emojitable.isSortingEnabled()
        self.emojitable.setSortingEnabled(False)
        item = self.emojitable.item(0, 0)
        item.setText(_translate("Form", "😄"))
        item = self.emojitable.item(0, 1)
        item.setText(_translate("Form", "😆"))
        item = self.emojitable.item(0, 2)
        item.setText(_translate("Form", "😊"))
        item = self.emojitable.item(0, 3)
        item.setText(_translate("Form", "😃"))
        item = self.emojitable.item(0, 4)
        item.setText(_translate("Form", "😏"))
        item = self.emojitable.item(0, 5)
        item.setText(_translate("Form", "😍"))
        item = self.emojitable.item(0, 6)
        item.setText(_translate("Form", "😘"))
        item = self.emojitable.item(0, 7)
        item.setText(_translate("Form", "😚"))
        item = self.emojitable.item(1, 0)
        item.setText(_translate("Form", "😳"))
        item = self.emojitable.item(1, 1)
        item.setText(_translate("Form", "😌"))
        item = self.emojitable.item(1, 2)
        item.setText(_translate("Form", "😆"))
        item = self.emojitable.item(1, 3)
        item.setText(_translate("Form", "😁"))
        item = self.emojitable.item(1, 4)
        item.setText(_translate("Form", "😉"))
        item = self.emojitable.item(1, 5)
        item.setText(_translate("Form", "😜"))
        item = self.emojitable.item(1, 6)
        item.setText(_translate("Form", "😝"))
        item = self.emojitable.item(1, 7)
        item.setText(_translate("Form", "😀"))
        item = self.emojitable.item(2, 0)
        item.setText(_translate("Form", "😗"))
        item = self.emojitable.item(2, 1)
        item.setText(_translate("Form", "😙"))
        item = self.emojitable.item(2, 2)
        item.setText(_translate("Form", "😛"))
        item = self.emojitable.item(2, 3)
        item.setText(_translate("Form", "😴"))
        item = self.emojitable.item(2, 4)
        item.setText(_translate("Form", "😟"))
        item = self.emojitable.item(2, 5)
        item.setText(_translate("Form", "😦"))
        item = self.emojitable.item(2, 6)
        item.setText(_translate("Form", "😧"))
        item = self.emojitable.item(2, 7)
        item.setText(_translate("Form", "😮"))
        item = self.emojitable.item(3, 0)
        item.setText(_translate("Form", "😬"))
        item = self.emojitable.item(3, 1)
        item.setText(_translate("Form", "😕"))
        item = self.emojitable.item(3, 2)
        item.setText(_translate("Form", "😯"))
        item = self.emojitable.item(3, 3)
        item.setText(_translate("Form", "😑"))
        item = self.emojitable.item(3, 4)
        item.setText(_translate("Form", "😒"))
        item = self.emojitable.item(3, 5)
        item.setText(_translate("Form", "😅"))
        item = self.emojitable.item(3, 6)
        item.setText(_translate("Form", "😓"))
        item = self.emojitable.item(3, 7)
        item.setText(_translate("Form", "😥"))
        item = self.emojitable.item(4, 0)
        item.setText(_translate("Form", "😩"))
        item = self.emojitable.item(4, 1)
        item.setText(_translate("Form", "😔"))
        item = self.emojitable.item(4, 2)
        item.setText(_translate("Form", "😞"))
        item = self.emojitable.item(4, 3)
        item.setText(_translate("Form", "😖"))
        item = self.emojitable.item(4, 4)
        item.setText(_translate("Form", "😨"))
        item = self.emojitable.item(4, 5)
        item.setText(_translate("Form", "😰"))
        item = self.emojitable.item(4, 6)
        item.setText(_translate("Form", "😣"))
        item = self.emojitable.item(4, 7)
        item.setText(_translate("Form", "😢"))
        item = self.emojitable.item(5, 0)
        item.setText(_translate("Form", "😭"))
        item = self.emojitable.item(5, 1)
        item.setText(_translate("Form", "😂"))
        item = self.emojitable.item(5, 2)
        item.setText(_translate("Form", "😲"))
        item = self.emojitable.item(5, 3)
        item.setText(_translate("Form", "😱"))
        item = self.emojitable.item(5, 4)
        item.setText(_translate("Form", "😫"))
        item = self.emojitable.item(5, 5)
        item.setText(_translate("Form", "😠"))
        item = self.emojitable.item(5, 6)
        item.setText(_translate("Form", "😡"))
        item = self.emojitable.item(5, 7)
        item.setText(_translate("Form", "😤"))
        item = self.emojitable.item(6, 0)
        item.setText(_translate("Form", "😪"))
        item = self.emojitable.item(6, 1)
        item.setText(_translate("Form", "😋"))
        item = self.emojitable.item(6, 2)
        item.setText(_translate("Form", "😷"))
        item = self.emojitable.item(6, 3)
        item.setText(_translate("Form", "😎"))
        item = self.emojitable.item(6, 4)
        item.setText(_translate("Form", "😵"))
        item = self.emojitable.item(6, 5)
        item.setText(_translate("Form", "👿"))
        item = self.emojitable.item(6, 6)
        item.setText(_translate("Form", "😈"))
        item = self.emojitable.item(6, 7)
        item.setText(_translate("Form", "😐"))
        item = self.emojitable.item(7, 0)
        item.setText(_translate("Form", "😶"))
        item = self.emojitable.item(7, 1)
        item.setText(_translate("Form", "😇"))
        item = self.emojitable.item(7, 2)
        item.setText(_translate("Form", "👽"))
        item = self.emojitable.item(7, 3)
        item.setText(_translate("Form", "💛"))
        item = self.emojitable.item(7, 4)
        item.setText(_translate("Form", "💙"))
        item = self.emojitable.item(7, 5)
        item.setText(_translate("Form", "💜"))
        item = self.emojitable.item(7, 6)
        item.setText(_translate("Form", "💚"))
        item = self.emojitable.item(7, 7)
        item.setText(_translate("Form", "💔"))
        item = self.emojitable.item(8, 0)
        item.setText(_translate("Form", "💆"))
        item = self.emojitable.item(8, 1)
        item.setText(_translate("Form", "💇"))
        item = self.emojitable.item(8, 2)
        item.setText(_translate("Form", "💅"))
        item = self.emojitable.item(8, 3)
        item.setText(_translate("Form", "👦"))
        item = self.emojitable.item(8, 4)
        item.setText(_translate("Form", "👧"))
        item = self.emojitable.item(8, 5)
        item.setText(_translate("Form", "👩"))
        item = self.emojitable.item(8, 6)
        item.setText(_translate("Form", "👨"))
        item = self.emojitable.item(8, 7)
        item.setText(_translate("Form", "👶"))
        item = self.emojitable.item(9, 0)
        item.setText(_translate("Form", "👵"))
        item = self.emojitable.item(9, 1)
        item.setText(_translate("Form", "👴"))
        item = self.emojitable.item(9, 2)
        item.setText(_translate("Form", "👱"))
        item = self.emojitable.item(9, 3)
        item.setText(_translate("Form", "👲"))
        item = self.emojitable.item(9, 4)
        item.setText(_translate("Form", "👳"))
        item = self.emojitable.item(9, 5)
        item.setText(_translate("Form", "👷"))
        item = self.emojitable.item(9, 6)
        item.setText(_translate("Form", "👮"))
        item = self.emojitable.item(9, 7)
        item.setText(_translate("Form", "👼"))
        self.emojitable.setSortingEnabled(__sortingEnabled)
