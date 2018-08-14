from pyral import Rally, rallyWorkset

def connect_to_rally(commands):
    options = [arg for arg in commands if arg.startswith('--')]
    args = [arg for arg in commands if arg not in options]
    server, user, password, apikey, workspace, project = rallyWorkset(options)
    rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)
    return rally
