#! /usr/bin/env python
import os
from dotenv import load_dotenv
load_dotenv()

TEXTBOOK_PATH = os.environ.get("TEXTBOOK_PATH")
WRITE_PATH = os.environ.get("WRITE_PATH")
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
from base64 import b64decode
from github import Github


api = Github(login_or_token=GITHUB_ACCESS_TOKEN)
site = api.get_repo("open-resources/instructor_stats_bank")


def create_branch(branch_name):
    return site.create_git_ref(
        f'refs/heads/{branch_name}'.format(**locals()),
        site.get_branch('main').commit.sha
    )


def commit_change(branch_name):
    index_file = site.get_contents('index.html')
    # index_content = b64decode(index_file.content)
    # updated_content = index_content.replace('<html>', '<html lang="en">')
    site.create_file(
        path='/index.html',
        message='Add language to markup',
        content=updated_content,
        branch=branch_name
    )

    return site.update_file(
        path='/index.html',
        message='Add language to markup',
        content=updated_content,
        sha=index_file.sha,
        branch=branch_name
    )


def create_pull_request(branch_name):
    return site.create_pull(
        title="Add language to markup",
        body=(
            "# Description\n\nAdd `lang=en` to the HTML tag.\n"
            "# QA\n\nThis will literally change nothing of significance."
        ),
        base="master",
        head=branch_name
    )

branch_name = "add-language"
create_branch(branch_name)
commit_change(branch_name)
pull = create_pull_request(branch_name)

print(pull.html_url)