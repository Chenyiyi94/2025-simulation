import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load data
file_path = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\spikes.csv'
v1_nodes = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\v1_nodes.csv'

# Read the first 10000 rows
data1 = pd.read_csv(file_path,nrows=10000, sep=' ')
nodes = pd.read_csv(v1_nodes, sep=' ')
print(nodes[0:20])

data1_sorted = data1.sort_values(by='timestamps', ascending=True)   # Sort the DataFrame by the 'timestamps' in ascending(升序) order
print(data1_sorted[0:20])

'''
# Temporarily set pandas to display all rows
with pd.option_context('display.max_rows', None):
    print(data1_sorted)

# Optional: Save the sorted DataFrame back to a CSV file if needed
output_file_path = '/Users/luyinyang/Downloads/Neuroscience/v1_biophysical/document/spikes1_sorted.csv'
data1_sorted.to_csv(output_file_path, index=False)
'''

# first 1000 entries (timestamps from 0 to 700 milliseconds)
data_plot = data1_sorted.head(1000)


fig = plt.figure()
start_p = 0
end_p = 0
location_dict = dict()
for i in range(len(nodes)):
    location_dict[nodes['id'][i]] = [nodes['x_soma'][i], nodes['y_soma'][i], nodes['z_soma'][i]]

color_dict=dict()
for i in range(len(nodes)):
    color_dict[nodes['id'][i]]=[nodes['ei'][i]][0]
for step in range(4):  # data from first 2000ms, take 400ms for each loop
    start_p=step*400+400
    end_p=start_p+400
    temp = []
    for i in range(len(data1_sorted)):
        t = data1_sorted['timestamps'][i]
        if t>start_p and t<end_p:
            temp.append([data1_sorted['timestamps'][i],data1_sorted['node_ids'][i]])
        elif t>=end_p:
            break
    # print(temp)

    #print([(key,location_dict[key]) for key in location_dict.keys()])

    location_list=[]
    for i in temp:
        location_list.append(location_dict[i[1]])
    location_list=np.array(location_list)


    # print([(key,color_dict[key]) for key in color_dict.keys()])
    color_list=[]
    for i in temp:
        if color_dict[i[1]]=='e':
            color_list.append('r')
        else:
            color_list.append('b')


    ax = fig.add_subplot(2,2,step+1, projection='3d')    # Plotting the 3D scatter plot

    # Use the columns you want to plot
    x = location_list[:,0]
    y = location_list[:,1]
    z = location_list[:,2]

    ax.scatter(x, y, z, marker='o',s=8,color=color_list)

    # Adding labels to the axes
    ax.set_xlabel('x_soma')
    ax.set_ylabel('y_soma')
    ax.set_zlabel('z_soma')
    ax.set_title(str(start_p)+'-'+str(end_p))

plt.tight_layout()
plt.show()