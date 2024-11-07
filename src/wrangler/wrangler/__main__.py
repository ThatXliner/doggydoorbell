import csv
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pydub import AudioSegment


def process(file, annotations, output_folder, segment_length=3000):
    print(f"Processing {file}")
    filename = str(file.resolve())
    audio = AudioSegment.from_file(filename)
    audio_length = len(audio)

    # # Get annotations specific to this file
    # file_annotations = annotations.get(filename, [])

    # Split audio and apply labels
    for i in range(0, audio_length, segment_length):
        segment = audio[i : i + segment_length]
        segment_label = get_segment_label(i, i + segment_length, file.stem, annotations)

        # Save segment with label as part of filename
        segment_filename = (
            f"{file.stem}_segment_{i // segment_length + 1}_{segment_label}.mp3"
        )
        segment_path = output_folder.joinpath(segment_filename)
        segment.export(str(segment_path.resolve()), format="mp3")
        print(f"Exported {segment_path} with label {segment_label}")


def split_and_label_audio(input_folder, annotations, segment_length=3000):
    # Load annotations from JSON file
    # with open(annotation_file, 'r') as f:
    #     annotations = json.load(f)

    output_folder = Path(input_folder) / "output"
    output_folder.mkdir(exist_ok=True)
    with ThreadPoolExecutor() as executor:
        futures = []
        for file in Path(input_folder).glob("*.mp3"):
            futures.append(
                executor.submit(
                    process,
                    file,
                    annotations,
                    output_folder,
                    segment_length=segment_length,
                )
            )
        # Wait for all futures to complete
        for future in futures:
            future.result()


def get_segment_label(start_time, end_time, filename, annotations):
    labels = set()
    for annotation in annotations[filename]:
        # Convert times to milliseconds and check for overlap
        annotation_start = annotation["start_time"] * 1000
        annotation_end = annotation["end_time"] * 1000
        if annotation_start < end_time and annotation_end > start_time:
            labels.add(annotation["label"].split("/")[-1])

    return "_".join(labels) if labels else "unlabeled"


def main():
    # Example usage
    # input_folder = 'path_to_your_audio_folder'  # Update this with your audio directory
    # annotation_file = 'path_to_your_annotation_file.json'  # Path to your annotation JSON file
    annotations = {}
    for line in Path(sys.argv[2]).read_text().splitlines()[1:]:
        segment_id, start_time_seconds, end_time_seconds, label = line.split("\t")
        annotations[segment_id.rsplit("_", maxsplit=1)[0]] = annotations.get(
            segment_id, []
        ) + [
            {
                "start_time": float(start_time_seconds),
                "end_time": float(end_time_seconds),
                "label": label,
            }
        ]
    # annotations = {line.split('\t')[0].split("_")[0]:(line.split('\t')[1], line.split('\t')[2]) }
    split_and_label_audio(sys.argv[1], annotations)


if __name__ == "__main__":
    main()
