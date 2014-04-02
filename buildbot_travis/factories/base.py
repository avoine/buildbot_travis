
from buildbot.process import factory
from buildbot.steps.source import SVN, Git

class BaseFactory(factory.BuildFactory):
    """
    Generic factory that deals with SVN (or Git)
    """

    def __init__(self, projectname, repository, vcs_type=None, branch=None, username=None, password=None, subrepos=None):
        factory.BuildFactory.__init__(self, [])
        self.addRepository(projectname, repository, vcs_type, branch, username, password)
        if subrepos:
            for subrepo in subrepos:
                self.addRepository(
                    **subrepo
                    )

    def addRepository(self, project=None, repository=None, vcs_type=None, branch=None, username=None, password=None, **kwargs):
        kwargs = dict(kwargs)

        if not repository.endswith("/") and not repository.startswith("git@"):
            repository += "/"

        if not vcs_type:
            if repository.startswith("https://svn."):
                vcs_type = "svn"
            elif repository.startswith("git://") or repository.startswith("git@"):
                vcs_type = "git"

        if not branch:
            branch = dict(svn="trunk", git="master")[vcs_type]

        if vcs_type == "svn":
            kwargs.update(dict(
                baseURL=repository,
                defaultBranch=branch,
                username=username,
                password=password,
                codebase=project,
                ))

            self.addStep(SVN(**kwargs))

        elif vcs_type == "git":
            kwargs.update(dict(
                repourl=repository,
                branch=branch,
                codebase=project,
                ))

            self.addStep(Git(**kwargs))

