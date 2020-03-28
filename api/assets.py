import copy


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
    # TODO(@alexvelea) Fix this is ids
    tournament_square = BuildingType('Tournament Square', -1)
    horse_upkeep = BuildingType('Horse Drinking Pool', -1)

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
        barracks, stable, siege, rally, tournament_square, horse_upkeep,
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


class Tribe:
    teutons = "teutons"
    romans = "romans"
    gauls = "gauls"


class UnitType:
    cavalry = "cavalry"
    infantry = "infantry"

    def __init__(self, atk_upgrade=0, def_upgrade=0, whole_object=None):
        if whole_object is None:
            self.name = ""
            self.uid = 0
            self.tribe = ""
            self.unit_type = ""
            self.atk = 0
            self.inf_def = 0
            self.cav_def = 0
            self.speed = 0
            self.upkeep = 0
            self.cost = [0, 0, 0, 0]
            self.atk_upgrade = atk_upgrade
            self.def_upgrade = def_upgrade
        else:
            self.__dict__.update(whole_object.__dict__)

    @classmethod
    def from_init(cls, name, uid, tribe, unit_type, train_building, atk, inf_def, cav_def, speed, loot, upkeep, cost):
        unit = UnitType()
        unit.name = name
        unit.uid = uid
        unit.tribe = tribe
        unit.unit_type = unit_type
        unit.train_building = train_building
        unit.atk = atk
        unit.inf_def = inf_def
        unit.cav_def = cav_def
        unit.speed = speed
        unit.loot = loot
        unit.upkeep = upkeep
        unit.cost = copy.deepcopy(cost)
        return unit

    def __hash__(self):
        return hash((self.name, self.tribe))

    def __eq__(self, other):
        return self.name == other.name and self.tribe == other.tribe

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return self.name

class Unit:
    settle = 4
    reinforce = 2
    attack_normal = 3
    raid = 4

    legionnaire = UnitType.from_init("Legionnaire", 1, Tribe.romans, UnitType.infantry, Building.barracks, 40, 35, 50, 6, 50, 1, [120, 100, 150, 30])
    praetorian = UnitType.from_init("Praetorian", 2, Tribe.romans, UnitType.infantry, Building.barracks, 30, 65, 35, 5, 20, 1, [100, 130, 160, 70])
    imperian = UnitType.from_init("Imperian", 3, Tribe.romans, UnitType.infantry, Building.barracks, 70, 40, 25, 7, 50, 1, [150, 160, 210, 80])
    legati = UnitType.from_init("Equites Legati", 4, Tribe.romans, UnitType.cavalry, Building.stable, 0, 20, 10, 16, 0, 2, [140, 160, 20, 40])
    imperatoris = UnitType.from_init("Equites Imperatoris", 5, Tribe.romans, UnitType.cavalry, Building.stable, 120, 65, 50, 14, 100, 3, [550, 440, 320, 100])
    caesaris = UnitType.from_init("Equites Caesaris", 6, Tribe.romans, UnitType.cavalry, Building.stable, 180, 80, 105, 10, 70, 4, [550, 640, 800, 180])
    roman_ram = UnitType.from_init("Battering ram", 7, Tribe.romans, UnitType.infantry, Building.siege, 60, 30, 75, 4, 0, 3, [900, 360, 500, 70])
    roman_catapult = UnitType.from_init("Fire Catapult", 8, Tribe.romans, UnitType.infantry, Building.siege, 75, 60, 10, 3, 0, 6, [950, 1350, 600, 90])
    roman_chief = UnitType.from_init("Senator", 9, Tribe.romans, UnitType.infantry, Building.residence, 50, 40, 30, 4, 0, 5, [30750, 27200, 45000, 37500])
    roman_settler = UnitType.from_init("Settler", 10, Tribe.romans, UnitType.infantry, Building.residence, 0, 80, 80, 5, 3000, 1, [5800, 5300, 7200, 5500])

    romans = \
        [legionnaire, praetorian, imperian,
         legati, imperatoris, caesaris,
         roman_ram, roman_catapult,
         roman_chief, roman_settler]

    all = romans
