# CODWG Demo Plan

## Intro (1:00)

Thanks, excited to share what we've been working on with the group.

The area of Web3-data Kamu is focusing on is how organization can rapidly exchange structured data and transform and improve it along the way in a trustless environment.

Today I will show you our tool that is one of the key pieces to creating such planet-scale data supply chains.

>> kamu

Kamu us a single-binary tool which you can download today and use on your laptop
    think of it as git + kubernetes + blockchain for data
    (I promise it will all make sense by the end)

We start by creating a workspace

>> kamu init

## Pull from IPFS (0:40)

It makes sharing data very easy.
The same simplicity that IPFS achieves for sharing files - Kamu brings to structured data.

Here's how you can pull data from the network.

>> kamu pull "ipns://com.cryptocompare.ohlcv.eth-usd.ipns.kamu.dev" --as cryptocompare.ohlcv.eth-usd --no-alias
>> kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/com.cryptocompare.ohlcv.eth-usd" --as cryptocompare.ohlcv.eth-usd --no-alias
>> kamu list

## Explore (1:50)

>> kamu tail cryptocompare.ohlcv.eth-usd
>> kamu inspect schema cryptocompare.ohlcv.eth-usd
>> kamu sql --engine datafusion -c "select max(close) from 'cryptocompare.ohlcv.eth-usd'"
>> kamu notebook

## Root Datasets (2:30)

To understand how data enters the network let's create our own dataset

kubectl vibes

>> vim datasets/account.transactions.yaml
>> kamu add datasets/account.transactions.yaml
>> kamu pull account.transactions
>> notebook

## Ledger + Stream nature (1:30)

Reveal 1st secret

seed did

>> kamu log cryptocompare.ohlcv.eth-usd
>> kamu pull cryptocompare.ohlcv.eth-usd
>> kamu log cryptocompare.ohlcv.eth-usd

    Want orgs to share data in near-real-time data streams

## Derivative Datasets (3:40)

Root datasets is how you get data into the system
but now let's look at how you can process data

>> vim datasets/account.balance.yaml
>> vim datasets/account.market-value.usd.yaml

>> kamu add datasets/account.balance.yaml
>> kamu add datasets/account.market-value.usd.yaml
>> kamu pull account.balance
>> kamu pull account.market-value.usd

## Stream Processing (2:00)

Let's take a look at our pipline:

>> kamu ui

Derivative datasets are streams too:

>> kamu pull --recursive account.market-value.usd

    Cum-sum and other do absolute minimal incremental updates, don't recompute from scratch

Composability!!!!

>> show full pipeline

Only possible thanks to 3rd gen stream processing engines
    won't get into it, 
    but if batch processing is algebra - strem processing is like calculus - a superset which is a lot more powerful

## Collaboration & Trust (2:30)

Easy to share data (S3, IPFS)

>> kamu push -h

    Collab is P2P, but creating a central registry

To make collaboration possible we go at very great lenghts on verifiability, reproduciblity, and provenance

>> kamu verify cryptocompare.ohlcv.eth-usd
>> kamu verify account.balance

Trust is anchored in the publishers
    SQL smart contracts

On data processing side:
    Blurs the line bw on- off-chain data
    Blockchains satisfy all properties of ODF dataset

On data supply side:
    Can provide stronger trust guarantees than Oracles

## Summary

    IoT-volumes
    designed for near-real-time latencies
    strong verifiability and fine-grain provenance

## Working Group

Dataset structure
    Schemas for structured data
      e.g. 180Protocol

    Not just schemas but also other metadata
        licenses
        semantics
        stewardwhip and governance info

Data evolution
  dynamic data & low latency
  evolution of schema
    definition of compatibility

Compute runtime / sandboxing environment
    WASM is cool, but how do we bring 5 decades of evolution analytical data processing to it
        formats Apache Parquet & Arrow
        modern engines

Big picture
    going beyond one dataset 
        e.g. join
        associated query planning scheduling...

Privacy
