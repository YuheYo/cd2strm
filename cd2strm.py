import yaml
import shutil
from pathlib import Path

CONFIG_FILE = "config.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_largest_m2ts(stream_dir):
    m2ts_files = list(stream_dir.glob("*.m2ts"))
    if not m2ts_files:
        return None
    return max(m2ts_files, key=lambda f: f.stat().st_size)


def generate_strm(movie_dir, largest_m2ts, output_dir):
    movie_name = movie_dir.name
    out_dir = Path(output_dir) / movie_name
    out_dir.mkdir(parents=True, exist_ok=True)

    strm_path = out_dir / f"{movie_name}.strm"

    if strm_path.exists():
        print(f"  [SKIP] Already exists: {strm_path}")
        return

    with open(strm_path, "w", encoding="utf-8") as f:
        f.write(str(largest_m2ts))

    print(f"  [STRM] Generated: {strm_path}")


def copy_images(movie_dir, output_dir, image_files):
    movie_name = movie_dir.name
    out_dir = Path(output_dir) / movie_name

    for img in image_files:
        src = movie_dir / img
        dst = out_dir / img
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"  [IMG]  Copied: {img}")


def scan_movies(source, output, image_files):
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
            print(f"  [WARN] No STREAM: {movie.name}")
            continue

        largest = find_largest_m2ts(stream)

        if not largest:
            print(f"  [WARN] No m2ts: {movie.name}")
            continue

        size = largest.stat().st_size / 1024 / 1024 / 1024

        print(f"\nFound: {movie.name}")
        print(f"  Main : {largest.name}")
        print(f"  Size : {size:.2f} GB")

        generate_strm(movie, largest, output)
        copy_images(movie, output, image_files)

        count += 1

    print(f"\nFinished. Generated {count} STRM files.\n")


def main():
    config = load_config()

    output = config["output"]

    image_files = config.get("image_files", [
        "poster.jpg",
        "fanart.jpg",
        "clearlogo.png",
    ])

    for source in config["source"]:
        scan_movies(source, output, image_files)


if __name__ == "__main__":
    main()
