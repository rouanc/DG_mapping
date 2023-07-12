from Transformation import *


def homogeneousForm(RotationMatrix, TransVector):
    """ target: Rigid3D Lidar to mapping frame
        input: Rotation matrix , translation vector, consider all of them
        output: Homogeneous Matrix
    """
    
    # a stands for (0, 0, 0) add on the bottom of the Rotation matrix
    a = np.concatenate((RotationMatrix, np.zeros((1, 3))), axis=0)
    # b stands for (1) add on the bottom of translation vector
    b = np.concatenate((TransVector, np.ones((1,1)) ), axis=0)
    # Combine a and b => becoming a 4*4 matrix
    Transformation= np.concatenate((a, b), axis=1)
    return Transformation