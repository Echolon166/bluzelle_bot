def human_format(num):
    """Format number to get the human readable presentation of it.

    Args:
        num (int): Number to be formatted

    Returns:
        str: Human readable presentation of the number.
    """

    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."), ["", "k", "m", "b", "t"][magnitude]
    )
