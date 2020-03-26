from functools import reduce


def lvl_to_int(lvl_str) -> (int, int):
    """
        "4+1" -> (4, 1)
        "4" -> (4, 0)
    :param lvl_str: lvl parsed from soup
    :return: tuple of (current_level, levels_under_construction)
    """
    if '+' in lvl_str:
        base_lvl = int(lvl_str[0:lvl_str.find('+')])
        bonus_lvl = int(lvl_str[1 + lvl_str.find('+'):])
        return base_lvl, bonus_lvl
    else:
        return int(lvl_str), 0


def countdown_to_sec(txt) -> int:
    """
        "0:11:15" -> 675
    :param txt: countdown clock
    :return: time remaining in seconds
    """
    return reduce(lambda x, y: x * 60 + y, map(lambda x: int(x), txt.split(':')))


def comma_number_to_int(txt) -> int:
    """
        "29,394" -> 29394
    :param txt: number with commas
    :return: int version
    """
    return reduce(lambda x, y: x * 1000 + y, map(lambda x: int(x), txt.split(',')))
