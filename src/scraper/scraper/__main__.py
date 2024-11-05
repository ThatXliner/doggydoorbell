"""The main CLI entry point."""

import yt_dlp
from pathlib import Path
import json
import sys
TAGS = {"/m/0bt9lr"
,"/m/0bt9lr"
,"/m/05tny_"
,"/m/07r_k2n"
,"/m/07qf0zm"
,"/m/07rc7d9"
,"/m/0ghcn6"
,"/t/dd00136"}
def main() -> None:
    """Run the app."""
    URLS = []
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    # csv = [line.split(", ") for line in Path(sys.argv[1]).read_text().splitlines()[2:] if any(tag in line for tag in TAGS)]
    csv =  [x.removeprefix('https://img.youtube.com/vi/').split('/') for x in json.loads(Path(sys.argv[1]).read_text())]
    print(len(csv))
    URLS.extend(f'https://www.youtube.com/watch?v={line[0]}' for line in csv)
    with yt_dlp.YoutubeDL(params={"paths": {"home": str(output.resolve())}, "outtmpl": {"default": "%(id)s.%(ext)s"}, "ignoreerrors": "only_download"}) as ydl:
        ydl.download(URLS)


if __name__ == "__main__":
    main()
