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
        self.ui.btnGetIssues.clicked.connect(self.getUserIssues)
        self.show()

    def connect2jira(self):
        global jiraMy
        isconnected = True
        user_name = self.ui.leUserName.text()
        pass_user = self.ui.lePassword.text()
        options = {'server': 'http://localhost:2990/jira'}
        self.ui.btnConnect.setText('Not Connected !')
        try:
            jiraMy = JIRA(options, basic_auth=(user_name, pass_user))
        except JIRAError as je:
            if je.status_code == 401:
                self.ui.lbConnectionStatus.setText("Cannot connect. Check ur name and pass {}".format(je.text))
                self.ui.btnConnect.setText('Try Again!')
                isconnected = False
        finally:

            if isconnected:
                projects = jiraMy.projects()
                self.ui.btnConnect.setText('Connected !')
                self.ui.lvProjects.addItems([projects.name for projects in projects])

                users = jiraMy.search_users('.')
                self.ui.lvUsers.addItems([user.name for user in users])

    def getUserIssues(self):
        global issues
        try:
            prj = self.ui.lvProjects.currentItem().text()
            print([prj])
            usr = self.ui.lvUsers.currentItem().text()
            print([usr])
            query_issues = "assignee = {}".format(usr)

            block_size = 100
            block_num = 0
            issues = jiraMy.search_issues(query_issues,startAt = block_num * block_size, maxResults = block_size,fields = "issuetype, created, resolutiondate, reporter, assignee, status")
        except JIRAError as je:
            print(je.status_code, je.text)
        finally:
            if len(issues) > 0:
                print([issue.fields.created for issue in issues])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginGui()
    win.show()
    sys.exit(app.exec_())
