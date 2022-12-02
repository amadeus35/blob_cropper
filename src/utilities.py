def AppMsg(msg):
    """
    Prints a formated application message
    """
    print(f"[CROPPER]: {msg}")


def findRange(num_list: list):
    if len(num_list) == 0:
        return None
    elif len(num_list) == 1:
        return (num_list[0], num_list[0])
    else:
        min_val = min(num_list)
        max_val = max(num_list)
        return (min_val, max_val)
