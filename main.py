import os
import cv2
from ultralytics import YOLO
from pose_utils import calculate_elbow_angles
from counter import shoulder_press_counter
from visualizer import draw_angle, draw_info_panel

# ============================================================
# MAIN
# ============================================================

def main():
    print("Loading YOLO Pose model...")

    model = YOLO("yolo26n-pose.pt")

#     # ========================================================
#     # KEYPOINT MAPPING
#     # ========================================================

    keypoints = {
        "LEFT_SHOULDER": 5,
        "RIGHT_SHOULDER": 6,
        "LEFT_ELBOW": 7,
        "RIGHT_ELBOW": 8,
        "LEFT_WRIST": 9,
        "RIGHT_WRIST": 10
    }

#     # ========================================================
#     # OPEN VIDEO
#     # ========================================================

    cap = cv2.VideoCapture("input/01.mp4")

    if not cap.isOpened():
        print("ERROR: Could not open video.")
        return

    # ========================================================
    # COUNTER VARIABLES
    # ========================================================

    counter = 0       # Stores the total number of completed shoulder presses.
    state = "DOWN"    # Sets the initial exercise state to DOWN.
    up_frames = 0     # Counts consecutive frames in which the UP angle condition is met.
    down_frames = 0   # Counts consecutive frames in which the DOWN angle condition is met.


    # ========================================================
    # COUNTER SETTINGS
    # ========================================================

    up_angle = 155       # The average elbow angle must be greater than 155° to detect the UP position.
    down_angle = 80      # The average elbow angle must be less than 80° to detect the DOWN position.
    stable_frames = 3    # Requires 3 consecutive frames to confirm the UP or DOWN position.

    # ========================================================
    # PROCESS VIDEO
    # ========================================================

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (1280, 720))

        # ====================================================
        # YOLO POSE
        # ====================================================

        results = model(frame, conf=0.5, verbose=False)

        # ====================================================
        # DEFAULT FRAME
        # ====================================================

        annotated_frame = frame

        # ====================================================
        # PERSON DETECTION
        # ====================================================

        if len(results) > 0:
            result = results[0]

            if result.keypoints is not None:

                # print(type(result.keypoints.xy))
                keypoints_xy = result.keypoints.xy.cpu().numpy()
                # print(type(keypoints_xy))
                # print(keypoints_xy)


                if len(keypoints_xy) > 0:
                    # ========================================
                    # FIRST PERSON
                    # ========================================

                    person = keypoints_xy[0]

                    # ========================================
                    # CALCULATE ANGLES
                    # ========================================

                    left_angle, right_angle, average_angle = calculate_elbow_angles(person, keypoints)

                    # ========================================
                    # UPDATE COUNTER
                    # ========================================

                    counter, state, up_frames, down_frames = shoulder_press_counter(average_angle, counter, state, up_frames, down_frames, up_angle, down_angle, stable_frames)

                    # ========================================Q
                    # YOLO POSE DRAWING
                    # ========================================

                    annotated_frame = result.plot()

                    # ========================================
                    # DRAW LEFT ANGLE
                    # ========================================

                    le = person[7]
                    draw_angle(annotated_frame, le, left_angle)

                    # ========================================
                    # DRAW RIGHT ANGLE
                    # ========================================

                    re = person[8]
                    draw_angle(annotated_frame, re, right_angle)

                    # ========================================
                    # INFORMATION PANEL
                    # ========================================

                    annotated_frame = draw_info_panel(annotated_frame, counter, state, average_angle)

        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow("AI Shoulder Press Counter", annotated_frame)
    

        # ====================================================
        # QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ========================================================
    # RELEASE
    # ========================================================

    cap.release()
    cv2.destroyAllWindows()

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 50)
    print("PROCESSING COMPLETE")
    print("=" * 50)
    print(f"Total Shoulder Presses: {counter}")
    print("=" * 50)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()