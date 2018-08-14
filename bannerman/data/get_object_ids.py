import re

def get_object_ids(rally_item):
    if rally_item.RallyItemType == 'USER':
        try:
            ref_match = re.match("([a-zA-Z]+)/(.*)", rally_item.ref)
            setattr(rally_item, 'Id', ref_match.group(2))
        except AttributeError:
            print(ref_match.group(2))
        except:
            raise ValueError("Regular expression did not match a User Id")
    try:
        rally_item.ParentId = rally_item.Parent.oid
    except AttributeError:
        pass
    try:
        rally_item.OwnerId =  rally_item.Owner.oid
    except AttributeError:
        pass
    try:
        rally_item.ProjectId = rally_item.Project.oid
    except AttributeError:
        pass
    try:
        rally_item.ReleaseId = rally_item.Release.oid
    except AttributeError:
        pass
    try:
        rally_item.WorkspaceId = rally_item.Workspace.oid
    except AttributeError:
        pass
    try:
        rally_item.FlowStateId = rally_item.FlowState.oid
    except AttributeError:
        pass
    try:
        rally_item.FunctionId = rally_item.PortfolioItem.oid
    except AttributeError:
        pass
    try:
        rally_item.IterationId = rally_item.Iteration.oid
    except AttributeError:
        pass
    try:
        rally_item.SubmittedById = rally_item.SubmittedBy.oid
    except AttributeError:
        pass
    try:
        rally_item.TestFolderId = rally_item.TestFolder.oid
    except AttributeError:
        pass
    try:
        rally_item.StateId = rally_item.State.oid
    except AttributeError:
        pass
    try:
        rally_item.StoryId = rally_item.Requirement.oid
    except AttributeError:
        try:
            rally_item.StoryId = rally_item.WorkProduct.oid
        except AttributeError:
            pass
    return
