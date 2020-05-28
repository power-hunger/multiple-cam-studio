import numpy as np
import json
from scipy.spatial import transform

CAM_SERIALS_N_CALIBRATION = {'950122060941': {'degrees': 0, 'x': 0, 'y': 0, 'z': 0},
                             '950122060940': {'degrees': -60.5, 'x': 1.30875, 'y': 2.4, 'z': -0.0218},
                             '951422060619': {'degrees': -124, 'x': 4.3875, 'y': 2.13125, 'z': -0.0625},
                             '951422063135': {'degrees': -180, 'x': 5.375, 'y': -0.0375, 'z': -0.0468750},
                             '951422062948': {'degrees': -236, 'x': 4.10625, 'y': -2.275, 'z': -0.05},
                             '951422061191': {'degrees': -298.875, 'x': 1.2218750, 'y': -2.1656250, 'z': 0.0125}}
START_TIME = 1589639952
END_TIME = 1589640274


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
    for cam_serial in CAM_SERIALS_N_CALIBRATION:
        cam_degrees = CAM_SERIALS_N_CALIBRATION[cam_serial]['degrees']
        cam_x = CAM_SERIALS_N_CALIBRATION[cam_serial]['x']
        cam_y = CAM_SERIALS_N_CALIBRATION[cam_serial]['y']
        cam_z = CAM_SERIALS_N_CALIBRATION[cam_serial]['z']

        print("Rotating camera: " + cam_serial + " by " +
              str(cam_degrees) + " degrees; " +
              str(cam_x) + " x points; " +
              str(cam_y) + " y points; " +
              str(cam_z) + " z points")

        with open('data/' + cam_serial + '.json') as f:
            json_data = json.load(f)

        rotated_json = []
        for frame in range(len(json_data)):
            dynamic_list = []
            for point in range(len(json_data[frame]["skeletons"][0])):
                x = json_data[frame]["skeletons"][0][point]["x"]
                y = json_data[frame]["skeletons"][0][point]["y"]
                z = json_data[frame]["skeletons"][0][point]["z"]
                x_rotated, y_rotated, z_rotated = rotate_point(x, y, z, cam_degrees)

                x_rot_n_sub = x_rotated + cam_y
                y_rot_n_sub = y_rotated + cam_z
                z_rot_n_sub = z_rotated + cam_x

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

        with open('results/' + cam_serial + '_rotated.json', 'w+') as the_file:
            the_file.write(json_dump)


def create_top_point_placeholder():
    empty_top_point_json = []
    for empty_frame in range(START_TIME, END_TIME):
        runner_list = []
        for empty_point in range(18):
            runner_list.append({"confidence": 0, "x": 0, "y": 0, "z": 0})

        empty_top_point_json.append({"skeletons": [runner_list], "timestamp": empty_frame})

    return empty_top_point_json


def pick_top_point():
    top_point_json = create_top_point_placeholder()

    for cam_serial in CAM_SERIALS_N_CALIBRATION:
        with open('results/' + cam_serial + '_rotated.json') as f:
            cam_points = json.load(f)

        top_point_frame = 0
        for time in range(START_TIME, END_TIME):

            for frame in range(len(cam_points)):

                if cam_points[frame]["timestamp"] == time:

                    for point in range(len(cam_points[frame]["skeletons"][0])):

                        if top_point_json[top_point_frame]["skeletons"][0][point]["confidence"] < cam_points[frame]["skeletons"][0][point]["confidence"]:
                            top_point_json[top_point_frame]["skeletons"][0][point]["confidence"] = cam_points[frame]["skeletons"][0][point]["confidence"]
                            top_point_json[top_point_frame]["skeletons"][0][point]["x"] = cam_points[frame]["skeletons"][0][point]["x"]
                            top_point_json[top_point_frame]["skeletons"][0][point]["y"] = cam_points[frame]["skeletons"][0][point]["y"]
                            top_point_json[top_point_frame]["skeletons"][0][point]["z"] = cam_points[frame]["skeletons"][0][point]["z"]
                    # check only first frame (1 FPS)
                    break

            top_point_frame = top_point_frame + 1

    json_dump = json.dumps(top_point_json)
    with open('results/top_point_json_1fps.json', 'w+') as the_file:
        the_file.write(json_dump)


def create_1_fps_data():
    for cam_serial in CAM_SERIALS_N_CALIBRATION:
        with open('results/' + cam_serial + '_rotated.json') as f:
            cam_points = json.load(f)
        top_point_json = create_top_point_placeholder()
        top_point_frame = 0
        for time in range(START_TIME, END_TIME):
            for frame in range(len(cam_points)):
                if cam_points[frame]["timestamp"] == time:
                    for point in range(len(cam_points[frame]["skeletons"][0])):
                        if top_point_json[top_point_frame]["skeletons"][0][point]["confidence"] < \
                                cam_points[frame]["skeletons"][0][point]["confidence"]:
                            top_point_json[top_point_frame]["skeletons"][0][point]["confidence"] = \
                            cam_points[frame]["skeletons"][0][point]["confidence"]
                            top_point_json[top_point_frame]["skeletons"][0][point]["x"] = \
                            cam_points[frame]["skeletons"][0][point]["x"]
                            top_point_json[top_point_frame]["skeletons"][0][point]["y"] = \
                            cam_points[frame]["skeletons"][0][point]["y"]
                            top_point_json[top_point_frame]["skeletons"][0][point]["z"] = \
                            cam_points[frame]["skeletons"][0][point]["z"]
                    # check only first frame (1 FPS)
                    break

            top_point_frame = top_point_frame + 1

        json_dump = json.dumps(top_point_json)
        with open('1fps_results/' + cam_serial + '_1fps.json', 'w+') as the_file:
            the_file.write(json_dump)


def get_conf(cam_points):
    conf_list = []
    for frame in range(len(cam_points)):
        for point in range(len(cam_points[frame]["skeletons"][0])):
            conf_list.append(cam_points[frame]["skeletons"][0][point]["confidence"])

    # removing first 90 sec because of setting up the env and not doing exercise
    conf_list = conf_list[1620:]
    return sum(conf_list) / len(conf_list)


def get_avg_conf_of_cams():

    avg_conf_list = []
    for cam_serial in CAM_SERIALS_N_CALIBRATION:
        with open('1fps_results/' + cam_serial + '_1fps.json') as f:
            cam_points = json.load(f)

        avg_conf = get_conf(cam_points)
        avg_conf_list.append(avg_conf)
        print("Camera with serial number: " + cam_serial + " avg confidence is: " + str(avg_conf))

    print("Single camera's avg conf is: " + str(sum(avg_conf_list)/len(avg_conf_list)))

    with open('1fps_results/top_point_json_1fps.json') as f:
        cam_points = json.load(f)
    print("All camera avg conf is: " + str(get_conf(cam_points)))


def main():
    # rotate_cam()
    # pick_top_point()
    # create_1_fps_data()
    get_avg_conf_of_cams()




if __name__ == "__main__":
    main()