import numpy as np

from bannerman.reports import tts_estimate_v_actual as tts
from bokeh.plotting import figure, show, output_file

import colorcet as cc

# Load the Iris Data Set
tts_df = tts.build_tts_estimate_v_actual_report()
colors = cc.inferno

print(len(colors))
x = 'StoryEstimate_pts'
y = 'ActualHoursPerPoint'

unique_projects = list(tts_df['ProjectName'].unique())
color_mappings = zip(
    unique_projects,
    [colors[round(((i)*256)/len(unique_projects))] for i in range(len(unique_projects))]
)

TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,reset,box_select,poly_select"
plot = figure(tools=TOOLS)

for project, color in color_mappings:
    plot.scatter(
        x = tts_df[tts_df['ProjectName']==project][x],
        y = tts_df[tts_df['ProjectName']==project][y],
        fill_color = color,
        fill_alpha = 0.6,
        size=20,
        line_color = None
    )

plot2 = figure()
plot2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color='#009E60')
show(plot2)
