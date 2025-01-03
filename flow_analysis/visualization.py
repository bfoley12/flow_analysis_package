import matplotlib.pyplot as plt
import seaborn as sns

def plot_channel_spread(batch, group_by = "marker", return_fig = False):
    color_by = "sample"
    xlabel = "Marker"
    if group_by == "sample":
        color_by = "marker"
        xlabel = "Sample"
    batch_long = batch.data.melt(id_vars="sample", variable_name="marker", value_name="intensity")

    batch_long_pd = batch_long.to_pandas()

    # Create a grouped violin plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=batch_long_pd, x=group_by, y="intensity", hue=color_by, split=False, inner="quart", palette="muted", ax=ax)
    ax.set_title("Spread of Channels by Sample")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Value")
    
    if return_fig:
        return fig
    plt.show()