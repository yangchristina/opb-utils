# requires functions in issues-to-questions.py

if __name__ == "__main__":
    print('hi')

    # read_chapter("7")
    with open('issues.txt', 'w') as f:
        f.write('')
    # latex_to_markdown('')
    # Public Web Github
    g = Github(login_or_token=GITHUB_ACCESS_TOKEN)

    print('group 1', github_profiles[0:3])
    print('group 2', github_profiles[3:])
    ch7issues = read_all_chapter("7", github_profiles[0:3])
    ch8issues = read_all_chapter("8", github_profiles[3:])
    all_issues = ch7issues + ch8issues
    # read_chapter("7", [{"question_number": i, 'issue_title': 'TODO'} for i in range(1,10,2)])

    # Github Enterprise with custom hostname
    # g = Github(base_url="https://{hostname}/api/v3", auth=auth)

    repo = g.get_repo("open-resources/instructor_stats_bank")
    body = "This question can be found in the GitHub repo for the OpenIntro Stats textbook. For example, here is a link to one sample chapter: https://github.com/OpenIntroStat/openintro-statistics/blob/master/ch_distributions/TeX/ch_distributions.tex"
    for i, issue in enumerate(all_issues[33:]):
        try:
            print('issue', issue)
            if "assignee" in issue:
                repo.create_issue(title=issue["issue_title"], body=body, assignee=issue["assignee"])
            else:
                repo.create_issue(title=issue["issue_title"], body=body)
        except Exception as e:
            print("Q", i)
            print('Error creating issue', issue)
            print(e)
            time.sleep(5)
            continue