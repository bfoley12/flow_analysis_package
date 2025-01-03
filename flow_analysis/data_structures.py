from flowio import FlowData
import os
import numpy as np
import polars as pl

class FlowBatch:
    def __init__(self, file_path):
        self.file = [FlowData(os.path.join(file_path, path)) for path in os.listdir(file_path)]
        self.metadata = self._extract_metadata()
        self.panel = self._extract_panel()
        self.data = self._extract_data()

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
    
    