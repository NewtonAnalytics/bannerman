from bannerman.banner import db

class User(db.Model):
    __tablename__ = 'Workspace.Users'
    Id = db.Column(db.String(24), primary_key=True)
    DisplayName = db.Column(db.String(40))
    Role = db.Column(db.String(24))
    EmailAddress = db.Column(db.String(50))
    tasks = db.relationship('Task', backref='owner', lazy='dynamic')
    projects = db.relationship('Project', backref='owner', lazy='dynamic')
    capabilities = db.relationship('Capability', backref='owner', lazy='dynamic')
    features = db.relationship('Feature', backref='owner', lazy='dynamic')
    functions = db.relationship('Function', backref='owner', lazy='dynamic')
    test_cases = db.relationship('TestCase', backref='owner', lazy='dynamic')
    stories = db.relationship('Story', backref='owner', lazy='dynamic')

    def __repr__(self):
        return "<User: {}, {} - {}".format(self.DisplayName, self.Role, self.EmailAddress)

class Function(db.Model):
    __tablename__ = 'Projects.Functions'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    LastUpdateDate = db.Column(db.String, index=True)
    PreliminaryEstimate = db.Column(db.String(24))
    ActualStartDate = db.Column(db.String)
    ActualEndDate = db.Column(db.String)
    CreationDate = db.Column(db.String)
    ParentId = db.Column(db.String(24), db.ForeignKey('Projects.Features.Id'))
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    StateId = db.Column(db.String(24), db.ForeignKey('Projects.States.Id'))
    StateChangedDate = db.Column(db.String(50))
    PercentDoneByStoryCount =  db.Column(db.Float)
    PercentDoneByStoryPlanEstimate = db.Column(db.Float)
    ReleaseId = db.Column(db.String(24), db.ForeignKey('Projects.Releases.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    stories = db.relationship('Story', backref='function', lazy='dynamic')

    def __repr__(self):
        return "<Function - {}>".format(self.Name)

class Feature(db.Model):
    __tablename__ = 'Projects.Features'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    LastUpdateDate = db.Column(db.String, index=True)
    PreliminaryEstimate = db.Column(db.String(24))
    ActualStartDate = db.Column(db.String)
    ActualEndDate = db.Column(db.String)
    CreationDate = db.Column(db.String)
    ParentId = db.Column(db.String(24), db.ForeignKey('Projects.Capabilities.Id'))
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    StateId = db.Column(db.String(24), db.ForeignKey('Projects.States.Id'))
    StateChangedDate = db.Column(db.String(50))
    PercentDoneByStoryCount = db.Column(db.Float)
    PercentDoneByStoryPlanEstimate = db.Column(db.Float)
    ReleaseId = db.Column(db.String(24), db.ForeignKey('Projects.Releases.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    functions = db.relationship('Function', backref='parent_feature', lazy='dynamic')

    def __repr__(self):
        return "<Feature - {}>".format(self.Name)

class Capability(db.Model):
    __tablename__ = 'Projects.Capabilities'
    Id = db.Column(db.String(24), primary_key=True)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    LastUpdateDate = db.Column(db.String, index=True)
    PreliminaryEstimate = db.Column(db.Integer)
    ActualStartDate = db.Column(db.String)
    ActualEndDate = db.Column(db.String)
    CreationDate = db.Column(db.String)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    StateId = db.Column(db.String(24), db.ForeignKey('Projects.States.Id'))
    StateChangedDate = db.Column(db.String(50))
    PercentDoneByStoryCount = db.Column(db.Float)
    PercentDoneByStoryPlanEstimate = db.Column(db.Float)
    ReleaseId = db.Column(db.String(24), db.ForeignKey('Projects.Releases.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    features = db.relationship('Feature', backref='parent_capability', lazy='dynamic')
    def __repr__(self):
        return "<Capability - {}>".format(self.Name)

class Iteration(db.Model):
    __tablename__ = 'Projects.Iterations'
    Id = db.Column(db.String(24), primary_key=True)
    Name = db.Column(db.String(128))
    StartDate = db.Column(db.String, index=True)
    EndDate = db.Column(db.String, index=True)
    PlanEstimate = db.Column(db.Float)
    PlannedVelocity = db.Column(db.Float)
    State = db.Column(db.String(24))
    CreationDate = db.Column(db.String)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    stories = db.relationship('Story', backref='iteration', lazy='dynamic')
    tasks = db.relationship('Task', backref='iteration', lazy='dynamic')
    defects = db.relationship('Defect', backref='iteration', lazy='dynamic')

    def __repr__(self):
        return "<Iteration - {}, {} - {}>".format(self.Name, self.StartDate, self.EndDate)

class Story(db.Model):
    __tablename__ = 'Projects.Stories'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    #FlowStateId = db.Column(db.String(24), db.ForeignKey('Projects.FlowStates.Id'))
    PlanEstimate = db.Column(db.Integer)
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    ActualStartDate = db.Column(db.String, index=True)
    ActualEndDate = db.Column(db.String, index=True)
    CreationDate = db.Column(db.String)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    PercentDoneByStoryCount = db.Column(db.Float)
    PercentDoneByStoryPlanEstimate = db.Column(db.Float)
    ReleaseId = db.Column(db.String(24), db.ForeignKey('Projects.Releases.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    IterationId = db.Column(db.String(24), db.ForeignKey('Projects.Iterations.Id'))
    FunctionId = db.Column(db.String(24), db.ForeignKey('Projects.Functions.Id'))
    State = db.Column(db.String(24))
    KanbanState = db.Column(db.String(24))
    AcceptedDate = db.Column(db.String)
    ScheduleState = db.Column(db.String)
    tasks = db.relationship('Task', backref='story', lazy='dynamic')
    defects = db.relationship('Defect', backref='story', lazy='dynamic')

    def __repr__(self):
        return "<Story - {}, {} points; {}>".format(self.Name, self.PlanEstimate, self.State)

class Task(db.Model):
    __tablename__ = 'Projects.Tasks'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    Blocked = db.Column(db.Boolean)
    BlockedReason = db.Column(db.String(128))
    IterationId = db.Column(db.String(24), db.ForeignKey('Projects.Iterations.Id'))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    CreationDate = db.Column(db.String)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    ReleaseId = db.Column(db.String(24), db.ForeignKey('Projects.Releases.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    State = db.Column(db.String(24))
    Estimate = db.Column(db.Float)
    TimeSpent = db.Column(db.Float)
    Actuals = db.Column(db.Float)
    ToDo = db.Column(db.Float)
    StoryId = db.Column(db.String(24), db.ForeignKey('Projects.Stories.Id'))

    def __repr__(self):
        return "<Task - {}, {} estimated, {} to do>".format(self.Name, self.Estimate, self.ToDo)

class Defect(db.Model):
    __tablename__ = 'Projects.Defects'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    Blocked = db.Column(db.Boolean)
    BlockedReason = db.Column(db.String(128))
    ClosedDate = db.Column(db.String)
    AcceptedDate = db.Column(db.String)
    #FlowStateChangedDate = db.Column(db.String(50))
    LastUpdateDate = db.Column(db.String, index=True)
    InProgressDate = db.Column(db.String)
    IterationId = db.Column(db.String(24), db.ForeignKey('Projects.Iterations.Id'))
    StoryId = db.Column(db.String(24), db.ForeignKey('Projects.Stories.Id'))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    SubmittedById = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    #FlowStateId = db.Column(db.String(24), db.ForeignKey('Projects.FlowStates.Id'))
    CreationDate = db.Column(db.String)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    ReleaseId = db.Column(db.String(24), db.ForeignKey('Projects.Releases.Id'))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    ScheduleState = db.Column(db.String(24))
    Severity = db.Column(db.String(10))
    Environment = db.Column(db.String(50))
    TaskEstimateTotal = db.Column(db.Float)
    TaskActualTotal = db.Column(db.Float)
    TaskRemainingTotal = db.Column(db.Float)
    LastDiscussionAgeInMinutes = db.Column(db.Float)
    DefectState = db.Column(db.String(24))
    Priority = db.Column(db.String(24))
    Resolution = db.Column(db.String(50))

    defect_submitter = db.relationship("User", foreign_keys=[SubmittedById])
    defect_owner = db.relationship("User", foreign_keys=[OwnerId])

    def __repr__(self):
        return "<Defect - {}, Severity = {}>".format(self.Name, self.Severity)

class Release(db.Model):
    __tablename__ = 'Projects.Releases'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    CreationDate = db.Column(db.String)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))
    PlanEstimate = db.Column(db.Float)
    ReleaseDate = db.Column(db.String)
    ReleaseStartDate = db.Column(db.String)
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    TaskEstimateTotal = db.Column(db.Float)
    TaskActualTotal = db.Column(db.Float)
    TaskRemainingTotal = db.Column(db.Float)
    GrossEstimateConversionRatio = db.Column(db.Float)
    State = db.Column(db.String(24))
    PlannedVelocity = db.Column(db.Float)
    PointsAccepted = db.Column(db.Float)
    defects = db.relationship('Defect', backref='release', lazy='dynamic')
    tasks = db.relationship('Task', backref='release', lazy='dynamic')
    stories = db.relationship('Story', backref='release', lazy='dynamic')
    features = db.relationship('Feature', backref='release', lazy='dynamic')
    functions = db.relationship('Function', backref='release', lazy='dynamic')
    capabilities = db.relationship('Capability', backref='release', lazy='dynamic')

    def __repr__(self):
        return "<Release - {}, released on {}>".format(self.Name, self.ReleaseDate)

class Project(db.Model):
    __tablename__ = 'Workspace.Projects'
    Id = db.Column(db.String(24), primary_key=True)
    Name = db.Column(db.String(128))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    CreationDate = db.Column(db.String(50))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    releases = db.relationship('Release', backref='project', lazy='dynamic')
    defects = db.relationship('Defect', backref='project', lazy='dynamic')
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    stories = db.relationship('Story', backref='project', lazy='dynamic')
    iterations = db.relationship('Iteration', backref='project', lazy='dynamic')
    capabilities = db.relationship('Capability', backref='project', lazy='dynamic')
    features = db.relationship('Feature', backref='project', lazy='dynamic')
    functions = db.relationship('Function', backref='project', lazy='dynamic')
    test_folders = db.relationship('TestFolder', backref='project', lazy='dynamic')
    #flow_states = db.relationship('FlowState', backref='project', lazy='dynamic')

    def __repr__(self):
        return "<Project - {}>".format(self.Name)

"""
class FlowState(db.Model):
    __tablename__ = 'Projects.FlowStates'
    Id = db.Column(db.String(24), primary_key=True, nullable=False)
    Name = db.Column(db.String(128))
    #WorkspaceId = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    AgeThreshold = db.Column(db.String(24))
    CreationDate = db.Column(db.String)
    ExitPolicy = db.Column(db.String(128))
    OrderIndex = db.Column(db.Float)
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))

    def __repr__(self):
        return "<FlowState - {}>".format(self.Name)
"""

class TestCase(db.Model):
    __tablename__ = 'Projects.TestCases'
    Id = db.Column(db.String(24), primary_key=True)
    Name = db.Column(db.String(128))
    #WorkspaceId = db.Column(db.String(24), db.ForeignKey('workspace.id')
    ShortName = db.Column(db.String(24))
    CreationDate = db.Column(db.String(50))
    Method = db.Column(db.String(24))
    OwnerId = db.Column(db.String(24), db.ForeignKey('Workspace.Users.Id'))
    TestFolderId = db.Column(db.String(24), db.ForeignKey('Projects.TestFolders.Id'))
    TestingType = db.Column(db.String(24))
    Priority = db.Column(db.String(24))

class TestFolder(db.Model):
    __tablename__ = 'Projects.TestFolders'
    Id = db.Column(db.String(24), primary_key=True)
    Name = db.Column(db.String(128))
    ShortName = db.Column(db.String(24))
    CreationDate = db.Column(db.String(50))
    ProjectId = db.Column(db.String(24), db.ForeignKey('Workspace.Projects.Id'))

    test_cases = db.relationship('TestCase', backref='folder', lazy='dynamic')

class State(db.Model):
    __tablename__ = 'Projects.States'
    Id = db.Column(db.String(24), primary_key=True)
    Name = db.Column(db.String(24))
    CreationDate = db.Column(db.String(24))
    OrderIndex = db.Column(db.Integer)

    capabilities = db.relationship('Capability', backref='state', lazy='dynamic')
    features = db.relationship('Feature', backref='state', lazy='dynamic')
    functions = db.relationship('Function', backref='state', lazy='dynamic')