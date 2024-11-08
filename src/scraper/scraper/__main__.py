"""The main CLI entry point."""

import json
import sys
import time
from itertools import zip_longest
from pathlib import Path

import yt_dlp


def chunk_list[T](lst: list[T], n: int) -> list[tuple[T]]:
    # Use zip_longest to chunk the list, filling the last chunk with None if needed
    args = [iter(lst)] * n
    return list(zip_longest(*args, fillvalue=None))


# # Example usage
# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# chunked = chunk_list(my_list, 3)
# print(chunked)  # Output: [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
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
    already_exists = {x.stem for x in output.glob("*.mp3")}
    urls = {
        f"https://www.youtube.com/watch?v={line.split('\t')[0].rsplit('_', 1)[0]}"
        for line in Path(sys.argv[1]).read_text().splitlines()[1:]
        if line.split("\t")[-1] in TAGS
        and line.split("\t")[0].rsplit("_", 1)[0] not in already_exists
    }
    print(len(urls))
    url_epochs = chunk_list(list(urls), 100)
    with yt_dlp.YoutubeDL(
        params={
            "paths": {"home": str(output.resolve())},
            "outtmpl": {"default": "%(id)s.%(ext)s"},
            "ignoreerrors": "only_download",
            "extractaudio": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "nopostoverwrites": False,
                    "preferredcodec": "mp3",
                    "preferredquality": "5",
                }
            ],
        }
    ) as ydl:
        for urls in url_epochs:
            ydl.download(urls)
            # Cooldown to avoid rate limits
            time.sleep(60)


if __name__ == "__main__":
    main()
