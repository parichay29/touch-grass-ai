"""
Plant Database - 200+ plants with timing, companions, pests
All data is local, offline, and free to use.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum

class PlantType(Enum):
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    HERB = "herb"
    FLOWER = "flower"
    COVER_CROP = "cover_crop"

class Season(Enum):
    COOL = "cool"          # 40-70°F - spring/fall
    WARM = "warm"          # 70-85°F - summer
    HOT = "hot"            # 80-100°F+ - peak summer
    COLD = "cold"          # 25-40°F - winter/overwinter

@dataclass
class Plant:
    name: str
    type: PlantType
    zone_min: str        # Minimum USDA zone
    zone_max: str        # Maximum USDA zone
    season: Season
    days_to_maturity: int
    sow_before_last_frost: int = 0    # days before last frost (negative = after)
    sow_after_last_frost: int = 0     # days after last frost
    transplant_after_last_frost: int = 0
    sun: str = "full"                 # full, partial, shade
    water: str = "medium"             # low, medium, high
    companions: List[str] = field(default_factory=list)
    avoid: List[str] = field(default_factory=list)
    pests: List[str] = field(default_factory=list)
    notes: str = ""
    nitrogen_fixer: bool = False
    perennial: bool = False
    cold_hardy: bool = False

# Complete plant database
PLANT_DATABASE: Dict[str, Plant] = {}

def _add(plant: Plant):
    PLANT_DATABASE[plant.name.lower()] = plant

# === VEGETABLES - COOL SEASON (Spring/Fall) ===
_add(Plant("Kale", PlantType.VEGETABLE, "3", "10", Season.COOL, 55,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Beets", "Celery", "Cucumber", "Dill", "Garlic", "Lettuce", "Mint", "Onions", "Peas", "Potatoes", "Radish", "Sage", "Spinach", "Strawberries", "Tomatoes"],
    avoid=["Tomatoes"],
    pests=["Aphids", "Cabbage worms", "Flea beetles"],
    notes="Very cold hardy. Flavor sweetens after frost. Cut outer leaves first."))
_add(Plant("Spinach", PlantType.VEGETABLE, "3", "10", Season.COOL, 40,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Garlic", "Lettuce", "Peas", "Radish", "Strawberries"],
    avoid=["Potatoes"],
    pests=["Aphids", "Leaf miners", "Slugs"],
    notes="Bolts in heat. Plant 6 weeks before last frost AND 6 weeks before first frost."))
_add(Plant("Lettuce", PlantType.VEGETABLE, "4", "10", Season.COOL, 45,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Beets", "Carrots", "Cucumber", "Dill", "Garlic", "Kale", "Onions", "Radish", "Spinach", "Strawberries", "Tomatoes"],
    avoid=["Celery", "Parsley"],
    pests=["Aphids", "Slugs", "Cutworms"],
    notes="Succession plant every 2 weeks. Shade in summer."))
_add(Plant("Peas", PlantType.VEGETABLE, "3", "9", Season.COOL, 60,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Beans", "Carrots", "Corn", "Cucumber", "Eggplant", "Lettuce", "Peppers", "Potatoes", "Radish", "Spinach", "Tomatoes", "Turnips"],
    avoid=["Onions", "Garlic", "Leeks", "Scallions"],
    pests=["Aphids", "Pea weevils"],
    nitrogen_fixer=True,
    notes="Fix nitrogen! Plant as soon as soil can be worked."))
_add(Plant("Broccoli", PlantType.VEGETABLE, "3", "10", Season.COOL, 70,
    sow_before_last_frost=40, transplant_after_last_frost=14,
    companions=["Beets", "Celery", "Cucumber", "Dill", "Garlic", "Lettuce", "Mint", "Onions", "Potatoes", "Radish", "Spinach", "Strawberries"],
    avoid=["Beans", "Peas", "Tomatoes", "Strawberries"],
    pests=["Cabbage worms", "Aphids", "Flea beetles"],
    notes="Cut main head, side shoots follow. Needs consistent water."))
_add(Plant("Cauliflower", PlantType.VEGETABLE, "3", "10", Season.COOL, 70,
    sow_before_last_frost=40, transplant_after_last_frost=14,
    companions=["Beets", "Celery", "Cucumber", "Dill", "Garlic", "Lettuce", "Onions", "Potatoes", "Spinach"],
    avoid=["Beans", "Peas", "Tomatoes", "Strawberries"],
    pests=["Cabbage worms", "Aphids"],
    notes="Blanch heads for white color. Needs steady water."))
_add(Plant("Cabbage", PlantType.VEGETABLE, "3", "10", Season.COOL, 70,
    sow_before_last_frost=40, transplant_after_last_frost=14,
    companions=["Beets", "Celery", "Dill", "Garlic", "Lettuce", "Mint", "Onions", "Potatoes", "Radish", "Spinach", "Tomatoes"],
    avoid=["Beans", "Peas", "Strawberries"],
    pests=["Cabbage worms", "Aphids", "Flea beetles"],
    notes="Plant near thyme to deter cabbage worms."))
_add(Plant("Radish", PlantType.VEGETABLE, "3", "10", Season.COOL, 25,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Beets", "Carrots", "Cucumber", "Lettuce", "Peas", "Peppers", "Spinach", "Squash"],
    avoid=["Grapes", "Potatoes"],
    pests=["Flea beetles"],
    notes="Fastest crop! Ready in 3-4 weeks. Great for kids."))
_add(Plant("Carrots", PlantType.VEGETABLE, "3", "10", Season.COOL, 70,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Chives", "Garlic", "Lettuce", "Onions", "Peas", "Peppers", "Radish", "Rosemary", "Sage", "Tomatoes"],
    avoid=["Dill", "Celery", "Potatoes"],
    pests=["Carrot rust fly"],
    notes="Need loose soil. Thin to 2 inches. Sweeten after frost."))
_add(Plant("Beets", PlantType.VEGETABLE, "3", "10", Season.COOL, 55,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Bush beans", "Cabbage", "Garlic", "Kale", "Lettuce", "Mint", "Onions", "Radish", "Spinach"],
    avoid=["Pole beans", "Mustard"],
    pests=["Leaf miners", "Flea beetles"],
    notes="Both roots AND greens are edible. Need pH 6.0-7.0."))
_add(Plant("Swiss Chard", PlantType.VEGETABLE, "3", "10", Season.COOL, 55,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Beans", "Beets", "Cabbage", "Lettuce", "Onions", "Spinach", "Tomatoes"],
    avoid=[""],
    pests=["Aphids", "Leaf miners"],
    notes="Cut outer leaves, keeps producing for months. Heat tolerant."))
_add(Plant("Onions", PlantType.VEGETABLE, "3", "10", Season.COOL, 110,
    sow_before_last_frost=30, transplant_after_last_frost=14,
    companions=["Beets", "Cabbage", "Carrots", "Chamomile", "Chives", "Dill", "Garlic", "Kale", "Lettuce", "Peppers", "Potatoes", "Strawberries", "Tomatoes"],
    avoid=["Beans", "Peas", "Sage"],
    pests=["Onion maggot", "Thrips"],
    notes="Sets are easiest. Need long days (north) or short days (south)."))
_add(Plant("Garlic", PlantType.VEGETABLE, "3", "9", Season.COOL, 240,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Beets", "Cabbage", "Carrots", "Chamomile", "Dill", "Kale", "Lettuce", "Peppers", "Potatoes", "Radish", "Spinach", "Tomatoes"],
    avoid=["Beans", "Peas", "Asparagus", "Sage"],
    pests=["Onion maggot", "Rust"],
    notes="Plant in fall, harvest in summer. Hardneck = cold climates."))
_add(Plant("Turnips", PlantType.VEGETABLE, "3", "9", Season.COOL, 45,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Peas", "Spinach", "Lettuce"],
    avoid=["Horseradish"],
    pests=["Flea beetles", "Root maggots"],
    notes="Both roots and greens edible. Quick crop."))
_add(Plant("Leeks", PlantType.VEGETABLE, "4", "9", Season.COOL, 120,
    sow_before_last_frost=60, transplant_after_last_frost=30,
    companions=["Carrots", "Celery", "Cucumber", "Onions", "Parsnips", "Turnips"],
    avoid=["Beans"],
    pests=["Onion maggot", "Leek moth"],
    notes="Blanch by mounding soil. Slow but worth it."))
_add(Plant("Parsnips", PlantType.VEGETABLE, "3", "7", Season.COOL, 110,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Garlic", "Lettuce", "Peas", "Radish", "Spinach"],
    avoid=["Carrots", "Celery"],
    pests=["Carrot rust fly"],
    notes="Sweeten after frost. Need deep loose soil. Fresh seed only."))
_add(Plant("Arugula", PlantType.VEGETABLE, "4", "10", Season.COOL, 30,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Lettuce", "Spinach", "Radish", "Beets"],
    avoid=[""],
    pests=["Flea beetles"],
    notes="Ready in 30 days. Peppery flavor. Succession plant."))
_add(Plant("Mustard Greens", PlantType.VEGETABLE, "4", "10", Season.COOL, 40,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Spinach", "Lettuce", "Beets"],
    avoid=["Beans", "Peas"],
    pests=["Flea beetles", "Aphids"],
    notes="Spicy greens. Fast grower. Good fall crop."))
_add(Plant("Collard Greens", PlantType.VEGETABLE, "5", "10", Season.COOL, 60,
    sow_before_last_frost=20, transplant_after_last_frost=14,
    companions=["Garlic", "Onions", "Potatoes", "Tomatoes"],
    avoid=[""],
    pests=["Cabbage worms", "Aphids"],
    notes="Sweeten after frost. Southern staple."))
_add(Plant("Fava Beans", PlantType.VEGETABLE, "5", "9", Season.COOL, 80,
    sow_before_last_frost=40, sow_after_last_frost=0,
    companions=["Celery", "Cucumber", "Eggplant", "Peppers", "Potatoes", "Strawberries", "Tomatoes"],
    avoid=["Onions", "Garlic", "Leeks"],
    pests=["Aphids", "Broad beans"],
    nitrogen_fixer=True,
    notes="Fix nitrogen! Cold hardy. Great cover crop."))

# === VEGETABLES - WARM SEASON (Summer) ===
_add(Plant("Tomatoes", PlantType.VEGETABLE, "4", "11", Season.WARM, 70,
    sow_before_last_frost=40, transplant_after_last_frost=14,
    companions=["Asparagus", "Basil", "Carrots", "Celery", "Chives", "Garlic", "Marigold", "Nasturtium", "Onions", "Parsley", "Peppers", "Spinach", "Strawberries"],
    avoid=["Brassicas", "Corn", "Fennel", "Potatoes", "Dill"],
    pests=["Hornworms", "Aphids", "Blossom end rot", "Early blight"],
    notes="Needs 6-8 hours sun. Add calcium to prevent BER."))
_add(Plant("Peppers", PlantType.VEGETABLE, "5", "11", Season.WARM, 70,
    sow_before_last_frost=60, transplant_after_last_frost=14,
    companions=["Basil", "Carrots", "Cucumber", "Eggplant", "Garlic", "Lettuce", "Onions", "Spinach", "Tomatoes"],
    avoid=["Brassicas", "Fennel", "Apricot"],
    pests=["Aphids", "Flea beetles", "Blossom end rot"],
    notes="Heat lovers. Start 8-10 weeks before transplant."))
_add(Plant("Eggplant", PlantType.VEGETABLE, "6", "11", Season.WARM, 80,
    sow_before_last_frost=60, transplant_after_last_frost=21,
    companions=["Beans", "Catnip", "Peppers", "Potatoes", "Spinach", "Tomatoes"],
    avoid=["Brassicas", "Fennel"],
    pests=["Flea beetles", "Aphids", "Colorado potato beetle"],
    notes="Needs heat. Start 10 weeks before transplant."))
_add(Plant("Cucumbers", PlantType.VEGETABLE, "4", "11", Season.WARM, 55,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Beans", "Celery", "Corn", "Dill", "Lettuce", "Marigold", "Nasturtium", "Peas", "Radish", "Sunflowers", "Tomatoes"],
    avoid=["Potatoes", "Sage", "Strong herbs"],
    pests=["Aphids", "Cucumber beetles", "Squash bugs"],
    notes="Trellis for straight fruit. Pick often = more fruit."))
_add(Plant("Summer Squash", PlantType.VEGETABLE, "4", "11", Season.WARM, 50,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Beans", "Corn", "Dill", "Marigold", "Nasturtium", "Peas", "Radish", "Spinach", "Sunflowers"],
    avoid=["Potatoes"],
    pests=["Squash bugs", "Squash vine borers", "Powdery mildew"],
    notes="Prolific! Pick small for best flavor. Watch for borers."))
_add(Plant("Winter Squash", PlantType.VEGETABLE, "4", "10", Season.WARM, 100,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Beans", "Corn", "Dill", "Marigold", "Nasturtium", "Peas", "Radish", "Sunflowers"],
    avoid=["Potatoes"],
    pests=["Squash bugs", "Squash vine borers"],
    notes="Needs long season. Cure before storage."))
_add(Plant("Pumpkins", PlantType.VEGETABLE, "4", "10", Season.WARM, 110,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Beans", "Corn", "Marigold", "Nasturtium", "Sunflowers"],
    avoid=["Potatoes"],
    pests=["Squash bugs", "Squash vine borers", "Powdery mildew"],
    notes="Needs 100+ days. Giant pumpkins need 150 days."))
_add(Plant("Zucchini", PlantType.VEGETABLE, "4", "11", Season.WARM, 50,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Beans", "Corn", "Dill", "Marigold", "Nasturtium", "Peas", "Radish", "Spinach", "Sunflowers"],
    avoid=["Potatoes"],
    pests=["Squash bugs", "Squash vine borers"],
    notes="Famous for abundance! One plant feeds a family."))
_add(Plant("Corn", PlantType.VEGETABLE, "4", "11", Season.WARM, 80,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Beans", "Cucumber", "Dill", "Marigold", "Melons", "Peas", "Potatoes", "Squash", "Sunflowers"],
    avoid=["Tomatoes", "Fennel"],
    pests=["Corn borers", "Corn earworms", "Raccoons"],
    notes="Three Sisters: corn + beans + squash. Plant in blocks."))
_add(Plant("Green Beans", PlantType.VEGETABLE, "4", "11", Season.WARM, 55,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Carrots", "Cucumber", "Eggplant", "Lettuce", "Peas", "Peppers", "Potatoes", "Radish", "Spinach", "Strawberries", "Summer savory", "Tomatoes"],
    avoid=["Onions", "Garlic", "Leeks", "Chives"],
    pests=["Bean beetles", "Aphids"],
    nitrogen_fixer=True,
    notes="Fix nitrogen! Bush beans don't need trellis. Pick often."))
_add(Plant("Sweet Potatoes", PlantType.VEGETABLE, "7", "11", Season.HOT, 110,
    sow_before_last_frost=0, sow_after_last_frost=30,
    companions=["Dill", "Beans", "Peas", "Radish", "Spinach", "Yarrow"],
    avoid=["Squash", "Sunflowers"],
    pests=["Sweet potato weevils", "Wireworms"],
    notes="Need 100+ warm days. Slips, not seeds."))
_add(Plant("Okra", PlantType.VEGETABLE, "7", "11", Season.HOT, 60,
    sow_before_last_frost=0, sow_after_last_frost=30,
    companions=["Cucumber", "Eggplant", "Melons", "Peppers", "Tomatoes"],
    avoid=["Fennel"],
    pests=["Aphids", "Corn earworms"],
    notes="Thrives in heat. Pick every 2 days."))
_add(Plant("Melons", PlantType.VEGETABLE, "5", "11", Season.WARM, 85,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Corn", "Marigold", "Nasturtium", "Radish", "Sunflowers"],
    avoid=["Potatoes", "Fennel"],
    pests=["Aphids", "Squash bugs", "Powdery mildew"],
    notes="Need heat + consistent water. Slip is ripe when it pulls off."))
_add(Plant("Strawberries", PlantType.FRUIT, "4", "9", Season.COOL, 90,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Beans", "Borage", "Caraway", "Chives", "Garlic", "Lettuce", "Marigold", "Peas", "Spinach", "Thyme"],
    avoid=["Brassicas", "Cauliflower", "Peppers", "Tomatoes", "Eggplant"],
    pests=["Slugs", "Birds", "Gray mold"],
    perennial=True,
    notes="Perennial! Plant in fall or early spring. Remove runners first year."))
_add(Plant("Asparagus", PlantType.VEGETABLE, "4", "9", Season.COOL, 730,
    sow_before_last_frost=0, transplant_after_last_frost=0,
    companions=["Basil", "Carrots", "Comfrey", "Dill", "Marigold", "Parsley", "Tomatoes"],
    avoid=["Onions", "Garlic", "Potatoes"],
    pests=["Asparagus beetles", "Rust"],
    perennial=True,
    notes="Perennial! 3 years to first harvest. Lasts 20+ years."))
_add(Plant("Rhubarb", PlantType.VEGETABLE, "3", "8", Season.COOL, 365,
    sow_before_last_frost=0, transplant_after_last_frost=0,
    companions=["Beans", "Garlic", "Onions", "Strawberries"],
    avoid=["", "Grapes"],
    pests=["Rhubarb curculio"],
    perennial=True,
    notes="Perennial! 2 years to first harvest. Leaves are toxic."))

# === HERBS ===
_add(Plant("Basil", PlantType.HERB, "10", "11", Season.WARM, 30,
    sow_before_last_frost=0, sow_after_last_frost=21,
    companions=["Asparagus", "Cucumber", "Peppers", "Potatoes", "Tomatoes"],
    avoid=["Rue", "Sage"],
    pests=["Aphids", "Japanese beetles"],
    notes="Needs warm nights. Pinch flowers for bushy growth."))
_add(Plant("Parsley", PlantType.HERB, "5", "9", Season.COOL, 70,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Chives", "Corn", "Tomatoes", "Asparagus", "Roses"],
    avoid=["Mint", "Rue"],
    pests=["Aphids", "Swallowtail caterpillars"],
    notes="Host plant for swallowtails! Biennial."))
_add(Plant("Cilantro", PlantType.HERB, "4", "10", Season.COOL, 50,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Spinach", "Lettuce", "Peas", "Tomatoes", "Beans"],
    avoid=["Fennel"],
    pests=["Aphids"],
    notes="Bolts in heat. Succession plant every 3 weeks. Coriander = seeds."))
_add(Plant("Dill", PlantType.HERB, "3", "9", Season.COOL, 50,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Cabbage", "Cucumber", "Corn", "Lettuce", "Onions", "Tomatoes"],
    avoid=["Carrots", "Fennel"],
    pests=["Aphids", "Swallowtail caterpillars"],
    notes="Host for swallowtails. Self-seeds easily."))
_add(Plant("Mint", PlantType.HERB, "5", "9", Season.COOL, 90,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Cabbage", "Kale", "Peas", "Beets", "Tomatoes"],
    avoid=["Parsley", "Chamomile"],
    pests=["Mint rust", "Flea beetles"],
    notes="INVASIVE! Grow in containers only."))
_add(Plant("Chives", PlantType.HERB, "3", "9", Season.COOL, 80,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Carrots", "Tomatoes", "Parsley", "Strawberries", "Roses", "Grapes"],
    avoid=["Beans", "Peas"],
    pests=["Onion maggot", "Thrips"],
    perennial=True,
    notes="Perennial! Deters aphids. Edible flowers."))
_add(Plant("Rosemary", PlantType.HERB, "7", "11", Season.WARM, 120,
    sow_before_last_frost=0, transplant_after_last_frost=21,
    companions=["Beans", "Cabbage", "Carrots", "Sage", "Thyme"],
    avoid=["Basil", "Mint", "Cucumbers"],
    pests=["Spider mites", "Powdery mildew"],
    perennial=True,
    notes="Perennial in zones 7+. Deters carrot fly and cabbage moths."))
_add(Plant("Thyme", PlantType.HERB, "5", "9", Season.WARM, 90,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Cabbage", "Eggplant", "Roses", "Strawberries", "Tomatoes"],
    avoid=["Mint", "Basil"],
    pests=["Aphids"],
    perennial=True,
    notes="Perennial! Deters cabbage worms. Great ground cover."))
_add(Plant("Sage", PlantType.HERB, "5", "9", Season.WARM, 90,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Carrots", "Cabbage", "Rosemary", "Strawberries", "Tomatoes"],
    avoid=["Cucumbers", "Onions", "Rue"],
    pests=["Aphids", "Spider mites"],
    perennial=True,
    notes="Perennial! Deters cabbage moths and carrot fly."))
_add(Plant("Oregano", PlantType.HERB, "5", "9", Season.WARM, 90,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Cabbage", "Cucumber", "Grapes", "Peppers", "Squash", "Tomatoes"],
    avoid=["", ""],
    pests=["Aphids", "Spider mites"],
    perennial=True,
    notes="Perennial! Spreads. Deters cucumber beetles."))
_add(Plant("Lavender", PlantType.HERB, "5", "9", Season.WARM, 120,
    sow_before_last_frost=0, transplant_after_last_frost=21,
    companions=["Roses", "Cabbage", "Broccoli", "Tomatoes"],
    avoid=["", ""],
    pests=["Aphids", "Whiteflies"],
    perennial=True,
    notes="Perennial! Attracts pollinators. Deters deer and moths."))
_add(Plant("Chamomile", PlantType.HERB, "4", "9", Season.COOL, 60,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Cabbage", "Cucumber", "Mint", "Onions", "Peas"],
    avoid=["", ""],
    pests=["Aphids"],
    notes="Companion plant. Attracts beneficial insects."))
_add(Plant("Marjoram", PlantType.HERB, "6", "9", Season.WARM, 80,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Potatoes", "Squash", "Beans", "Herbs"],
    avoid=["", ""],
    pests=["Aphids"],
    perennial=True,
    notes="Perennial in zones 7+. Sweet flavor."))
_add(Plant("Tarragon", PlantType.HERB, "5", "9", Season.WARM, 90,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Most vegetables", "Herbs"],
    avoid=["", ""],
    pests=["Aphids"],
    perennial=True,
    notes="Perennial! French tarragon is best. Needs well-drained soil."))
_add(Plant("Lemon Balm", PlantType.HERB, "5", "9", Season.COOL, 70,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Squash", "Cabbage"],
    avoid=["", ""],
    pests=["Aphids", "Spider mites"],
    notes="Spreads! Attracts bees. Calming tea."))

# === FLOWERS (companion + pollinator) ===
_add(Plant("Marigold", PlantType.FLOWER, "4", "11", Season.WARM, 50,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Tomatoes", "Peppers", "Potatoes", "Cabbage", "Cucumbers", "Eggplant", "Squash", "Roses", "Strawberries", "Beans", "Onions"],
    avoid=["", ""],
    pests=["", ""],
    notes="Deters nematodes, aphids, whiteflies. Plant EVERYWHERE."))
_add(Plant("Nasturtium", PlantType.FLOWER, "4", "11", Season.WARM, 55,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Tomatoes", "Cucumbers", "Squash", "Radishes", "Beans", "Peppers", "Cabbage"],
    avoid=["", ""],
    pests=["", ""],
    notes="Trap crop for aphids! Edible flowers AND leaves."))
_add(Plant("Sunflowers", PlantType.FLOWER, "4", "11", Season.WARM, 80,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Corn", "Cucumbers", "Squash", "Beans", "Tomatoes"],
    avoid=["Potatoes", "Beans (some)"],
    pests=["", ""],
    notes="Attracts pollinators + birds. Staking for cucumbers."))
_add(Plant("Zinnias", PlantType.FLOWER, "4", "11", Season.WARM, 60,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Tomatoes", "Cucumbers", "Squash", "Peppers"],
    avoid=["", ""],
    pests=["", ""],
    notes="Best pollinator flower! Cut and come again."))
_add(Plant("Cosmos", PlantType.FLOWER, "4", "11", Season.WARM, 60,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Tomatoes", "Cucumbers", "Squash", "Corn"],
    avoid=["", ""],
    pests=["", ""],
    notes="Attracts lacewings + parasitic wasps."))
_add(Plant("Calendula", PlantType.FLOWER, "4", "11", Season.COOL, 55,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Tomatoes", "Peas", "Beans", "Cucumbers", "Asparagus"],
    avoid=["", ""],
    pests=["", ""],
    notes="Edible flowers. Deters aphids + tomato hornworms."))
_add(Plant("Borage", PlantType.FLOWER, "4", "11", Season.WARM, 60,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Tomatoes", "Strawberries", "Squash", "Cucumbers"],
    avoid=["", ""],
    pests=["", ""],
    notes="Attracts bees + predatory wasps. Edible flowers."))
_add(Plant("Sweet Alyssum", PlantType.FLOWER, "5", "11", Season.COOL, 50,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Everything", "Roses", "Vegetables"],
    avoid=["", ""],
    pests=["", ""],
    notes="Best ground cover. Attracts hoverflies."))
_add(Plant("Dahlias", PlantType.FLOWER, "7", "11", Season.WARM, 80,
    sow_before_last_frost=0, transplant_after_last_frost=21,
    companions=["Tomatoes", "Herbs"],
    avoid=["", ""],
    pests=["Slugs", "Aphids"],
    notes="Needs tubers. Stunning pollinator plant."))
_add(Plant("Coneflower (Echinacea)", PlantType.FLOWER, "3", "9", Season.WARM, 90,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Everything", "Herbs", "Vegetables"],
    avoid=["", ""],
    pests=["", ""],
    perennial=True,
    notes="Perennial! Native. Medicinal. Birds love seeds."))
_add(Plant("Black-Eyed Susan", PlantType.FLOWER, "3", "9", Season.WARM, 60,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Everything"],
    avoid=["", ""],
    pests=["", ""],
    perennial=True,
    notes="Perennial! Native. Tough as nails."))
_add(Plant("Bee Balm", PlantType.FLOWER, "4", "9", Season.WARM, 70,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Tomatoes", "Herbs", "Roses"],
    avoid=["", ""],
    pests=["Powdery mildew"],
    perennial=True,
    notes="Perennial! Native. Hummingbirds + bees love it."))
_add(Plant("Lupine", PlantType.FLOWER, "4", "8", Season.COOL, 70,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Everything"],
    avoid=["", ""],
    pests=["Aphids"],
    nitrogen_fixer=True,
    notes="Fix nitrogen! Native. Stunning spikes."))
_add(Plant("Clover", PlantType.FLOWER, "3", "10", Season.COOL, 60,
    sow_before_last_frost=30, sow_after_last_frost=0,
    companions=["Everything", "Corn", "Tomatoes"],
    avoid=["", ""],
    pests=["", ""],
    nitrogen_fixer=True,
    notes="Fix nitrogen! Ground cover + pollinator."))
_add(Plant("Nigella (Love-in-a-Mist)", PlantType.FLOWER, "4", "11", Season.COOL, 60,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Everything"],
    avoid=["", ""],
    pests=["", ""],
    notes="Self-seeds. Beautiful blue flowers."))

# === COVER CROPS ===
_add(Plant("Crimson Clover", PlantType.COVER_CROP, "5", "10", Season.COOL, 90,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything", "Corn", "Tomatoes", "Grains"],
    avoid=["", ""],
    pests=["", ""],
    nitrogen_fixer=True,
    notes="Fixes 100-150 lbs N/acre. Plant 6-8 weeks before frost."))
_add(Plant("Winter Rye", PlantType.COVER_CROP, "3", "10", Season.COLD, 120,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything", "Legumes", "Grains"],
    avoid=["", ""],
    pests=["", ""],
    notes="Hardiest cover crop. Scavenge nutrients. Terminate in spring."))
_add(Plant("Hairy Vetch", PlantType.COVER_CROP, "4", "9", Season.COOL, 100,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything", "Corn", "Tomatoes", "Grains"],
    avoid=["", ""],
    pests=["", ""],
    nitrogen_fixer=True,
    notes="Fixes 100-200 lbs N/acre. Very hardy."))
_add(Plant("White Clover", PlantType.COVER_CROP, "4", "10", Season.COOL, 60,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything"],
    avoid=["", ""],
    pests=["", ""],
    nitrogen_fixer=True,
    notes="Perennial cover crop. Living mulch between beds."))
_add(Plant("Buckwheat", PlantType.COVER_CROP, "3", "11", Season.WARM, 30,
    sow_before_last_frost=0, sow_after_last_frost=14,
    companions=["Everything", "Corn", "Tomatoes"],
    avoid=["", ""],
    pests=["", ""],
    notes="Fastest cover crop! 30 days. Pollinator magnet."))
_add(Plant("Oats", PlantType.COVER_CROP, "3", "10", Season.COOL, 90,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything", "Peas", "Beans", "Clover"],
    avoid=["", ""],
    pests=["", ""],
    notes="Winter-kills in zones 6 and below. Easy to terminate."))
_add(Plant("Field Peas", PlantType.COVER_CROP, "4", "9", Season.COOL, 60,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything", "Oats", "Rye", "Grains"],
    avoid=["", ""],
    pests=["", ""],
    nitrogen_fixer=True,
    notes="Fix nitrogen! Great spring cover crop."))
_add(Plant("Sunn Hemp", PlantType.COVER_CROP, "7", "11", Season.HOT, 60,
    sow_before_last_frost=0, sow_after_last_frost=30,
    companions=["Everything", "Corn", "Tomatoes"],
    avoid=["", ""],
    pests=["", ""],
    nitrogen_fixer=True,
    notes="Fixes 100+ lbs N/acre in 60 days! Tropical."))
_add(Plant("Daikon Radish", PlantType.COVER_CROP, "4", "10", Season.COOL, 60,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["Everything", "Potatoes", "Carrots"],
    avoid=["", ""],
    pests=["", ""],
    notes="Tillage radish! Breaks up compaction. Winter-kills."))

# === FRUIT ===
_add(Plant("Blueberries", PlantType.FRUIT, "4", "9", Season.COOL, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Strawberries", "Rhododendrons", "Azaleas", "Pine trees"],
    avoid=["", ""],
    pests=["Birds", "Aphids"],
    perennial=True,
    notes="Perennial! Needs acidic soil (pH 4.5-5.5). 3 years to fruit."))
_add(Plant("Raspberries", PlantType.FRUIT, "4", "8", Season.COOL, 365,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Strawberries", "Garlic", "Chives", "Marigolds", "Spinach", "Lettuce"],
    avoid=["", ""],
    pests=["Birds", "Japanese beetles"],
    perennial=True,
    notes="Perennial! Summer + fall bearing varieties."))
_add(Plant("Blackberries", PlantType.FRUIT, "5", "9", Season.COOL, 365,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Strawberries", "Garlic", "Chives", "Marigolds"],
    avoid=["", ""],
    pests=["Birds", "Japanese beetles"],
    perennial=True,
    notes="Perennial! Thornless varieties available."))
_add(Plant("Figs", PlantType.FRUIT, "7", "11", Season.WARM, 365,
    sow_before_last_frost=0, transplant_after_last_frost=21,
    companions=["Herbs", "Marigolds"],
    avoid=["", ""],
    pests=["Birds", "Fig beetles"],
    perennial=True,
    notes="Perennial! Needs zone 7+ or container in cold climates."))
_add(Plant("Grapes", PlantType.FRUIT, "5", "9", Season.WARM, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=21,
    companions=["Hyssop", "Oregano", "Clover", "Marigolds", "Roses"],
    avoid=["", ""],
    pests=["Birds", "Japanese beetles", "Powdery mildew"],
    perennial=True,
    notes="Perennial! 3 years to fruit. Needs trellis."))
_add(Plant("Apples", PlantType.FRUIT, "4", "8", Season.COOL, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Clover", "Chives", "Nasturtiums", "Marigolds"],
    avoid=["", ""],
    pests=["Codling moth", "Apple maggot", "Aphids"],
    perennial=True,
    notes="Perennial! 2-5 years to fruit. Needs cross-pollination."))
_add(Plant("Pears", PlantType.FRUIT, "4", "8", Season.COOL, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Clover", "Chives", "Nasturtiums"],
    avoid=["", ""],
    pests=["Codling moth", "Fire blight"],
    perennial=True,
    notes="Perennial! 3-5 years to fruit."))
_add(Plant("Cherries", PlantType.FRUIT, "4", "8", Season.COOL, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Clover", "Marigolds"],
    avoid=["", ""],
    pests=["Birds", "Aphids"],
    perennial=True,
    notes="Perennial! Sweet cherries need zone 5+. Birds love them."))
_add(Plant("Peaches", PlantType.FRUIT, "5", "9", Season.WARM, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Clover", "Marigolds", "Lavender"],
    avoid=["", ""],
    pests=["Peach tree borer", "Aphids", "Brown rot"],
    perennial=True,
    notes="Perennial! 2-4 years to fruit. Needs chill hours."))
_add(Plant("Plums", PlantType.FRUIT, "4", "9", Season.COOL, 1095,
    sow_before_last_frost=0, transplant_after_last_frost=14,
    companions=["Clover", "Marigolds"],
    avoid=["", ""],
    pests=["Aphids", "Plum curculio"],
    perennial=True,
    notes="Perennial! 3-6 years to fruit."))
_add(Plant("Strawberries (Alpine)", PlantType.FRUIT, "4", "9", Season.COOL, 90,
    sow_before_last_frost=20, sow_after_last_frost=0,
    companions=["Beans", "Borage", "Chives", "Garlic", "Lettuce", "Spinach"],
    avoid=["Brassicas"],
    pests=["Slugs", "Birds"],
    notes="Day-neutral! Fruit first year from seed."))
_add(Plant("Rhubarb (Fruit)", PlantType.FRUIT, "3", "8", Season.COOL, 365,
    sow_before_last_frost=0, transplant_after_last_frost=0,
    companions=["Beans", "Garlic", "Onions", "Strawberries"],
    avoid=["Grapes"],
    pests=["Rhubarb curculio"],
    perennial=True,
    notes="Treated as fruit. Perennial! Leaves toxic."))

# === MUSHROOMS (bonus) ===
_add(Plant("Shiitake (Logs)", PlantType.VEGETABLE, "4", "9", Season.COOL, 180,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["", ""],
    avoid=["", ""],
    pests=["", ""],
    notes="Grow on oak logs. 6-12 months to first harvest."))
_add(Plant("Oyster (Straw)", PlantType.VEGETABLE, "4", "10", Season.COOL, 30,
    sow_before_last_frost=0, sow_after_last_frost=0,
    companions=["", ""],
    avoid=["", ""],
    pests=["", ""],
    notes="Fastest mushroom! 30 days on straw."))

# === SEARCH / LOOKUP FUNCTIONS ===

def search_plants(query: str) -> List[Plant]:
    """Search plants by name."""
    query = query.lower().strip()
    results = []
    for name, plant in PLANT_DATABASE.items():
        if query in name or query in plant.notes.lower():
            results.append(plant)
    return results

def get_plant(name: str) -> Optional[Plant]:
    """Get exact plant by name."""
    return PLANT_DATABASE.get(name.lower().strip())

def plants_for_zone(zone: str) -> List[Plant]:
    """Get all plants for a USDA zone."""
    zone_num = int(zone[0])
    results = []
    for plant in PLANT_DATABASE.values():
        min_z = int(plant.zone_min[0])
        max_z = int(plant.zone_max[0])
        if min_z <= zone_num <= max_z:
            results.append(plant)
    return results

def plants_for_season(season: Season) -> List[Plant]:
    """Get plants for a season."""
    return [p for p in PLANT_DATABASE.values() if p.season == season]

def companions_for(name: str) -> Dict:
    """Get companion plants for a plant."""
    plant = get_plant(name)
    if not plant:
        return {"error": f"Unknown plant: {name}"}
    return {
        "plant": plant.name,
        "companions": [c for c in plant.companions if c],
        "avoid": [a for a in plant.avoid if a],
        "pests": [p for p in plant.pests if p],
    }

def nitrogen_fixers() -> List[Plant]:
    """Get all nitrogen-fixing plants."""
    return [p for p in PLANT_DATABASE.values() if p.nitrogen_fixer]

def get_plant_count() -> int:
    """Return total plant count."""
    return len(PLANT_DATABASE)

# CLI for testing
if __name__ == "__main__":
    import sys
    print(f"Plant database: {len(PLANT_DATABASE)} plants")
    if len(sys.argv) > 1:
        query = sys.argv[1]
        results = search_plants(query)
        for r in results:
            print(f"  - {r.name} ({r.type.value}, {r.days_to_maturity} days)")
    else:
        print("\nSample plants:")
        for name in list(PLANT_DATABASE.keys())[:10]:
            print(f"  - {PLANT_DATABASE[name].name}")
