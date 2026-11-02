def shoulder_press_counter(
    average_angle,
    counter,
    state,
    up_frames,
    down_frames,
    up_angle,
    down_angle,
    stable_frames
):

    # --------------------------------------------------------
    # ARMS EXTENDED
    # --------------------------------------------------------

    if average_angle > up_angle:

        # Count how many consecutive frames show
        # that the arms are in the UP/EXTENDED position.
        #
        # Example:
        # up_angle = 155
        # stable_frames = 3
        #
        # Frame 1 -> angle = 160 -> up_frames = 1
        # Frame 2 -> angle = 162 -> up_frames = 2
        # Frame 3 -> angle = 165 -> up_frames = 3
        #
        # After 3 consecutive frames above 155 degrees,
        # the UP position is confirmed.

        up_frames += 1
        down_frames = 0


    # --------------------------------------------------------
    # ARMS LOWERED
    # --------------------------------------------------------

    elif average_angle < down_angle:

        # Count how many consecutive frames show
        # that the arms are in the DOWN/LOWERED position.
        #
        # Example:
        # down_angle = 80
        # stable_frames = 3
        #
        # Frame 1 -> angle = 75 -> down_frames = 1
        # Frame 2 -> angle = 70 -> down_frames = 2
        # Frame 3 -> angle = 65 -> down_frames = 3
        #
        # After 3 consecutive frames below 80 degrees,
        # the DOWN position is confirmed.
        #
        # This means the person has lowered their arms
        # enough to reach the required DOWN position.

        down_frames += 1
        up_frames = 0


    # --------------------------------------------------------
    # MIDDLE POSITION
    # --------------------------------------------------------

    else:

        # The elbow angle is between 80 and 155 degrees.
        #
        # Example:
        # angle = 100 degrees
        #
        # The arms are neither in the confirmed UP range
        # nor in the confirmed DOWN range.
        #
        # Reset both counters because the required position
        # has not been detected in this frame.

        up_frames = 0
        down_frames = 0


    # --------------------------------------------------------
    # DOWN -> UP
    # --------------------------------------------------------

    if state == "DOWN" and up_frames >= stable_frames:

        # The elbow angle has remained above 155 degrees
        # for at least 3 consecutive frames.
        #
        # Example:
        # up_frames = 3
        # stable_frames = 3
        #
        # 3 >= 3 -> UP position is confirmed.
        #
        # The person has extended their arms overhead,
        # so we change the state from DOWN to UP.

        state = "UP"


    # --------------------------------------------------------
    # UP -> DOWN
    # --------------------------------------------------------

    elif state == "UP" and down_frames >= stable_frames:

        # The elbow angle has remained below 80 degrees
        # for at least 3 consecutive frames.
        #
        # Example:
        # down_frames = 3
        # stable_frames = 3
        #
        # 3 >= 3 -> DOWN position is confirmed.
        #
        # The person has lowered their arms back to the
        # required DOWN position after pressing overhead.
        #
        # One complete shoulder press is now counted:
        #
        # DOWN → 3 stable UP frames → 3 stable DOWN frames → +1 repetition.

        counter += 1
        state = "DOWN"

        print(f"Shoulder Press: {counter}")


    return counter, state, up_frames, down_frames





# Example:
# The actual arm is still UP, but the pose model may give:
#
# 160° → 158° → 79° → 157° → 160° -> 75°(actual)
#                  ↑
#            Detection error
#
# If we count immediately at 79°, we may count a wrong repetition.
#
# So we wait for 3 consecutive DOWN frames:
#
# 79° → 75° → 72°
#
# Now we are more confident that the person is really DOWN. রংগিলা ভাবি