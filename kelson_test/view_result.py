import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
rcParams['figure.figsize'] = 20, 10
import pandas as pd

full_df = pd.read_csv("/home/oliver/Desktop/kelson/MoorDyn-dev/kelson_test/specifications/line_Line1.out", 
                      sep = "\t", 
                      dtype= str)

#cleaning up the names of columns:
rename_dict = {c:c.replace(" ", "") for c in full_df.columns}
full_df = full_df.rename(rename_dict)
columns = [c.replace(" ", "") for c in full_df.columns if "Time" not in c]
columns = [c for c in columns if len(c)>1]
 
#now finding the number of segments:
segments = list({int(("").join(c.split("Node")).split("p")[0]) for c in columns if "Seg" not in c})

counter = 0
tension = full_df[" Seg1Te "]
step = 1500

for i in full_df.index[3::step]:
    counter = counter + 1
    temp_series = full_df.iloc[i]
    segment_timestamp = []
    temp_tension = tension[3:i:step].apply(float).to_numpy()
    
    for s in segments:
        x = float(temp_series[" Node{}px ".format(s)].replace(" ", ""))
        y = float(temp_series[" Node{}pz ".format(s)].replace(" ", ""))
        #z = temp_series[" Node{}pz ".format(s)]
        segment_timestamp.append([x, y])
        
    fig, (ax1, ax2) = plt.subplots(1, 2)

    segment_timestamp = np.array(segment_timestamp)
    
    ax1.scatter([10], [20], marker = "^", s = 40, c = "r")
    ax1.plot(segment_timestamp[:, 0], segment_timestamp[:, 1], linewidth = 7)
    ax1.grid(True)
    
    ax1.set_xlim(6, 22.5)
    ax1.set_ylim(6, 22.5)
    ax1.set_title("t = {} (s)".format(full_df["Time"][i]))
    ax1.set(xlabel = "(m)", ylabel = "(m)")
    
    ax2.plot(full_df.loc[3:i-1:step, "Time"].apply(float).to_numpy(),
             temp_tension, linewidth = 5)
    ax2.grid(True)
    ax2.set_title("Tension At Anchor")
    ax2.set(xlabel = "time (s)", ylabel = "(N)")
    #plt.savefig("/home/oliver/Desktop/kelson/MoorDyn-dev/kelson_test/output_images/img{}.png".format("0"*(10-len(str(counter)))+str(counter)))
    
    
    plt.show()
    
    

    