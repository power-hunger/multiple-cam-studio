import numpy as np
import json
from scipy.spatial import transform

CAM_SERIALS_N_DEGREES = {'950122060941': 0, '951422062948': -240, '951422060619': -120,
               '951422063135': -180, '950122060940': -60, '951422061191': -300}


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
    for cam_data in CAM_SERIALS_N_DEGREES:
        print("Rotating camera: " + cam_data + " by " + str(CAM_SERIALS_N_DEGREES[cam_data]) + " degrees")

        with open('data/' + cam_data + '.json') as f:
            json_data = json.load(f)

        rotated_json = []
        for frame in range(len(json_data)):
            dynamic_list = []
            for point in range(len(json_data[frame]["skeletons"][0])):
                x = json_data[frame]["skeletons"][0][point]["x"]
                y = json_data[frame]["skeletons"][0][point]["y"]
                z = json_data[frame]["skeletons"][0][point]["z"]
                x_rotated, y_rotated, z_rotated = rotate_point(x, y, z, CAM_SERIALS_N_DEGREES[cam_data])

                if "confidence" in json_data[frame]["skeletons"][0][point]:

                    dynamic_list.append({"confidence": json_data[frame]["skeletons"][0][point]["confidence"],
                                          "x": x_rotated,
                                          "y": y_rotated,
                                          "z": z_rotated})
                else:
                    dynamic_list.append({"confidence": -1.0,
                                          "x": x_rotated,
                                          "y": y_rotated,
                                          "z": z_rotated})

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