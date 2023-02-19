import sys
import netCDF4
import xarray
import csv

netcdf_bytes = sys.stdin.buffer.read()
nc4_ds = netCDF4.Dataset("input", memory=netcdf_bytes)
store = xarray.backends.NetCDF4DataStore(nc4_ds)
ds = xarray.open_dataset(store)

writer = csv.writer(sys.stdout)

for s in range(len(ds.stations)):
    id = ds.node_id[s].item().decode()
    name = ds.nodenames[s].item().decode()
    lat = ds.stations[s].lat.item()
    lon = ds.stations[s].lon.item()
    writer.writerow([id, name, lat, lon])
