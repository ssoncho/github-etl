import pandas as pd

from db import recreate_database
from extract import extract_repositories, extract_issues, extract_commits, get_language_map
from transform import (transform_owners, 
                       transform_languages, 
                       transform_repositories,
                       transform_issues,
                       transform_commits)
from load import load_owners, load_languages, load_repositories, load_issues, load_commits

def main():
    recreate_database()
    org_name = "microsoft"

    repositories_data = extract_repositories(org_name)

    owners_df = transform_owners(repositories_data)
    load_owners(owners_df)

    languages_df = transform_languages(repositories_data)
    load_languages(languages_df)

    language_map = get_language_map()

    repositories_df = transform_repositories(
        repositories_data,
        language_map,
    )
    load_repositories(repositories_df)
    print(f"Загружено {len(repositories_data)} репозиториев")

    # Получение и загрузка issues для каждого репозитория
    all_issues_dfs = []
    all_commits_dfs = []
    for repo in repositories_data:
        repo_id = repo["id"]
        repo_name = repo["name"]
        issues_data = extract_issues(org_name, repo_name)
        if issues_data:
            issues_df = transform_issues(issues_data, repo_id)
            if not issues_df.empty:
                all_issues_dfs.append(issues_df)

        commits_data = extract_commits(org_name, repo_name)
        if commits_data:
            commits_df = transform_commits(commits_data, repo_id)
            if not commits_df.empty:
                all_commits_dfs.append(commits_df)

    if all_issues_dfs:
        combined_issues_df = pd.concat(all_issues_dfs, ignore_index=True)
        load_issues(combined_issues_df)
        print(f"Загружено {len(combined_issues_df)} issues")
    else:
        print("Issues не найдены")

    if all_commits_dfs:
        combined_commits_df = pd.concat(all_commits_dfs, ignore_index=True)
        load_commits(combined_commits_df)
        print(f"Загружено {len(combined_commits_df)} commits")
    else:
        print("Commits не найдены")


if __name__ == "__main__":
    main()