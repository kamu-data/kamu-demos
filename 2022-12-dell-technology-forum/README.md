# Dell Technologies Forum 2022 Demo


## Parties
This demo is a collaboration of:
- University of Twente (ESportsLab)
- Dell Technologies
- Kamu Data Inc.


## Demo Structure
Directories:
- `/ingest` - datasets and scripts related to adding new data
- `/frontend` - notebooks used for data science and to display the results
- `/Makefile` - the controlling script

Data flow:
- RocketLeague plugin produces the match replay file
- File is placed into `ingest/replays` directory
- The `ingest/ingest.py` script:
  - Detects new replay files
  - Calls `kamu pull` to parse replays into structured dataset
  - Updates the rest of datasets in the pipeline
  - Syncs datasets into IPFS
- User on the frontend side:
  - Runs `kamu pull --all` to update datasets from IPFS
  - Opens a Jupyter notebook to visualize data


## Prerequisites
1. Install `kamu` ([instructions](https://docs.kamu.dev/cli/get-started/installation/))
2. (Optional) Install `ipfs` daemon


## Using the Demo

### Initialize the pipeline
In the demo directory run:
```bash
# On the ingest side
make init-ingest

# On the frontend side
make init-frontend
```

> Alternatively you can use `init-ingest-lfs` and `init-frontend-lfs` to use local file system instead of IPFS.

This initialized the datasets and connects via shared storage so that:
- `kamu push` on the ingest side will store the updates in IPFS (or LFS)
- and `kamu pull --all` on the frontend side will get the fresh data


### Ingesting data
First start the ingest process by running:
```bash
make ingest-loop
```

If you don't have RocketLeague set up - you can manually add some sample replays to the directory monitored by ingest process:
```bash
cp ingest/replays-sample/2D9559FB4928ED80E5F1D48DDA3AA8E2.replay ingest/replays/
```

The ingest process will now:
- automatically detect new file
- ingest the data into `kamu`
- push the updated datasets into shared storage


### Pull data to frontend
While in the `frontend/` directory do this to get the latest data:
```bash
kamu pull --all
```

### Visualize data
Start the notebook environment:
```bash
kamu notebook
```

Pick and execute individual notebooks.


### Cleaning up
To clean the whole workspace up you can run:
```bash
make clean-all
```

This will remove all replays, all IPFS demo keys, and kamu workspaces
