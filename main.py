import pandas as pd

from config import ORGANIZATIONS

from extract import (extract_repositories, extract_issues, extract_commits, 
                     get_language_map, get_owner_id, get_repository_ids)
from transform import (transform_owners, 
                       transform_languages, 
                       transform_repositories,
                       transform_issues,
                       transform_commits)
from load import (
    load_owners,
    load_languages,
    load_repositories,
    load_issues,
    load_commits,
)
from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def main():
    run_migrations()

    for org in ORGANIZATIONS:
        owner_id = get_owner_id(org)
        if owner_id is None:
            existing_repo_ids = {}
        else:
            existing_repo_ids = get_repository_ids(owner_id)

        repositories_data = extract_repositories(org)

        new_repo_ids = {
            repo["id"]
            for repo in repositories_data
            if repo["id"] not in existing_repo_ids
        }

        owners_df = transform_owners(repositories_data)
        load_owners(owners_df)

        languages_df = transform_languages(repositories_data)
        load_languages(languages_df)

        language_map = get_language_map()

        repositories_df = transform_repositories(
            repositories_data,
            language_map,
        )
        load_repositories(repositories_df, org_name=org)
        print(f"{org}: Загружено {len(repositories_data)} репозиториев")

        # Получение и загрузка issues и commits для каждого репозитория
        all_issues_dfs = []
        all_commits_dfs = []
        for repo in repositories_data:
            repo_id = repo["id"]
            repo_name = repo["name"]
            is_new_repo = repo_id in new_repo_ids
            issues_data = extract_issues(org, repo_name, is_new_repo)
            if issues_data:
                issues_df = transform_issues(issues_data, repo_id)
                if not issues_df.empty:
                    all_issues_dfs.append(issues_df)

            commits_data = extract_commits(org, repo_name, is_new_repo)
            if commits_data:
                commits_df = transform_commits(commits_data, repo_id)
                if not commits_df.empty:
                    all_commits_dfs.append(commits_df)

        combined_issues_df = pd.DataFrame()
        if all_issues_dfs:
            combined_issues_df = pd.concat(all_issues_dfs, ignore_index=True)
        load_issues(combined_issues_df, org_name=org)
        print(f"{org}: Загружено {len(combined_issues_df)} issues")

        combined_commits_df = pd.DataFrame()
        if all_commits_dfs:
            combined_commits_df = pd.concat(all_commits_dfs, ignore_index=True)
        load_commits(combined_commits_df, org_name=org)
        print(f"{org}: Загружено {len(combined_commits_df)} commits")

if __name__ == "__main__":
    main()