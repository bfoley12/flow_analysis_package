from flow_analysis.data_structures import FlowBatch
import flow_analysis.visualization as viz
import flow_analysis.preprocessing as pp
import yaml
import polars as pl

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
test_data_path = config["test_data_path"]

fb = FlowBatch(test_data_path)
fb = pp.transform(fb)
fb.data = fb.data.with_columns((pl.col("FSC-A") / pl.col("SSC-A")).alias("FSC-SSC"))
pp.calculate_debris(fb, method = "dbscan")
viz.single_channel_spread(fb, "entropy")
fb.data = fb.data.filter(pl.col("FSC-SSC") < 500, pl.col("entropy") > 1.15)
viz.single_channel_spread(fb, "entropy")
#viz.channel_spread(fb)
print(fb)