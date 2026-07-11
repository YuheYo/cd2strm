import yaml
from pathlib import Path

CONFIG_FILE = "config.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    print("Source:")
    for path in config["source"]:
        print(" -", path)

    print("Output:")
    print(config["output"])


if __name__ == "__main__":
    main()
