"""The main CLI entry point."""

import json
import sys
from pathlib import Path

import yt_dlp

TAGS = {
    "/t/dd00136",
    "/t/dd00141",
    "/m/01z5f",
    "/m/0bt9lr",
}


def main() -> None:
    """Run the app."""
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    urls = {
        f"https://www.youtube.com/watch?v={line.split('\t')[0].rsplit('_', 1)[0]}"
        for line in Path(sys.argv[1]).read_text().splitlines()[1:]
        if line.split("\t")[-1] in TAGS
    }
    print(urls)
    with yt_dlp.YoutubeDL(
        params={
            "paths": {"home": str(output.resolve())},
            "outtmpl": {"default": "%(id)s.%(ext)s"},
            "ignoreerrors": "only_download",
        }
    ) as ydl:
        ydl.download(urls)


if __name__ == "__main__":
    main()
