from bannerman.banner import db
from bannerman.entities.models import Function, Feature, Capability, Iteration, Story, Task, \
    Defect, Release, Project, State, User, TestCase, TestFolder

mappings = {
    "Id" : "oid",
    "Name" : "Name",
    "Owner" : "Owner",
    "LastUpdateDate" : "LastUpdateDate",
    "PreliminaryEstimate" : "PreliminaryEstimateValue",
    "ActualStartDate" : "ActualStartDate",
    "ActualEndDate" : "ActualEndDate",
    "CreationDate" : "CreationDate",
    "Parent" : "Parent",
    "Child" : "Child",
    "Project" : "Project",
    "PercentDoneByStoryCount" : "PercentDoneByStoryCount",
    "PercentDoneByStoryPlanEstimate" : "PercentDoneByStoryPlanEstimate",
    "Workspace" : "Workspace",
    "Iteration" : "Iteration",
    "Defects" : "Defects",
    "PortfolioItem" : "PortfolioItem",
    "Estimate" : "Estimate",
    "PlanEstimate" : "PlanEstimate",
    "FlowState" : "FlowState",
    "Tasks" : "Tasks",
    "Release" : "Release",
    "AcceptedDate" : "AcceptedDate",
    "ScheduleState" : "ScheduleState",
    "Blocked" : "Blocked",
    "BlockedReason" : "BlockedReason",
    "State" : "State",
    "TimeSpent" : "TimeSpent",
    "ToDo" : "ToDo",
    "StartDate" : "StartDate",
    "EndDate" : "EndDate",
    "Notes" : "Notes",
    "PlannedVelocity" : "PlannedVelocity",
    "Actuals" : "Actuals",
    "ClosedDate" : "ClosedDate",
    "Environment" : "Environment",
    "FlowStateChangedDate" : "FlowStateChangedDate",
    "InProgressDate" : "InProgressDate",
    "Requirement" : "Requirement",
    "SubmittedBy" : "SubmittedBy",
    "Severity" : "Severity",
    "TaskStatus" : "TaskStatus",
    "TaskEstimateTotal" : "TaskEstimateTotal",
    "TaskActualTotal" : "TaskActualTotal",
    "TaskRemainingTotal" : "TaskRemainingTotal",
    "LastDiscussionAgeInMinutes" : "LastDiscussionAgeInMinutes",
    "PointsAccepted" : "Accepted",
    "GrossEstimateConversionRatio" : "GrossEstimateConversionRatio",
    "ReleaseDate" : "ReleaseDate",
    "ReleaseStartDate" : "ReleaseStartDate",
    "AgeThreshold" : "AgeThreshold",
    "ExitPolicy" : "ExitPolicy",
    "OrderIndex" : "OrderIndex",
    "WorkProduct" : "WorkProduct",
    "EmailAddress" : "EmailAddress",
    "DisplayName" : "DisplayName",
    "Role" : "Role",
    "ref" : "ref",
    "KanbanState" : "BAKanbanStates",
    "ParentId" : "ParentId",
    "OwnerId" : "OwnerId",
    "ReleaseId" : "ReleaseId",
    "WorkspaceId" : "WorkspaceId",
    "FlowStateId" : "FlowStateId",
    "FunctionId" : "FunctionId",
    "IterationId" : "IterationId",
    "SubmittedById" : "SubmittedById",
    "StoryId" : "StoryId",
    "ProjectId" : "ProjectId",
    "Priority" : "Priority",
    "Resolution" : "Resolution",
    "DefectState" : "State",
    "StateId" : "StateId",
    "ShortName" : "FormattedID",
    "Method" : "Method",
    "TestFolderId" : "TestFolderId",
    "TestingType" : "Type",
    "StateChangedDate" : "StateChangedDate"
}

def add_to_db(extracted_item):
    if extracted_item.RallyItemType == 'FUNCTION':
        db_item = Function()
    elif extracted_item.RallyItemType == 'FEATURE':
        db_item = Feature()
    elif extracted_item.RallyItemType == 'CAPABILITY':
        db_item = Capability()
    elif extracted_item.RallyItemType == 'ITERATION':
        db_item = Iteration()
    elif extracted_item.RallyItemType == 'TASK':
        db_item = Task()
    elif extracted_item.RallyItemType == 'STORY':
        db_item = Story()
    elif extracted_item.RallyItemType == 'DEFECT':
        db_item = Defect()
    elif extracted_item.RallyItemType == 'RELEASE':
        db_item = Release()
    elif extracted_item.RallyItemType == 'PROJECT':
        db_item = Project()
    elif extracted_item.RallyItemType == 'STATE':
        db_item = State()
    elif extracted_item.RallyItemType == 'USER':
        db_item = User()
    elif extracted_item.RallyItemType == 'TESTCASE':
        db_item = TestCase()
    elif extracted_item.RallyItemType == 'TESTFOLDER':
        db_item = TestFolder()
    elif extracted_item.RallyItemType == 'HIERARCHICALREQUIREMENT':
        db_item = Story()
    item_attrs = [i for i in dir(db_item) if not i.islower()]
    for attr in item_attrs:
        try:
            setattr(db_item, attr, getattr(extracted_item, mappings[attr]))
        except AttributeError:
            setattr(db_item, attr, None)
    db.session.add(db_item)
    return
