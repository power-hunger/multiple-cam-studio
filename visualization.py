# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import json

CAM_SERIALS = ['950122060941']
#LIMB_KEY_POINTS = {{1, 2}, {1, 5}, {2, 3}, {3, 4}, {5, 6}, {6, 7}, {1, 8}, {8, 9}, {9, 10}, {1, 11}, {11, 12}, {12, 13}, {1, 0}, {0, 14}, {14, 16}, {0, 15}, {15, 17}};


def generate_data(cam_serial):

    with open('top_point_json.json') as f:
        json_data = json.load(f)

    data_list = []

    for frame in range(len(json_data)):
        dynamic_list = []
        for point in range(len(json_data[frame]['skeletons'][0])):
            dynamic_list.append([json_data[frame]['skeletons'][0][point]['x'],
                                 json_data[frame]['skeletons'][0][point]['y'],
                                 json_data[frame]['skeletons'][0][point]['z']])
        data_list.append(dynamic_list)

    data_list_array = []
    for index in range(len(data_list)):
        npa = np.asarray(data_list[index], dtype=np.float64)
        data_list_array.append(npa)
        print(data_list[index])

    return data_list_array


def animate_scatters(iteration, data, scatters):
    """
    Update the data held by the scatter plot and therefore animates it.
    Args:
        iteration (int): Current iteration of the animation
        data (list): List of the data positions at each iteration.
        scatters (list): List of all the scatters (One per element)
    Returns:
        list: List of scatters (One per element) with new coordinates
    """
    for i in range(data[0].shape[0]):
        scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])

    return scatters


def main(data, cam_serial):
    """
    Creates the 3D figure and animates it with the input data.
    Args:
        data (list): List of the data positions at each iteration.
        save (bool): Whether to save the recording of the animation. (Default to False).
    """

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # Initialize scatters
    scatters = [ax.scatter(data[0][i, 0:1], data[0][i, 1:2], data[0][i, 2:], s=5) for i in range(data[0].shape[0])]

    # Number of iterations
    print(data)
    iterations = len(data)

    # Setting the axes properties
    ax.set_xlim3d([-1.5, 1.5])
    ax.set_xlabel('X')

    ax.set_ylim3d([-1.5, 1.5])
    ax.set_ylabel('Y')

    ax.set_zlim3d([1.6, 3.6])
    ax.set_zlabel('Z')

    ax.set_title('3D Animated Scatter Example')

    # Provide starting angle for the view.
    ax.view_init(100, 90)

    ani = animation.FuncAnimation(fig, animate_scatters, iterations, fargs=(data, scatters),
                                       interval=50, blit=False, repeat=True)

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800, extra_args=['-vcodec', 'libx264'])
    ani.save('videos/top_test.mp4', writer=writer)

    plt.show()


for cam_serial in CAM_SERIALS:
    print("Creating video for: " + cam_serial)
    data = generate_data(cam_serial)
    main(data, cam_serial)
