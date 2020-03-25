import village_center as center


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


def construct_building(credentials, village, location_id, building):
    # TODO(@alexvelea) Rethink this for granary/warehouse
    # Check if building is already constructed
    if len(village.center.find(building)):
        raise Exception

    # Make sure the spot it's empty
    if village.buildings[location_id].building.name != center.Buildings.empty.name:
        raise Exception

    soup = credentials.call(page='village2.php',
                            params={'vid': village.vid, 'id': location_id, 'b': building.id, 'k': village.k})
    village.update_from_soup(soup)
    new_building = village.buildings[location_id]

    if new_building.plus_lvl == 1 and new_building.lvl == 0:
        return True
    return False


# demo does not use K
def demolish_building(credentials, village, location_id):
    main_building = next(iter(village.center.find(center.Buildings.mainB)), None)
    if main_building is None:
        raise Exception

    if main_building.lvl < 10:
        raise Exception

    credentials.call(page='build.php', params={'id': main_building.location_id}, data={'drbid': location_id, 'ok.x': 0, 'ok.y': 0})

    # get demo finish time here
    return True
