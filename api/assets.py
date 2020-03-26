class BuildingType:
    # TODO(@alexvelea) Add some more info, such as
    # - capital only
    # - max level
    # - multiple build? (for granary, warehouse)
    # - requirements?

    def __init__(self, name=None, bid=None, whole_object=None):
        if whole_object is None:
            self.name = name
            self.bid = bid
        else:
            self.__dict__.update(whole_object.__dict__)

    def __str__(self):
        return self.name


# TODO(@alexvelea) Add The rest of the buildings extended Rax, Palace, wall as well as race-specific buildings
# Collection of all building types as well as various info for API calls
class Building:
    empty = BuildingType('Empty place', 0)

    # Overview Resources
    wood = BuildingType('Woodcutter', 1)
    clay = BuildingType('Clay Pit', 2)
    iron = BuildingType('Iron Mine', 3)
    crop = BuildingType('Cropland', 4)

    # Economy Infrastructure
    mainB = BuildingType('Main Building', 15)
    granary = BuildingType('Granary', 11)
    warehouse = BuildingType('Warehouse', 10)
    marketplace = BuildingType('Marketplace', 17)
    cranny = BuildingType('Cranny', 23)

    # Military
    barracks = BuildingType('Barracks', 19)
    stable = BuildingType('Stable', 20)
    siege = BuildingType('Siege Workshop', 21)
    rally = BuildingType('Rally Point', 16)

    # Military infrastructure
    academy = BuildingType('Academy', 22)
    armoury = BuildingType('Armoury', 13)
    blacksmith = BuildingType('Blacksmith', 12)

    # Expansion
    residence = BuildingType('Residence', 25)
    hall = BuildingType('Town Hall', 24)

    # Resources
    bonusWood = BuildingType('Sawmill', 5)
    bonusClay = BuildingType('Brickworks', 6)
    bonusIron = BuildingType('Iron Foundry', 7)
    bonusCrop1 = BuildingType('Flour Mill', 8)
    bonusCrop2 = BuildingType('Bakery', 9)

    all = [
        empty,
        wood, clay, iron, crop,
        mainB, granary, warehouse, marketplace, cranny,
        barracks, stable, siege, rally,
        academy, armoury, blacksmith,
        residence, hall,
        bonusWood, bonusClay, bonusIron, bonusCrop1, bonusCrop2
    ]

    @classmethod
    def get_by_name(cls, building_name):
        building = next(filter(lambda x: x.name == building_name, cls.all), None)
        if building is None:
            print("Can't find building: ", building_name)
            raise Exception
        return building
