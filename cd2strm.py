import yaml
from pathlib import Path

CONFIG_FILE = "config.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_bdmv(source):
    source = Path(source)

    if not source.exists():
        print(f"[ERROR] Source not found: {source}")
        return

    print(f"\nScanning: {source}")

    count = 0

    for bdmv in source.rglob("BDMV"):
        if not bdmv.is_dir():
            continue

        movie = bdmv.parent

        print(f"Found BDMV:")
        print(f"  Movie : {movie.name}")
        print(f"  Path  : {movie}")

        count += 1

    print(f"\nFinished.")
    print(f"Found {count} BDMV folders.\n")


def main():
    config = load_config()

    for source in config["source"]:
        find_bdmv(source)


if __name__ == "__main__":
    main()
