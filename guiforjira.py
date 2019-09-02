# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from select import select

import numpy as np
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QDialog, QApplication, QCompleter
from jira import JIRA, JIRAError
from sphinx.addnodes import index

from login import *


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

    # jiraMy: JIRA

    def __init__(self):
        super().__init__()

        self.dfProject = pd.DataFrame()
        self.modelP = pandasModel(self.dfProject)
        self.dfUser = pd.DataFrame()
        self.projects = []
        self.users = []

        self.allpersonal_issues = pd.DataFrame()  # issue DTO d which is Dictionary
        self.isconnected = False
        self.jiraMy: JIRA

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnConnect.clicked.connect(self.connect2jira)
        self.ui.btnGetIssues.clicked.connect(self.getUserIssues)
        self.ui.cbProjects.activated.connect(self.changeditem)
        self.ui.btnImportExcel.clicked.connect(self.import2excel)
        self.show()

    def connect2jira(self):

        # isconnected = True
        completerUsr = QCompleter()

        user_name = self.ui.leUserName.text()
        pass_user = self.ui.lePassword.text()
        options = {'server': 'http://localhost:2990/jira'}
        # options = {'server': 'http://jira.icterra.com:8443'}

        self.ui.btnConnect.setText('Not Connected !')
        # global jiraMy
        try:
            self.jiraMy = JIRA(options, basic_auth=(user_name, pass_user))
            info = self.jiraMy.server_info()
        except JIRAError as je:
            if je.status_code == 401:
                self.ui.lbConnectionStatus.setText("Cannot connect. Check your name and pass {}".format(je.text))
                self.ui.lbConnectionStatus.setBackgroundRole()
                self.ui.btnConnect.setText('Try Again!')
                isconnected = False
        finally:
            self.isconnected = True
            if self.isconnected:
                # global jiraMy
                self.projects = self.jiraMy.projects()

                try:
                    if len(self.projects) > 0:
                        for project in self.projects:
                            d = {
                                'key': project.key,
                                'name': project.name,
                                'id': project.id
                            }
                            self.dfProject = self.dfProject.append(d, ignore_index=True)
                    else:
                        d = {
                            'key': '',
                            'name': '',
                            'id': ''
                        }
                        self.dfProject = self.dfProject.append(d, ignore_index=True)

                    self.modelP = pandasModel(self.dfProject)

                except Exception as e:
                    print(e)

                self.ui.cbProjects.setModel(self.modelP)
                self.ui.cbProjects.setModelColumn(2)

                self.ui.btnConnect.setText('Connected !')

    def changeditem(self):
        # global jiraMy
        if self.isconnected:
            indx = self.ui.cbProjects.currentIndex()
            key = self.dfProject.iloc[indx]['key']

            tmpUserDf = pd.DataFrame()

            issue_query = "project = {}".format(key)
            block_size = 100
            block_num = 0

            while True:
                start_idx = block_num * block_size
                try:
                    issuesUser = self.jiraMy.search_issues(issue_query, start_idx, maxResults=block_size)

                except Exception as je:
                    print(je)
                if len(issuesUser) == 0:
                    break
                block_num += 1
                for issue in issuesUser:
                    d = {
                        'key': issue.key,
                        'assignee': issue.fields.assignee,
                        'creator': issue.fields.creator,
                        'project': issue.fields.project.name,
                        'reporter': issue.fields.reporter
                    }
                    tmpUserDf = tmpUserDf.append(d, ignore_index=True)

                tmpUserDf = tmpUserDf.drop_duplicates(subset='assignee')
                tmpUserModel = pandasModel(tmpUserDf)

            try:
                self.ui.lvUsers.setModel(tmpUserModel)
            except Exception as ex:
                print(ex)
            self.ui.lvUsers.setModelColumn(0)

    def getUserIssues(self):
        global issues

        global model
        try:
            usr = self.ui.lvUsers.selectedIndexes()

            startDate_year, startDate_month, startDate_day = self.ui.deStartDate.calendarWidget().selectedDate().getDate()
            startDate_str = '{0}-{1}-{2}'.format(startDate_year, startDate_month, startDate_day)
            dueDate_year, dueDate_month, dueDate_day = self.ui.deDueDate.calendarWidget().selectedDate().getDate()
            dueDate_str = '{0}-{1}-{2}'.format(dueDate_year, dueDate_month, dueDate_day)

            listIssue = []
            for s in usr:
                itemtext = s.data(Qt.DisplayRole)
                query_issues = "assignee = \'{}\' AND created > {} AND duedate < {} ".format(itemtext, startDate_str,
                                                                                             dueDate_str)

                block_size = 100
                block_num = 0
                issues = self.jiraMy.search_issues(query_issues, startAt=block_num * block_size, maxResults=block_size,
                                                   fields="project, issuetype, created, duedate, resolutiondate, reporter, assignee, status")
                for i in issues:
                    listIssue.append(i)
        except JIRAError as je:
            print(je.status_code, je.text)
        finally:

            if len(issues) > 0:

                for issue in listIssue:
                    d = {
                        'key': issue.key,
                        'assignee': issue.fields.assignee,
                        # 'creator': issue.fields.creator,
                        'project': issue.fields.project.name,
                        'reporter': issue.fields.reporter,
                        'created': issue.fields.created.split('T')[0],
                        'duedate': issue.fields.duedate,
                        'Planned Work': '',
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

                    self.allpersonal_issues = self.allpersonal_issues.append(d, ignore_index=True)

                    for t in range(self.allpersonal_issues.shape[0]):
                        try:
                            self.allpersonal_issues['Planned Work'].iloc[t] = np.busday_count(
                                self.allpersonal_issues.iloc[t, self.allpersonal_issues.columns.get_loc('created')],
                                self.allpersonal_issues.iloc[t, self.allpersonal_issues.columns.get_loc('duedate')]) + 1
                        except Exception as e:
                            print(e)

                model = pandasModel(self.allpersonal_issues)
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
                self.allpersonal_issues = self.allpersonal_issues.append(d, ignore_index=True)
                model = pandasModel(self.allpersonal_issues)
                self.ui.tbvIssuesOfUser.setModel(model)

    def import2excel(self):
        if len(self.allpersonal_issues) > 0:
            export_xl = self.allpersonal_issues.to_excel(r'/home/oelmas/PycharmProjects/PythonandJira/export_df.xlsx',
                                                         index=None, header=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginGui()
    win.show()
    sys.exit(app.exec_())
