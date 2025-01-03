from flow_analysis.data_structures import FlowBatch
import flow_analysis.visualization as viz

fb = FlowBatch("C:/Users/brend/OneDrive - Johns Hopkins/Hybrid Thymus/Data Analysis/TEC/2022-07-21 TEC enrichment + F1 characterization/Group_001")

viz.plot_channel_spread(fb)
print(fb)