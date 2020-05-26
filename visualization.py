# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import json

CAM_SERIALS = [ '951422062948', '950122060940']

def generate_data(nbr_iterations, nbr_elements, cam_data):
    """
    Generates dummy data.
    The elements will be assigned random initial positions and speed.
    Args:
        nbr_iterations (int): Number of iterations data needs to be generated for.
        nbr_elements (int): Number of elements (or points) that will move.
    Returns:
        list: list of positions of elements. (Iterations x (# Elements x Dimensions))
    """
    dims = (3,1)

    # Random initial positions.
    gaussian_mean = np.zeros(dims)
    gaussian_std = np.ones(dims)
    start_positions = np.array(list(map(np.random.normal, gaussian_mean, gaussian_std, [nbr_elements] * dims[0]))).T

    # Random speed
    start_speed = np.array(list(map(np.random.normal, gaussian_mean, gaussian_std, [nbr_elements] * dims[0]))).T

    # Computing trajectory
    data = [start_positions]
    for iteration in range(nbr_iterations):
        previous_positions = data[-1]
        new_positions = previous_positions + start_speed
        data.append(new_positions)

    with open('results/' + cam_data + '_rotated.json') as f:
        json_data = json.load(f)

    data_list = []

    for frame in range(len(json_data)):
        dynamic_list = []
        for point in range(len(json_data[frame]['skeletons'][0])):
            dynamic_list.append([json_data[frame]['skeletons'][0][point]['x'],
                                 json_data[frame]['skeletons'][0][point]['y'],
                                 json_data[frame]['skeletons'][0][point]['z']])
        data_list.append(dynamic_list)


    new_list = []
    for index in range(len(data_list)):
        npa = np.asarray(data_list[index], dtype=np.float64)
        new_list.append(npa)
        print(data_list[index])


    return new_list

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

def main(data, cam_data, save=False):
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

    if save:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800, extra_args=['-vcodec', 'libx264'])
        ani.save(cam_data + '_rotated.mp4', writer=writer)

    plt.show()


for cam_data in CAM_SERIALS:
    print("Creating video for: " + cam_data)
    data = generate_data(2, 1, cam_data)
    main(data, cam_data, save=True)