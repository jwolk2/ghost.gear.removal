FIRST_QUESTION = "When should you start the mission to give the ROV the most time before currents increase?"
IN_BETWEEN = "In between low and high tide"
HOUR_BEFORE = "1 Hour before low or high tide"
RIGHT_AT = "Right at low or high tide"

SECOND_QUESTION = "What do you want to do first with the ROV?"
ATTACH_BUOYS = "First, attach the buoys to lift the net"
CUT_NET = "First, cut the net"

def video_path(selections: list[str]) -> str:
    assert len(selections) > 1, "At least two selections are required to determine the video path."

    if selections[0] == IN_BETWEEN and selections[1] == ATTACH_BUOYS:
        return "assets/videos/Attach buoys in between hig:low tide.mp4"
    elif selections[0] == IN_BETWEEN and selections[1] == CUT_NET:
        return "assets/videos/Cut net at high tide.mp4"
    elif selections[0] == HOUR_BEFORE and selections[1] == ATTACH_BUOYS:
        return "assets/videos/Attach buoys One hour before.mp4"
    elif selections[0] == HOUR_BEFORE and selections[1] == CUT_NET:
        return "assets/videos/Cut net one hour before.mp4"
    elif selections[0] == RIGHT_AT and selections[1] == ATTACH_BUOYS:
        return "assets/videos/Attach buoys at High:low tide.mp4"
    elif selections[0] == RIGHT_AT and selections[1] == CUT_NET:
        return "assets/videos/Cut net at high tide.mp4"
    else:
        raise ValueError("Invalid selection combination.")


