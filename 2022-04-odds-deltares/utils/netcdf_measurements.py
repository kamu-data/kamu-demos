import sys
import netCDF4
import xarray

netcdf_bytes = sys.stdin.buffer.read()
nc4_ds = netCDF4.Dataset("input", memory=netcdf_bytes)
store = xarray.backends.NetCDF4DataStore(nc4_ds)
ds = xarray.open_dataset(store)

stations = ds.node_id.to_pandas().to_frame("station_id")
stations.station_id = stations.station_id.str.decode("utf-8")

pd = ds.waterlevel.to_pandas().reset_index().melt(id_vars=["time"], var_name="station", value_name="waterlevel")
pd["velocity"] = ds.velocity.to_pandas().reset_index().melt(id_vars=["time"], var_name="station", value_name="velocity").velocity
pd["discharge"] = ds.discharge.to_pandas().reset_index().melt(id_vars=["time"], var_name="station", value_name="discharge").discharge

pd = pd.join(stations, on="station")

pd.time = pd.time.dt.strftime("%Y-%m-%dT%H:%M:%S")
pd = pd.rename(columns={"time": "sim_time"})
pd["analysis_time"] = ds.analysis_time.dt.strftime("%Y-%m-%dT%H:%M:%S").item()

pd[["analysis_time", "sim_time", "station_id", "waterlevel", "velocity", "discharge"]].to_csv(sys.stdout, index=False, header=False)
