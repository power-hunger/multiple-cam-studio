import numpy as np
import json
from scipy.spatial import transform

CAM_SERIALS_N_CALIBRATION = {'950122060941': {'degrees': 0, 'x': 0, 'y': 0, 'z': 0},
                             '950122060940': {'degrees': -60.5, 'x': 1.30875, 'y': 2.4, 'z': -0.0218},
                             '951422060619': {'degrees': -124, 'x': 4.3875, 'y': 2.13125, 'z': -0.0625},
                             '951422063135': {'degrees': -180, 'x': 5.375, 'y': -0.0375, 'z': -0.0468750},
                             '951422062948': {'degrees': -236, 'x': 4.10625, 'y': -2.275, 'z': -0.05},
                             '951422061191': {'degrees': -298.875, 'x': 1.2218750, 'y': -2.1656250, 'z': 0.0125}}


def rotate_point(x, y, z, degrees):
    vec = [x,y,z]

    rotation_degrees = degrees
    rotation_radians = np.radians(rotation_degrees)
    rotation_axis = np.array([0, 1, 0])

    rotation_vector = rotation_radians * rotation_axis
    rotation = transform.Rotation.from_rotvec(rotation_vector)
    rotated_vec = rotation.apply(vec)

    return rotated_vec[0], rotated_vec[1], rotated_vec[2]


def rotate_cam():
    for cam_data in CAM_SERIALS_N_CALIBRATION:
        cam_degrees = CAM_SERIALS_N_CALIBRATION[cam_data]['degrees']
        cam_x = CAM_SERIALS_N_CALIBRATION[cam_data]['x']
        cam_y = CAM_SERIALS_N_CALIBRATION[cam_data]['y']
        cam_z = CAM_SERIALS_N_CALIBRATION[cam_data]['z']

        print("Rotating camera: " + cam_data + " by " +
              str(cam_degrees) + " degrees; " +
              str(cam_x) + " x points; " +
              str(cam_y) + " y points; " +
              str(cam_z) + " z points")

        with open('data/' + cam_data + '.json') as f:
            json_data = json.load(f)

        rotated_json = []
        for frame in range(len(json_data)):
            dynamic_list = []
            for point in range(len(json_data[frame]["skeletons"][0])):
                x = json_data[frame]["skeletons"][0][point]["x"]
                y = json_data[frame]["skeletons"][0][point]["y"]
                z = json_data[frame]["skeletons"][0][point]["z"]
                x_rotated, y_rotated, z_rotated = rotate_point(x, y, z, cam_degrees)

                x_rot_n_sub = x_rotated + cam_x
                y_rot_n_sub = y_rotated + cam_y
                z_rot_n_sub = z_rotated + cam_z

                if "confidence" in json_data[frame]["skeletons"][0][point]:

                    dynamic_list.append({"confidence": json_data[frame]["skeletons"][0][point]["confidence"],
                                          "x": x_rot_n_sub,
                                          "y": y_rot_n_sub,
                                          "z": z_rot_n_sub})
                else:
                    dynamic_list.append({"confidence": -1.0,
                                          "x": x_rot_n_sub,
                                          "y": y_rot_n_sub,
                                          "z": z_rot_n_sub})

            rotated_json.append({"skeletons": [dynamic_list], "timestamp": json_data[frame]["timestamp"]})

        json_dump = json.dumps(rotated_json)

        with open('results/' + cam_data + '_rotated.json', 'w+') as the_file:
            the_file.write(json_dump)


def pick_top_point():
    print("f")



def main():
    rotate_cam()
    # pick_top_point()


if __name__ == "__main__":
    main()