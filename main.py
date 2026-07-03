from extract import extract
from transform import transform_repositories
from load import load_repositories

def main():
    raw_data = extract("microsoft")
    repositories = transform_repositories(raw_data)
    load_repositories(repositories)

    print(f"Загружено {len(repositories)} репозиториев")


if __name__ == "__main__":
    main()