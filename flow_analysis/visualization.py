import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl

def channel_spread(batch, group_by = "marker", return_fig = False):
    color_by = "sample"
    xlabel = "Marker"
    if group_by == "sample":
        color_by = "marker"
        xlabel = "Sample"

    fluorescent_data = batch.data.select(batch.fluorescent_markers + ["sample"])
    fluorescent_long = fluorescent_data.melt(id_vars="sample", variable_name="marker", value_name="intensity")
    fluorescent_long_pd = fluorescent_long.to_pandas()

    characteristic_data = batch.data.drop(batch.fluorescent_markers)
    characteristic_long = characteristic_data.melt(id_vars="sample", variable_name="marker", value_name="intensity")
    characteristic_long_pd = characteristic_long.to_pandas()

    # Create a grouped violin plots
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 8))
    sns.violinplot(data=fluorescent_long_pd, x=group_by, y="intensity", hue=color_by, split=False, inner="quart", palette="muted", ax=axes[0])
    axes[0].set_title("Spread of Channels by Sample")
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel("Value")

    sns.boxplot(data=characteristic_long_pd, x=group_by, y="intensity", hue=color_by, palette="muted", ax=axes[1])
    axes[1].set_title("Spread of Channels by Sample")
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel("Value")
    
    if return_fig:
        return fig
    plt.show()

def single_channel_spread(batch, channel, return_fig = False):
    channel_data = batch.data.select([channel] + ["sample"])
    channel_long = channel_data.melt(id_vars="sample", variable_name="marker", value_name="intensity")
    channel_long_pd = channel_long.to_pandas()

    fig, ax = plt.subplots(figsize=(6, 8))
    sns.violinplot(data = channel_long_pd, x = "sample", y = "intensity", hue = "sample", palette = "muted", ax = ax)

    if return_fig:
        return fig
    plt.show()