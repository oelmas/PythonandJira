# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QDialog, QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from login import *
from jira import JIRA, JIRAError
from datetime import datetime
import pandas as pd
import numpy as np


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


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

    def calculate_works(self, datetime1, datetime2):
        arg1 = datetime.strptime(datetime1, '%Y-%m-%dT%H:%M:%S.%f%z')
        arg2 = datetime.strptime(datetime2, '%Y-%m-%dT%H:%M:%S.%f%z')
        result = arg2 - arg1
        return result.days, result.mins, result.seconds

    def getUserIssues(self):
        global issues
        allpersonal_issues = pd.DataFrame()
        global model
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
            issues = jiraMy.search_issues(query_issues, startAt=block_num * block_size, maxResults=block_size,
                                          fields="project, issuetype, created, duedate, resolutiondate, reporter, assignee, status")
        except JIRAError as je:
            print(je.status_code, je.text)
        finally:

            if len(issues) > 0:

                for issue in issues:
                    d = {
                        'key': issue.key,
                        'assignee': issue.fields.assignee,
                        # 'creator': issue.fields.creator,
                        'project': issue.fields.project.name,
                        'reporter': issue.fields.reporter,
                        'created': issue.fields.created.split('T')[0],
                        'duedate': issue.fields.duedate,
                        # 'components': issue.fields.components,
                        # 'description': issue.fields.description,
                        # 'summary': issue.fields.summary,
                        # 'fixVersions': issue.fields.fixVersions,
                        'subtask': issue.fields.issuetype.subtask,
                        'issuetype': issue.fields.issuetype.name,
                        # 'priority': issue.fields.priority.name,
                        # 'resolution': issue.fields.resolution,
                        'resolution.date': issue.fields.resolutiondate,
                        'status.name': issue.fields.status.name,
                        'status.description': issue.fields.status.description,
                        # 'updated': issue.fields.updated,
                        # 'versions': issue.fields.versions,
                        # 'watches': issue.fields.watches.watchCount,
                        # 'storypoints': issue.fields.customfield_10142
                    }

                    allpersonal_issues = allpersonal_issues.append(d, ignore_index=True)

                    allpersonal_issues['Planned Work'] = pd.to_datetime(allpersonal_issues['duedate']) - pd.to_datetime(
                        allpersonal_issues['created'])
                    allpersonal_issues['Planned Work'] = allpersonal_issues['Planned Work'] / np.timedelta64(1, 'D')

                model = pandasModel(allpersonal_issues)
                self.ui.tbvIssuesOfUser.setModel(model)
            else:
                d = {
                    'key': '',
                    'assignee': '',
                    # 'creator': issue.fields.creator,
                    'project': '',
                    'reporter': '',
                    'created': '',
                    'duedate': '',
                    # 'components': issue.fields.components,
                    # 'description': issue.fields.description,
                    # 'summary': issue.fields.summary,
                    # 'fixVersions': issue.fields.fixVersions,
                    'subtask': '',
                    'issuetype': '',
                    # 'priority': issue.fields.priority.name,
                    # 'resolution': issue.fields.resolution,
                    'resolution.date': '',
                    'status.name': '',
                    'status.description': '',
                    # 'updated': issue.fields.updated,
                    # 'versions': issue.fields.versions,
                    # 'watches': issue.fields.watches.watchCount,
                    # 'storypoints': issue.fields.customfield_10142
                }
                allpersonal_issues = allpersonal_issues.append(d, ignore_index=True)
                model = pandasModel(allpersonal_issues)
                self.ui.tbvIssuesOfUser.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginGui()
    win.show()
    sys.exit(app.exec_())
