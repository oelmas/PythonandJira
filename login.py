# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(888, 566)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbUserName = QtWidgets.QLabel(Dialog)
        self.lbUserName.setObjectName("lbUserName")
        self.horizontalLayout.addWidget(self.lbUserName)
        self.leUserName = QtWidgets.QLineEdit(Dialog)
        self.leUserName.setObjectName("leUserName")
        self.horizontalLayout.addWidget(self.leUserName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbPassword = QtWidgets.QLabel(Dialog)
        self.lbPassword.setObjectName("lbPassword")
        self.horizontalLayout_2.addWidget(self.lbPassword)
        self.lePassword = QtWidgets.QLineEdit(Dialog)
        self.lePassword.setObjectName("lePassword")
        self.horizontalLayout_2.addWidget(self.lePassword)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.lbConnectionStatus = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbConnectionStatus.sizePolicy().hasHeightForWidth())
        self.lbConnectionStatus.setSizePolicy(sizePolicy)
        self.lbConnectionStatus.setText("")
        self.lbConnectionStatus.setObjectName("lbConnectionStatus")
        self.horizontalLayout_3.addWidget(self.lbConnectionStatus)
        self.btnConnect = QtWidgets.QPushButton(Dialog)
        self.btnConnect.setObjectName("btnConnect")
        self.horizontalLayout_3.addWidget(self.btnConnect)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lvProjects = QtWidgets.QListWidget(Dialog)
        self.lvProjects.setObjectName("lvProjects")
        self.verticalLayout_2.addWidget(self.lvProjects)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.lvUsers = QtWidgets.QListWidget(Dialog)
        self.lvUsers.setObjectName("lvUsers")
        self.verticalLayout_3.addWidget(self.lvUsers)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tbvIssuesOfUser = QtWidgets.QTableView(Dialog)
        self.tbvIssuesOfUser.setObjectName("tbvIssuesOfUser")
        self.horizontalLayout_6.addWidget(self.tbvIssuesOfUser)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.deStartDate = QtWidgets.QDateEdit(Dialog)
        self.deStartDate.setCalendarPopup(True)
        self.deStartDate.setDate(QtCore.QDate(2019, 1, 1))
        self.deStartDate.setObjectName("deStartDate")
        self.horizontalLayout_5.addWidget(self.deStartDate)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.deDueDate = QtWidgets.QDateEdit(Dialog)
        self.deDueDate.setCalendarPopup(True)
        self.deDueDate.setDate(QtCore.QDate(2019, 1, 1))
        self.deDueDate.setObjectName("deDueDate")
        self.horizontalLayout_7.addWidget(self.deDueDate)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)
        self.btnGetIssues = QtWidgets.QPushButton(Dialog)
        self.btnGetIssues.setObjectName("btnGetIssues")
        self.verticalLayout_7.addWidget(self.btnGetIssues)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(self.leUserName.clear)
        self.pushButton.clicked.connect(self.lePassword.clear)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbUserName.setText(_translate("Dialog", "User Name:"))
        self.lbPassword.setText(_translate("Dialog", "User Password :"))
        self.btnConnect.setText(_translate("Dialog", "Connect"))
        self.pushButton.setText(_translate("Dialog", "Clear"))
        self.label.setText(_translate("Dialog", "Projects"))
        self.label_2.setText(_translate("Dialog", "Users"))
        self.label_3.setText(_translate("Dialog", "Start  Date:"))
        self.label_4.setText(_translate("Dialog", "Due Date : "))
        self.btnGetIssues.setText(_translate("Dialog", "Get User Issues"))
