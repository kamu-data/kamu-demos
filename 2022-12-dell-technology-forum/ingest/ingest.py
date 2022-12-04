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
    os.makedirs(args.replays_dir, exist_ok=True)
    os.makedirs(args.replays_staging_dir, exist_ok=True)

    replays_seen = init_seen_replays(args.replays_staging_dir)
    logger.info("Initialized with %s staged replays", len(replays_seen))

    if replays_seen:
        # Run ingest to ensure all previously staged files have been processed
        run_ingest()

    logger.info("Watching the %s direcory for replays", args.replays_dir)

    while True:
        time.sleep(args.loop_delay)

        new_replays = check_for_new_replays(args.replays_dir, replays_seen)
        if not new_replays:
            continue

        replays_seen.update(replay_id(fn) for fn in new_replays)
        logger.info("Found %s new replay(s)", len(new_replays))
        logger.debug("New replays: %s", new_replays)

        staged_replays = stage_replays(args.replays_staging_dir, new_replays)
        if not stage_replays:
            continue
        
        run_ingest()
        logger.info("Finished the ingest loop")
        logger.info("Watching the %s direcory for more replays", args.replays_dir)


def init_seen_replays(replays_staging_dir):
    if not os.path.exists(replays_staging_dir):
        return set()
    
    return {
        replay_id_staged(fn)
        for fn in os.listdir(replays_staging_dir)
    }


def check_for_new_replays(replays_dir, replays_seen):
    if not os.path.exists(replays_dir):
        return []

    return [
        os.path.join(replays_dir, fn)
        for fn in os.listdir(replays_dir)
        if replay_id(fn) not in replays_seen
    ]


def stage_replays(replays_staging_dir, new_replay_files):
    ret = []
    
    for fname in new_replay_files:
        rid = replay_id(fname)
        
        # Use timestamp of the original replay
        # Note: causes some replays to be skipped by Kamu if ingested out of order
        # header = replay_header(fname)
        # ts = header["header"]["body"]["properties"]["value"]["Date"]["value"]["str"]
        # timestamp = replay_timestamp(header)

        # Use current time for monotonous file ordering
        timestamp = datetime.datetime.utcnow()
        
        staged_path = os.path.join(
            replays_staging_dir,
            "{}-{}.replay".format(timestamp.strftime("%Y%m%dT%H%M%S"), rid)
        )
        
        logging.debug("Staging replay to %s", staged_path)
        shutil.copyfile(fname, staged_path)
        ret.append(staged_path)
    
    return ret


def run_ingest():
    from io import StringIO
    import csv

    logging.info("Updating the data pipelines")
    subprocess.run([
        "kamu pull --all",
    ], shell=True, check=True)

    klist = subprocess.run([
        "kamu list -o csv",
    ], shell=True, check=True, capture_output=True, text=True)

    rows = list(csv.reader(StringIO(klist.stdout)))
    dataset_names = [r[1] for r in rows[1:]]
    
    logging.info("Syncing all datasets to remote")
    klist = subprocess.run([
        "kamu push --force {}".format(" ".join(dataset_names)),
    ], shell=True, check=True)


#########################################################################################
# Replay utils
#########################################################################################

def replay_id(replay_path):
        return os.path.splitext(os.path.basename(replay_path))[0]

def replay_id_staged(staged_path):
        return os.path.splitext(os.path.basename(staged_path))[0].rsplit("-", 1)[1]

def replay_header(replay_path):
    return json.loads(subprocess.check_output([
        "rrrocket/rrrocket",
        "-n",
         replay_path,

    ]))

def replay_timestamp(header):
    ts = header["header"]["body"]["properties"]["value"]["Date"]["value"]["str"]
    return datetime.datetime.strptime(ts, "%Y-%m-%d %H-%M-%S")


#########################################################################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s", stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument('--replays-dir', default="./replays", help="Directory where original replay files are shared")
    parser.add_argument('--loop-delay', type=float, default=1.0, help="Delay between directory scans")
    parser.add_argument('--replays-staging-dir', default="./replays-staged", help="Directory renamed replay files are put for kamu")

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        logger.info("Aborting")
        pass
