# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detailrep.ui'
#
# Created: Wed Apr 15 11:51:33 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DetailReportWindow(object):
    def setupUi(self, DetailReportWindow):
        DetailReportWindow.setObjectName(_fromUtf8("DetailReportWindow"))
        DetailReportWindow.resize(672, 608)
        self.centralwidget = QtGui.QWidget(DetailReportWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 671, 561))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        DetailReportWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(DetailReportWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DetailReportWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(DetailReportWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DetailReportWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionPrint = QtGui.QAction(DetailReportWindow)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.toolBar.addAction(self.actionPrint)

        self.retranslateUi(DetailReportWindow)
        QtCore.QMetaObject.connectSlotsByName(DetailReportWindow)

    def retranslateUi(self, DetailReportWindow):
        DetailReportWindow.setWindowTitle(_translate("DetailReportWindow", "Item Analysis Report", None))
        self.toolBar.setWindowTitle(_translate("DetailReportWindow", "toolBar", None))
        self.actionPrint.setText(_translate("DetailReportWindow", "Print", None))
        self.actionPrint.setToolTip(_translate("DetailReportWindow", "Send this report to printer or generate PDF", None))

