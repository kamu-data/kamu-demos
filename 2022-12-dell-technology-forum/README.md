# Dell Technologies Forum 2022 Demo


## Parties
This demo is a collaboration of:
- University of Twente (ESportsLab)
- Dell Technologies
- Kamu Data Inc.


## Demo Structure
Directories:
- `ingest` - datasets and scripts related to adding new data to datasets
- `frontend` - notebooks used for data science and to display the results

Data flow:
- RocketLeague plugin produces the match replay file
- File is placed into `ingest/replays` directory
- The `matches` dataset in Kamu parses replay files into JSON using `rattletrap`
- The `matches` dataset is used as a basis for a few other derivative datasets
- Jupyter notebooks in `frontend/` directory are used for additional data analysis and visualization


## Prerequisites
1. Install `kamu` ([instructions](https://docs.kamu.dev/cli/get-started/installation/))


## Using the Demo

### Ingesting data
While in the `ingest/` directory do:
```bash
# Initialize the workspace
kamu init

# Create new datasets from manifest files
kamu add datasets/*

# Ingest data from replays in the ./replays/ directory
kamu pull --all
```

### Push data to repository
Steps below share data through a common directory - in future we will replace it with IPFS:
```bash
# Create a repo in shared directory
kamu repo add hub "file://`pwd`/../share"

# Perform initial push of datasets
kamu push <dataset_name> --to hub/<dataset_name>
```

### Processing new replays
You can now add more replays to the `replays/` directory and ingest them as:

```bash
# Ingest new replays
kamu pull --all

# Push all updates to the repository
kamu push <dataset 1> <datset 2> <dataset N>
```

### Pull data to frontend
While in the `frontend/` directory do:
```bash
kamu init

# For the first time you'll need to list datasets explicitly
kamu pull hub/<dataset 1> hub/<dataset 2> hub/<dataset N>

# Subsequently all datasets can be refreshed with
kamu pull --all
```

### Visualize data
Start the notebook environment:
```bash
kamu notebook
```

Pick and execute individual notebooks.
