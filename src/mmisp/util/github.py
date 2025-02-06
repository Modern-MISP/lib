from typing import Optional, Self

from github import Github, GithubException, UnknownObjectException
from github.ContentFile import ContentFile


class GithubUtils:
    _GITHUB_RAW_TEMPLATE = "https://raw.githubusercontent.com/{}/refs/heads/{}/"

    def __init__(self: Self, repository_name: str, branch_name: Optional[str] = None) -> None:
        self._github = Github()
        try:
            self.repository = self._github.get_repo(repository_name)
            self.branch = self.repository.get_branch(branch_name if branch_name else self.repository.default_branch)
            self.url_template = self._GITHUB_RAW_TEMPLATE.format(repository_name, self.branch.name)
        except (UnknownObjectException, GithubException):
            raise AttributeError

    def get_raw_url(self: Self) -> str:
        return self.url_template

    def list_directories(self: Self, path: str) -> Optional[list[str]]:
        try:
            content = self.repository.get_contents(path)
        except UnknownObjectException:
            return None

        if isinstance(content, ContentFile):
            return None

        dirs = []
        for element in content:
            if element.type == "dir":
                dirs.append(element.path)

        return dirs

    def list_files(self: Self, path: str) -> Optional[list[str]]:
        try:
            content = self.repository.get_contents(path)
        except UnknownObjectException:
            return None

        if isinstance(content, ContentFile):
            return [content.path]

        files = []
        for element in content:
            if element.type == "file":
                files.append(element.path)

        return files
