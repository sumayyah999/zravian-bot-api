import copy


class BuildingType:
    # TODO(@alexvelea) Add some more info, such as
    # - capital only
    # - multiple build? (for granary, warehouse)
    # - requirements?

    def __init__(self, name=None, bid=None, max_level=None, base_price=None, cost_grow=None, whole_object=None,):
        if whole_object is None:
            self.name = name
            self.bid = bid
            self.max_level = max_level
            self.base_price = base_price
            self.cost_grow = cost_grow
        else:
            self.__dict__.update(whole_object.__dict__)

    def resources_for_lvl(self, lvl):
        cost_multiplier = self.cost_grow ** (lvl - 1)
        return list(map(lambda x: 5 * round(x * cost_multiplier / 5), self.base_price))

    def __str__(self):
        return self.name


# TODO(@alexvelea) Add The rest of the buildings extended Rax, wall as well as race-specific buildings
# Collection of all building types as well as various info for API calls
class Building:
    cost_default = 1.28
    cost_resources = 1.67
    cost_resources_bonus = 1.8

    empty = BuildingType('Empty place', 0)

    # Overview Resources
    wood = BuildingType('Woodcutter', 1, max_level=20, base_price=[40, 100, 50, 60], cost_grow=cost_resources)
    clay = BuildingType('Clay Pit', 2, max_level=20, base_price=[80, 40, 80, 50], cost_grow=cost_resources)
    iron = BuildingType('Iron Mine', 3, max_level=20, base_price=[100, 80, 30, 60], cost_grow=cost_resources)
    crop = BuildingType('Cropland', 4, max_level=20, base_price=[70, 90, 70, 20], cost_grow=cost_resources)

    # Economy Infrastructure
    warehouse = BuildingType('Warehouse', 10, max_level=20, base_price=[130, 160, 90, 40], cost_grow=cost_default)
    granary = BuildingType('Granary', 11, max_level=20, base_price=[80, 100, 70, 20], cost_grow=cost_default)
    marketplace = BuildingType('Marketplace', 17, max_level=20, base_price=[80, 70, 120, 70], cost_grow=cost_default)
    trade_office = BuildingType("Trade Office", 28, max_level=20, base_price=[1400, 1330, 1200, 400], cost_grow=cost_default)

    # Infrastructure
    mainB = BuildingType('Main Building', 15, max_level=20, base_price=[70, 40, 60, 20], cost_grow=cost_default)
    cranny = BuildingType('Cranny', 23, max_level=10, base_price=[40, 50, 30, 10], cost_grow=cost_default)
    embassy = BuildingType('Embassy', 18, max_level=20, base_price=[180, 130, 150, 80], cost_grow=cost_default)
    hero_mansion = BuildingType("Hero's Mansion", 37, max_level=20, base_price=[700, 670, 700, 240], cost_grow=1.33)

    # Military
    barracks = BuildingType('Barracks', 19, max_level=20, base_price=[210, 140, 260, 120], cost_grow=cost_default)
    stable = BuildingType('Stable', 20, max_level=20, base_price=[260, 140, 220, 100], cost_grow=cost_default)
    siege = BuildingType('Siege Workshop', 21, max_level=20, base_price=[460, 510, 600, 320], cost_grow=cost_default)
    blacksmith = BuildingType('Blacksmith', 12, max_level=20, base_price=[170, 200, 380, 130], cost_grow=cost_default)
    armoury = BuildingType('Armoury', 13, max_level=20, base_price=[130, 210, 410, 130], cost_grow=cost_default)

    # Military infrastructure
    academy = BuildingType('Academy', 22, max_level=20, base_price=[220, 160, 90, 40], cost_grow=cost_default)
    rally = BuildingType('Rally Point', 16, max_level=20, base_price=[110, 160, 90, 70], cost_grow=cost_default)
    tournament_square = BuildingType('Tournament Square', 14, max_level=20, base_price=[1750, 2250, 1530, 240], cost_grow=cost_default)
    horse_upkeep = BuildingType('Horse Drinking Pool', 41, max_level=20, base_price=[780, 420, 660, 540], cost_grow=cost_default)
    brewery = BuildingType("Brewery", 35, max_level=10, base_price=[1460, 930, 1250, 1740], cost_grow=1.4)

    # Expansion
    residence = BuildingType('Residence', 25, max_level=20, base_price=[580, 460, 350, 180], cost_grow=cost_default)
    palace = BuildingType("Palace", 26, max_level=20, base_price=[550, 800, 750, 250], cost_grow=cost_default)
    hall = BuildingType('Town Hall', 24, max_level=20, base_price=[1250, 1110, 1260, 600], cost_grow=cost_default)

    # Resources
    bonusWood = BuildingType('Sawmill', 5, max_level=5, base_price=[520, 380, 290, 90], cost_grow=cost_resources_bonus)
    bonusClay = BuildingType('Brickworks', 6, max_level=5, base_price=[440, 480, 320, 50], cost_grow=cost_resources_bonus)
    bonusIron = BuildingType('Iron Foundry', 7, max_level=5, base_price=[200, 450, 510, 120], cost_grow=cost_resources_bonus)
    bonusCrop1 = BuildingType('Flour Mill', 8, max_level=5, base_price=[500, 440, 380, 1240], cost_grow=cost_resources_bonus)
    bonusCrop2 = BuildingType('Bakery', 9, max_level=5, base_price=[1200, 1480, 870, 1600], cost_grow=cost_resources_bonus)

    all = [
        empty,
        wood, clay, iron, crop,
        warehouse, granary,  marketplace, trade_office,
        mainB, cranny, embassy, hero_mansion,
        barracks, stable, siege, blacksmith, armoury,
        academy, rally, tournament_square, horse_upkeep, brewery,
        residence, palace, hall,
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
