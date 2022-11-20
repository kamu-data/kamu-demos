import json
import os
import pathlib
import subprocess

from rattletrap.structures import Replay

file_directory = pathlib.Path(__file__).parent.absolute()
rattletrap_exe = os.path.join(file_directory, "rattletrap")


def query_replay(input_file: str) -> Replay:
    json_output = json.loads(subprocess.check_output([
        rattletrap_exe,
        "-i", input_file,
        "-c",
        "--skip-crc",
    ]))
    return Replay.from_json(json_output)
