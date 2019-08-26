# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QDialog, QApplication
from login import *
from jira import JIRA, JIRAError
from time import strftime


def calculate_works(datetime1, datetime2):
    arg1 = datetime1.strptime(datetime1,'%Y-%m-%dT%H:%M:%S.%f%z')
    arg2 = datetime1.strptime(datetime2,'%Y-%m-%dT%H:%M:%S.%f%z')
    result = arg2 - arg1


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
                self.ui.lbConnectionStatus.setText("Cannot connect. Check your name and pass {}".format(je.text))
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

            startDate_year, startDate_month, startDate_day = self.ui.calStartDate.selectedDate().getDate()
            startDate_str = '{0}-{1}-{2}'.format(startDate_year, startDate_month, startDate_day)
            dueDate_year, dueDate_month, dueDate_day = self.ui.calDueDate.selectedDate().getDate()
            dueDate_str = '{0}-{1}-{2}'.format(dueDate_year, dueDate_month, dueDate_day)

            query_issues = "assignee = {} AND created > {} AND duedate < {} ".format(usr, startDate_str, dueDate_str)

            block_size = 100
            block_num = 0
            issues = jiraMy.search_issues(query_issues, startAt=block_num * block_size, maxResults=block_size,fields="issuetype, created, duedate, resolutiondate, reporter, assignee, status")
        except JIRAError as je:
            print(je.status_code, je.text)
        finally:
            if len(issues) > 0:

                print([calculate_works(issue.fields.created, issue.fields.duedate) for issue in issues])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginGui()
    win.show()
    sys.exit(app.exec_())
