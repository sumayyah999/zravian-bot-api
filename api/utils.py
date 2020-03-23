def lvl_to_int(lvl_str):
    if '+' in lvl_str:
        base_lvl = int(lvl_str[0:lvl_str.find('+')])
        bonus_lvl = int(lvl_str[1 + lvl_str.find('+'):])
        return base_lvl, bonus_lvl
    else:
        return int(lvl_str), 0
