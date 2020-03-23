def upgrade_building(credentials, village, location_id):
    page = 'village1.php' if location_id <= 18 else 'village2.php'
    old_building = village.buildings[location_id]
    old_k = village.k

    soup = credentials.call(page=page, params={'vid': village.vid, 'id': location_id, 'k': village.k})
    village.update_from_soup(soup)
    new_building = village.buildings[location_id]

    if village.k == old_k:
        village.k = ""

    if old_building.lvl + old_building.plus_lvl == new_building.lvl + new_building.plus_lvl:
        return False
    return True


# demo does not use K
def demolish_building(credentials, village, location_id):
    credentials.call(page='build.php', params={'id': 26}, data={'drbid': location_id, 'ok.x': 0, 'ok.y': 0})

    # get demo finish time here
    return True
