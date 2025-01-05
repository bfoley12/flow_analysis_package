import polars as pl
import numpy as np
from scipy.stats import entropy
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def transform(batch, func = "arcsinh", clip_negatives = True, inplace = False):
    if func == "arcsinh":
        batch.data = batch.data.with_columns([
                    batch.data.select(batch.fluorescent_markers).sum_horizontal().arcsinh().alias("total_fluorescence_arcsinh")
            ])
        batch.data = batch.data.with_columns([
                    pl.col(col).arcsinh() for col in batch.fluorescent_markers
                ])
    if clip_negatives:
        batch.data = batch.data.with_columns([
                    pl.col(col).clip(lower_bound=0) for col in batch.fluorescent_markers
                ])
    return batch

def calculate_debris(batch, method = "entropy", num_bins = 50, inplace = False):
    if method == "entropy":
        ent = _compute_entropy(batch.data.select(batch.fluorescent_markers), num_bins)
        return ent
    if method == "dbscan":
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(batch.data[batch.fluorescent_markers + ["FSC-A", "FSC-H", "SSC-A", "SSC-H"]])

        dbscan = DBSCAN(eps = 0.5, min_samples=10).fit(scaled_data)

        debris_indices = np.where(dbscan.labels_ == -1)[0]
    return -1

def _compute_entropy(batch, num_bins):
    batch.data = batch.data.with_columns(
            (pl.col(col) / pl.col("total_fluorescence_arcsinh")).alias(col)  # Overwrite original column
            for col in batch.fluorescent_markers
        )
    
    batch.data = batch.data.with_columns(
            pl.struct(batch.fluorescent_markers).map_elements(lambda row: entropy(np.array(list(row.values())))).alias("entropy")
        )
    return batch.data