from db import recreate_database
from extract import extract, get_language_map
from transform import (transform_owners, 
                       transform_languages, 
                       transform_repositories)
from load import load_owners, load_languages, load_repositories

def main():
    recreate_database()

    repositories_data = extract("microsoft")

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


if __name__ == "__main__":
    main()