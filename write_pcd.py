import numpy as np
import os 

def write_pcd_file(file_path, point_cloud):
    header = (
        "VERSION .7\n"
        "FIELDS x y z intensity\n"
        "SIZE 4 4 4 4\n"
        "TYPE F F F F\n"
        "COUNT 1 1 1 1\n"
        "WIDTH " + str(point_cloud.shape[0]) + "\n"
        "HEIGHT 1\n"
        "VIEWPOINT 0 0 0 1 0 0 0\n"
        "POINTS " + str(point_cloud.shape[0]) + "\n"
        "DATA ascii\n"
    )
    np.savetxt(file_path, point_cloud, fmt="%.6f", delimiter=" ", header=header)
    print(f"Saved point cloud as {file_path}")
    
    
def create_output_file_with_area(input_file, output_folder, area):
    # Extract the directory path from the input file
    directory = os.path.dirname(input_file)
    # Extract the filename from the input file path
    filename = os.path.basename(input_file)
    # Remove the existing extension from the filename
    filename_without_extension = os.path.splitext(filename)[0]
    # Construct the new filename with the area variable
    new_filename = f"{filename_without_extension}_{area}.csv"
    # Construct the output file path
    output_file = os.path.join(output_folder, new_filename)
    return output_file