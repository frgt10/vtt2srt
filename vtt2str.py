#!/usr/bin/env python3

import argparse
import webvtt
import re
from pathlib import Path


def parse_args():
    argparser = argparse.ArgumentParser(
        description="WEBVTT to SRT subtitle converter.",
    )

    argparser.add_argument(
        "path",
        metavar="PATH",
        help="A VTT file or directory with files to be converted.",
    )

    return argparser.parse_args()


def get_files(path: Path) -> list:
    files = []

    if path.is_dir():
        files += path.glob("*.vtt")
    else:
        files.append(path)

    return files


def convert_vtt_to_srt(vtt: Path) -> None:
    print("\nInput: " + vtt.name)
    srt = vtt.with_suffix(".srt")
    print("Output: " + srt.name)

    if vtt == srt:
        raise (Exception("The input and output file is the same file."))

    with srt.open(mode="w") as f:
        i = 0
        for caption in webvtt.read(vtt):
            i += 1
            print(i, file=f)
            print(
                re.sub(r"\.", ",", caption.start)
                + " --> "
                + re.sub(r"\.", ",", caption.end),
                file=f,
            )
            print(caption.text + "\n", file=f)


def main():
    args = parse_args()

    files = get_files(Path(args.path))

    total = len(files)
    i = 0

    for vtt in files:
        i += 1
        print("Process file %02d / %02d" % (i, total))
        convert_vtt_to_srt(vtt)


if __name__ == "__main__":
    main()
