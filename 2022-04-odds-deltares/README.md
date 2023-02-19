# Deltares Demo

This demo was created in collaboration with [Deltares](https://www.deltares.nl/en/) - an organization that uses data for flood management. It uses IoT-like data from water level measurement stations located on rivers of the Rhine basin in Netherlands which is collected by [Rijkswaterstaat](https://www.rijkswaterstaat.nl/en) (Ministry of Infrastructure and Water Management of Netherlands).

This project demonstrates how Kamu pipelines can be used for:
- Colletcing dynamic data from multiple different sources of raw data into a single dataset
- Achieving fully reproducible and traceable data science

## Getting Started

Fastest way to get started is by getting datasets from S3:

```sh
make init-s3
kamu list
```

You can then explore and analyze data using:

```sh
kamu ui
kamu notebook
```

## Setting up demo with IPFS

Start with a fully initialized workspace (e.g. by downloading data via step above).

Setup IPNS keys for every dataset:

```sh
make ipns-keys
```

Add all datasets to IPFS and update corresponding IPNS keys:

```sh
kamu push-ipns
```

Now on a different machine you should be able to pull all data from IPFS using:

```sh
make init-ipfs
```
