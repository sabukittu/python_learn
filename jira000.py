from jira import JIRA



jira_connect = JIRA(server='', basic_auth=('', ''))
project = jira_connect.project('')
jira_connect.create_issue(project='', summary=b, description=a, issuetype={'name': 'Task'})

