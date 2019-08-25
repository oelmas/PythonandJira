# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from login import *
from jira import JIRA, JIRAError


class LoginGui(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnConnect.clicked.connect(self.connect2jira)
        self.show()

    def connect2jira(self):
        global jira
        isConnected = True
        user_name = self.ui.leUserName.text()
        pass_user = self.ui.lePassword.text()
        options = {'server': 'http://localhost:2990/jira'}
        self.ui.btnConnect.setText('Not Connected !')
        try:
            jira = JIRA(options, basic_auth=(user_name, pass_user))
        except JIRAError as je:
            if je.status_code == 401:
                self.ui.lbConnectionStatus.setText("Cannot connect. Check ur name and pass")
                self.ui.btnConnect.setText('Try Again!')
                isConnected = False
        finally:

            if isConnected:
                self.ui.btnConnect.setText('Connected !')
                projects = jira.projects()

                self.ui.lvProjects.addItems([projects.name for projects in projects])

                users = jira.search_users('.')
                self.ui.lvUsers.addItems([user.name for user in users])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginGui()
    win.show()
    sys.exit(app.exec_())
