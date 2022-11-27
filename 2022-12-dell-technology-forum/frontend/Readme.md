Hi, for the analysis of goals heatmaps we need the carball package.

Normally, we install it through
```
pip install carball
```

However, one requirement has not been updates: boxcars-py(will not work with newer replays)
but more importantly, numpy cant be compiled(apparently)

So, i had to compile from source

in this case, we install all modules like so:
```
pip install carball --no-deps

pip install boxcars_py-0.1.15-cp310-cp310-manylinux1_x86_64.whl

pip install protobuf==3.19 xlrd==1.1.0 openpyxl
```