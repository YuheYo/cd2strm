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

        stream = bdmv / "STREAM"

        if not stream.exists():
            print("  STREAM folder missing")
            continue

        m2ts_files = list(stream.glob("*.m2ts"))

        if not m2ts_files:
            print("  No m2ts found")
            continue

        largest = max(m2ts_files, key=lambda f: f.stat().st_size)

        size = largest.stat().st_size / 1024 / 1024 / 1024

        print("Found BDMV:")
        print(f"  Movie : {movie.name}")
        print(f"  Path  : {movie}")
        print(f"  Main  : {largest.name}")
        print(f"  Size  : {size:.2f} GB")

        count += 1

    print(f"\nFinished.")
    print(f"Found {count} BDMV folders.\n")


def main():
    config = load_config()

    for source in config["source"]:
        find_bdmv(source)


if __name__ == "__main__":
    main()
