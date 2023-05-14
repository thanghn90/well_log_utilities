import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Input csv file name, chosen well UID of interest, and search radius
chosen_uid = sys.argv[1]
xy_fn = sys.argv[2]
radius = float(sys.argv[3])

df = pd.read_csv(xy_fn,dtype={'UID':'string', 'X':np.float32, 'Y': np.float32}) # read entire csv to pandas dataframe

# Find wells that fall within a radius of a chosen well UID
chosen_row = df[df['UID']==chosen_uid]
chosen_x = chosen_row['X'].to_numpy()
chosen_y = chosen_row['Y'].to_numpy()
r2 = radius**2
df['d2'] = (df['X']-chosen_x)**2 + (df['Y']-chosen_y)**2
nearby_fn = f"well_near_{chosen_uid}.csv"
df_nearby = df[df['d2'] < r2]
df_nearby['UID'].to_csv(nearby_fn,index=False,header=False)


# Following https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot
# To add hover text to a data point. Not very responsive, but works.
# Much faster than plotly go.Scatter
fig = plt.figure()
ax = fig.add_subplot(111)
main_plot = ax.scatter(x=df_nearby['X'], y=df_nearby['Y'])
main_annot = ax.annotate(
    "",
    xy=(0,0),
    xytext=(5,5),
    textcoords='offset points', # text position by offset
)
main_annot.set_visible(False)
# For the highlighted point, simply plot a point over it.
ax.scatter(x=chosen_x, y=chosen_y, color='yellow')
ax.annotate(
    chosen_uid,
    xy=(chosen_x,chosen_y),
    xytext=(10, 10),
    textcoords='offset points',
    bbox=dict(boxstyle="square", fc='#FFFFFF00'),
    arrowprops=dict(arrowstyle="->"),
)
ax.set_xlim((chosen_x-radius,chosen_x+radius))
ax.set_ylim((chosen_y-radius,chosen_y+radius))
ax.set_aspect(1.0)


def update_annot(ind):
    global df, main_plot, main_annot, text
    pos = main_plot.get_offsets()[ind["ind"][0]]
    main_annot.xy = pos
    text = f"{df['UID'].iloc[ind['ind']].to_string(index=False)}" # Well UID hover text
    main_annot.set_text(text)
    
def hover(event):
    global main_annot, main_plot
    vis = main_annot.get_visible()
    if event.inaxes == ax:
        cont, ind = main_plot.contains(event)
        if cont:
            update_annot(ind)
            main_annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                main_annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
