import sys
import lasio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.widgets import TextBox

# Get arguments from command line
# 1: list of las file paths
# 2: csv file containing well UID and curve mnemonic list (curve tables extracted using previous steps)
# 3: the well UID selected to be plotted

las_list_fn = sys.argv[1]
curve_table_fn = sys.argv[2]
uid = sys.argv[3]

print("List of las file paths: %s" %las_list_fn)
print("Curve table file name: %s" %curve_table_fn)
print("Selected well UID: %s" %uid)
print("")

# find las file corresponding to UID
f = open(las_list_fn,'r')
input_fn = ''
for line in f:
    if line.find(uid) > -1:
        input_fn = line.strip()
        break
f.close()
if input_fn:
    print("Input LAS file: %s" %input_fn)
else:
    print("Error! No las file found corresponding to uid %s in %s!" %(uid,las_list_fn))
    sys.exit(666)

# find list of curve mnemonics for this uid
f = open(curve_table_fn,'r')
curve_list = []
for line in f:
    if line.find(uid) > -1:
        curve_list = line.strip().split(',')[1:]
        break
n_curves = len(curve_list)
if n_curves > 0:
    print("List of well curves to be plotted:")
    print(curve_list)
else:
    print("Error! No curve list found for uid %s in %s!" %(uid,curve_table_fn))
    sys.exit(666)
    
# Read las file
lf = lasio.read(input_fn)

# Plot selected curves as subplot vertically
# Borrowing from Saurabh's demo script, as I don't want to reverse engineer everything
fig, ax = plt.subplots(nrows=1, ncols=n_curves,figsize=(5,6), sharey= True)
if n_curves < 2:
    ax2 = []
    ax2.append(ax)
    ax = ax2 # make sure it's a list.
fig.suptitle('Well %s' %uid,size=16,weight='bold')
plt.subplots_adjust(bottom=0.1)

# Set up depth axis and default min/max for gammaray coloring
depth = lf.index
z_min = depth.min()
z_max = depth.max()
z_range = z_max - z_min
cmap_min = 40.0
cmap_max = 150.0

# Set up section start and end depth input field
section_start = z_min
section_end = z_max
ax[0].set_ylim(section_end,section_start) # reversed, full range by default
ax_ss = plt.axes([0.25, 0, 0.2, 0.05])
tb_ss = TextBox(ax_ss, 'Plot Start Depth: ', initial=str(section_start))
def onTBSSSubmit(text):
    global section_start, section_end
    try:
        section_start = float(text)
        if section_start < z_min:
            section_start = z_min # snap to min
        if section_start > (section_end - 1):
            section_start = section_end - 1 # snap to just before end
        tb_ss.set_val(str(section_start))
        ax[0].set_ylim(section_end,section_start)
        plt.draw()
    except: # something not numeric
        tb_ss.set_val(str(section_start))
        pass
tb_ss.on_submit(onTBSSSubmit)

ax_se = plt.axes([0.75, 0, 0.2, 0.05])
tb_se = TextBox(ax_se, 'Plot End Depth: ', initial=str(section_end))
def onTBSESubmit(text):
    global section_start, section_end
    try:
        section_end = float(text)
        if section_end > z_max:
            section_end = z_max # snap to max
        if section_end < (section_start + 1):
            section_end = section_start + 1 # snap to just after start
        tb_se.set_val(str(section_end))
        ax[0].set_ylim(section_end,section_start)
        plt.draw()
    except: # something not numeric
        tb_se.set_val(str(section_end))
        pass
tb_se.on_submit(onTBSESubmit)




for j in range(0,n_curves):
    curve = curve_list[j]
    d = lf[curve]
    maxval = d[~np.isnan(d)].max()
    
    ax[j].imshow(d.reshape(d.shape[0],1),
          aspect='auto',
          origin='lower',
          cmap=colormaps['viridis'].reversed(),  # coloring GR in reverse: yellow is low, blue is high
          vmin=cmap_min,
          vmax=cmap_max,
          extent=(0.0, maxval, depth.min(), depth.max()))
    ax[j].fill_betweenx(depth,x2=0.0,x1=d,facecolor='white',alpha=1.0)
    ax[j].plot(d, depth, '-', color= 'black')
    ax[j].set_title(curve,weight='bold')
    

plt.show()


