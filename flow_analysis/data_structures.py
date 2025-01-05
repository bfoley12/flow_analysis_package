from flowio import FlowData
import os
import numpy as np
import polars as pl
import copy

class FlowBatch:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = [FlowData(os.path.join(file_path, path)) for path in os.listdir(file_path)]
        self.metadata = self._extract_metadata()
        self.panel = self._extract_panel()
        self.data = self._extract_data()
        self.fluorescent_markers =  self.panel.filter(pl.col("fluorescent_channel") == 1)["marker"].to_list()

    def _extract_metadata(self):
        metadata_dict = {i: sample.text for i, sample in enumerate(self.file)}
        rows = [{"sample": outer_key, **inner_dict} for outer_key, inner_dict in metadata_dict.items()]

        return pl.DataFrame(rows)
    
    def _extract_panel(self):
        panel = {}
        keywords = ["Time", "FSC-H", "FSC-W", "FSC-A", "SSC-H", "SSC-W", "SSC-A", "SSC-B-H", "SSC-B-W", "SSC-B-A"]
        for index, channel in self.file[0].channels.items():
            if channel["PnN"] in keywords:
                panel[channel["PnN"]] = channel["PnN"]
            else:
                panel[channel["PnN"]] = channel["PnS"]
        panel = pl.DataFrame({
            "fluorophore": list(panel.keys()),
            "marker": list(panel.values())
        })

        panel = panel.with_columns(
            (pl.col("marker").is_in(keywords).not_()).cast(pl.Int8()).alias("fluorescent_channel")
        )
        return panel

    def _extract_data(self):
        ret_data =[]
        for i, sample in enumerate(self.file):
            data = pl.DataFrame(np.reshape(sample.events, (-1, sample.channel_count)))
            data = data.rename({old: new for old, new in zip(data.columns, self.panel["marker"])})
            data = data.with_columns(pl.lit(i).alias("sample"))
            ret_data.append(data)
        ret_data = pl.concat(ret_data)
        return ret_data
    
    def clone(self) -> "FlowBatch":
        """Creates a new FlowBatch instance with cloned attributes but reloaded FlowData objects."""
        cloned_instance = FlowBatch(self.file_path)  # Reload FlowData objects
        cloned_instance.metadata = self.metadata.clone()  # Clone Polars DataFrame
        cloned_instance.panel = self.panel.clone()
        cloned_instance.data = self.data.clone()
        cloned_instance.fluorescent_markers = self.fluorescent_markers.copy()  # Clone list

        return cloned_instance
    