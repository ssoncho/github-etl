import pandas as pd

from db import recreate_database
from extract import extract_repositories, extract_issues, get_language_map
from transform import (transform_owners, 
                       transform_languages, 
                       transform_repositories,
                       transform_issues)
from load import load_owners, load_languages, load_repositories, load_issues

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

    # Получение и загрузка issues для каждого репозитория
    all_issues_dfs = []
    for repo in repositories_data:
        repo_id = repo["id"]
        repo_name = repo["name"]
        issues_data = extract_issues(org_name, repo_name)
        if issues_data:
            issues_df = transform_issues(issues_data, repo_id)
            all_issues_dfs.append(issues_df)

    if all_issues_dfs:
        combined_issues_df = pd.concat(all_issues_dfs, ignore_index=True)
        load_issues(combined_issues_df)
        print(f"Загружено {len(combined_issues_df)} issues")
    else:
        print("Issues не найдены")

    print(f"Загружено {len(repositories_data)} репозиториев")


if __name__ == "__main__":
    main()