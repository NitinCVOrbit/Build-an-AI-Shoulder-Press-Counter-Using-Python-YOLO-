import cv2
import numpy as np


# ============================================================
# CALCULATE ANGLE ----- Dot Product Method (Vector Method)
# ============================================================

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    denominator = (
        np.linalg.norm(ba) *
        np.linalg.norm(bc)
        + 1e-7
    )

    cosine_angle = np.dot(ba, bc) / denominator

    cosine_angle = np.clip(
        cosine_angle,
        -1.0,
        1.0
    )

    angle = np.degrees(
        np.arccos(cosine_angle)
    )

    return angle


# ============================================================
# CALCULATE BOTH ELBOW ANGLES
# ============================================================

def calculate_elbow_angles(person, keypoints):

    ls = person[keypoints["LEFT_SHOULDER"]]
    rs = person[keypoints["RIGHT_SHOULDER"]]

    le = person[keypoints["LEFT_ELBOW"]]
    re = person[keypoints["RIGHT_ELBOW"]]

    lw = person[keypoints["LEFT_WRIST"]]
    rw = person[keypoints["RIGHT_WRIST"]]

    # print(ls)
    # print(rs)

    left_angle = calculate_angle(
        ls,
        le,
        lw
    )

    right_angle = calculate_angle(
        rs,
        re,
        rw
    )

    average_angle = (
        left_angle + right_angle
    ) / 2

    return left_angle, right_angle, average_angle

# Calculate the average of both elbow angles.
# Both arms move together during a shoulder press,
# so we use one angle to represent both arms.
#
# Example:
# Left  = 150 degrees
# Right = 154 degrees
# Average = (150 + 154) / 2 = 152 degrees
#
# The average also reduces small differences caused
# by pose detection.

