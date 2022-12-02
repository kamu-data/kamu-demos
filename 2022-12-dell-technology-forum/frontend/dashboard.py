import os
import sys
import argparse
import logging
import time
import json
import subprocess
import datetime
import shutil

logger = logging.getLogger(__package__)


#########################################################################################

def main(args):
    test_jupyter_running(args)

    os.makedirs(args.output_dir, exist_ok=True)

    logger.info("Watching datasets for updates")
    head = None

    while True:
        time.sleep(args.loop_delay)

        new_head = get_head_raw()
        if new_head == head:
            continue
        
        head = new_head
        logger.debug("Detected new head: %s", head)

        render_dashboard(args)
        
        logger.info("Finished the render loop")
        logger.info("Watching datasets for updates")


# TODO: Kamu needs concurrency protection for this not to interfere with pulls
def get_head():
    from io import StringIO
    import csv

    klist = subprocess.run([
        "kamu",
        "list",
        "--output-format", "csv",
        "--wide",
    ], check=True, capture_output=True, text=True)

    for r in csv.reader(StringIO(klist.stdout)):
        if r[1] == "player-scores":
            return r[3]
    
    raise Exception("Failed to get head of player-scores dataset")


def get_head_raw():
    with open(".kamu/datasets/player-scores/refs/head", "r") as f:
        return f.read().strip()


def render_dashboard(args):
    logging.info("Rendering the notebook...")

    subprocess.run([
        args.container_runtime,
        "exec",
        "kamu-jupyter",
        "jupyter",
        "nbconvert",
        "--output-dir", args.output_dir,
        "--to", "html",
        "--template", "lab",
        "--no-input",
        "--execute",
        "dashboard.ipynb",
    ], check=True)


def test_jupyter_running(args):
    try:
        subprocess.run([
            args.container_runtime,
            "exec",
            "kamu-jupyter",
            "echo",
            "test",
        ], check=True, stdout=subprocess.PIPE)
    except:
        raise Exception(
            f"Container {args.jupyter_container_name} doesn't seems to be running under {args.container_runtime}"
        )


#########################################################################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s", stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument('--container-runtime', default="docker", help="Whether to use docker of podman")
    parser.add_argument('--jupyter-container-name', default="kamu-jupyter", help="Name of the container where Jupyter is running")
    parser.add_argument('--loop-delay', type=float, default=1.0, help="Delay between directory scans")
    parser.add_argument('--output-dir', default="output", help="Output directory")

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        logger.info("Aborting")
        pass
