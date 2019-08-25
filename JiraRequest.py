from jira import JIRA, JIRAError

import re

options = {'server': 'http://localhost:2990/jira'}
user_name = 'admin'
user_pass = 'admin'


#try:
jiraMy = JIRA(options, basic_auth=(user_name, user_pass))
#except JIRAError as je:
 #   if '401' in str(je):
  #      print("Not connected {0}".format(je.response.statuse_code))

# jira = JIRA(options, basic_auth=(user_name, user_pass))
projects = jiraMy.projects()
print(projects)
print([project.name for project in projects])

# issue_list = [
# {
#     'project': {'id': '10000'},
#     'summary': 'First issue of many',
#     'description': 'Look into this one',
#     'issuetype': {'name': ' Task'},
# },
# {
#     'project': {'id': '10000'},
#     'summary': 'Second issue',
#     'description': 'Another one',
#     'issuetype': {'name': ' Task'},
# },
# {
#     'project': {'id': '10000'},
#     'summary': 'Last issue',
#     'description': 'Final issue of batch.',
#     'issuetype': {'name': ' Task'},
# }]
#
# issues = jira.create_issues(field_list=issue_list)
# new_issue = jira.create_issue(project='PPP', summary='New issue from jira-python',
#                               description='Look into this one', issuetype={'name': 'Task'})
issues_in_proj = jiraMy.search_issues('project=TPP')
print(issues_in_proj)
print([iss.key for iss in issues_in_proj])

users = jiraMy.search_users('.')
print([user.name for user in users])


