from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

class ProductModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    image: str
    specs: Optional[str] = None

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    category: str
    description: str
    image: str
    popular: bool = False
    benefits: List[str] = []
    models: List[ProductModel] = []

class ContactInfo(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    website: str
    business_timing: str

# Image mapping: product name -> image filename
IMG = {
    "Bund Maker": "/products/bund_maker.png",
    "Seed Drill": "/products/seed_drill.png",
    "Rotavator": "/products/rotavator.png",
    "Cultivator": "/products/cultivator.png",
    "Power Weeder": "/products/power_weeder.png",
    "Earth Auger": "/products/earth_auger.png",
    "Disc Plough": "/products/disc_redger_plough.png",
    "Brush Cutter": "/products/brush_cutter.png",
    "Bio Thresher": "/products/bio_thresher.png",
    "Power Sprayer": "/products/power_sprayer.png",
    "Fertilizer Broadcaster": "/products/fertilizer_broadcaster.png",
    "Powder Duster": "/products/powder_duster.png",
    "Chainsaw": "/products/chainsaw.png",
    "Tree Pruner": "/products/tree_pruner.png",
    "Wheelbarrow": "/products/wheel_barrow.png",
    "Hedge Trimmer": "/products/hedge_trimmer.png",
    "Lawn Mower": "/products/lawn_mower.png",
    "Shovel": "/products/showel.png",
    "Hoe": "/products/hoe.png",
    "Bud Cutter": "/products/bud_cutter.png",
    "Rake": "/products/rake.png",
    "Fork": "/products/fork.png",
    "Grafting Knife": "/products/grafting_knife.png",
    "Manual Weeder": "/products/manual_weeder.png",
    "Trowel": "/products/trowel.png",
    "Sickle": "/products/sickle.png",
    "Secateur": "/products/secateur.png",
    "Bypass Pruner": "/products/bypass_pruner.png",
    "Anvil Pruner": "/products/anvil_pruner.png",
    "Hedge Shear": "/products/hedge_shear.png",
    "Grafting Machine": "/products/grafting_machine.png",
    "Nursery Bags": "/products/nursery_bags.png",
    "Flower Pots": "/products/flower_pots.png",
    "Grow Bags": "/products/grow_bags.png",
    "Vermibeds": "/products/vermibed.png",
    "Lopping Shear": "/products/lopping_shear.png",
    "Vertical Garden": "/products/vertical_garden.png",
    "Root Trays": "/products/root_tray.png",
    "Bone Meal": "/products/bone_meal.png",
    "De-oiled Cakes": "/products/de-oiled_cakes.png",
    "Blood Meal": "/products/blood_meal.png",
    "Vermicompost": "/products/vermicompost.png",
    "Manure": "/products/manure.png",
    "Cocopeat": "/products/cocopeat.png",
    "LECA Balls": "/products/leca_balls.png",
    "Artificial Soils": "/products/cocopeat.png",
    "Fish Meal": "/products/fish_meal.png",
    "Green Net / Polyfilms": "/products/green_net_polyfilms.png",
    "Greenhouse Accessories": "/products/greenhouse_accessories.png",
    "Mulch Films": "/products/mulch_films.png",
    "Walk-in Tunnels": "/products/walk-in_tunnels.png",
    "Small Greenhouse": "/products/small_greenhouse.png",
    "Propagation Sheets": "/products/propagation_sheets.png",
    "Trellis Nets": "/products/trellis_net.png",
    "Pop-up Sprinklers": "/products/pop-up_sprinkler.png",
    "Garden Sprinklers": "/products/garden_sprinkler.png",
    "Foggers": "/products/foggers.png",
    "Rain Guns": "/products/rain_guns.png",
    "Mini Sprinklers": "/products/mini_sprinkler.png",
    "Pumps": "/products/pumps.png",
    "Bell Fountain Sprinkler": "/products/bell_fountain_sprinkler.png",
    "Drip Irrigation": "/products/drip_irrigation.png",
    "Valves": "/products/valves.png",
    "Irrigation Accessories": "/products/garden_sprinkler.png",
    "Chakki": "/products/chakki.png",
    "Snake Rescue Kit": "/products/snake_rescue_kit.png",
    "Azola Beds": "/products/azola_bed.png",
    "Milk Can": "/products/milk_can.png",
    "Sieve": "/products/seive.png",
    "Crocodile Rescue Kit": "/products/crocodile_rescue_kit.png",
    "Monkey Rescue Kit": "/products/monkey_rescue_kit.png",
    "Leopard Rescue Net": "/products/leopard_rescue_net.png",
}

# Popular products - only these 10
POPULAR_NAMES = [
    "Rotavator", "Power Sprayer", "Lawn Mower", "Vermibeds",
    "Nursery Bags", "Vermicompost", "Small Greenhouse",
    "Rain Guns", "Drip Irrigation", "Snake Rescue Kit"
]

PRODUCTS_DATA = [
    # Farm Machinery
    {"name": "Bund Maker", "category": "Farm Machinery", "description": "Heavy-duty bund maker designed for efficient land leveling and water management in agricultural fields. Ideal for creating precise bunds and ridges.",
     "benefits": ["Efficient land leveling and water management", "Creates precise bunds and ridges", "Compatible with various tractor HP ranges"],
     "models": [{"name": "Standard Bund Maker", "specs": "Working width: 4ft | Suitable for: 35-50 HP tractors"},{"name": "Heavy Duty Bund Maker", "specs": "Working width: 5ft | Suitable for: 50-75 HP tractors"},{"name": "Hydraulic Bund Maker", "specs": "Working width: 6ft | Hydraulic operated | 50+ HP"}]},
    {"name": "Seed Drill", "category": "Farm Machinery", "description": "Precision seed drill for accurate seed placement and spacing. Ensures uniform germination and optimal crop yield across various soil types.",
     "benefits": ["Accurate seed placement and uniform spacing", "Suitable for multiple crop types", "Reduces seed wastage significantly"],
     "models": [{"name": "9-Row Seed Drill", "specs": "9 rows | Row spacing: 9 inch | Manual"},{"name": "11-Row Seed Drill", "specs": "11 rows | Row spacing: 9 inch | Automatic"},{"name": "13-Row Seed Drill", "specs": "13 rows | Row spacing: 7.5 inch | Multi-crop"}]},
    {"name": "Rotavator", "category": "Farm Machinery", "description": "High-performance rotavator for thorough soil preparation. Breaks and mixes soil effectively, creating an ideal seedbed for planting.",
     "benefits": ["Thorough soil preparation in a single pass", "Creates ideal seedbed for planting", "Saves time compared to multiple tillage operations"],
     "models": [{"name": "Light Rotavator", "specs": "Working width: 4ft | 35-45 HP | 36 blades"},{"name": "Medium Rotavator", "specs": "Working width: 5ft | 45-55 HP | 42 blades"},{"name": "Heavy Rotavator", "specs": "Working width: 6ft | 55-75 HP | 48 blades"}]},
    {"name": "Cultivator", "category": "Farm Machinery", "description": "Durable cultivator for secondary tillage operations. Effectively loosens soil, controls weeds, and prepares fields for sowing.",
     "benefits": ["Effective weed control between rows", "Loosens compacted soil for better aeration", "Suitable for multiple soil types"],
     "models": [{"name": "Spring Loaded Cultivator", "specs": "9 tynes | Spring loaded | 35-50 HP"},{"name": "Rigid Cultivator", "specs": "11 tynes | Rigid frame | 45-65 HP"},{"name": "Duck Foot Cultivator", "specs": "9 tynes | Duck foot blades | Weed control"}]},
    {"name": "Power Weeder", "category": "Farm Machinery", "description": "Compact and efficient power weeder for inter-row weeding operations. Reduces manual labor and improves weeding efficiency in row crops.",
     "benefits": ["Reduces manual weeding labor significantly", "Compact design for narrow row spacing", "Fuel-efficient and easy to operate"],
     "models": [{"name": "Mini Power Weeder", "specs": "2.5 HP | Petrol | Width: 12 inch"},{"name": "Standard Power Weeder", "specs": "5 HP | Diesel | Width: 18 inch"},{"name": "Heavy Duty Power Weeder", "specs": "7 HP | Diesel | Width: 24 inch"}]},
    {"name": "Earth Auger", "category": "Farm Machinery", "description": "Powerful earth auger for digging holes for tree planting, fencing, and foundation work. Quick and efficient drilling in various soil conditions.",
     "benefits": ["Fast hole digging for planting and fencing", "Works efficiently in various soil types", "Available in hand-held and tractor-mounted options"],
     "models": [{"name": "Hand-held Earth Auger", "specs": "52cc | 2-stroke | Bit dia: 4-12 inch"},{"name": "Tractor Mounted Auger", "specs": "PTO driven | Bit dia: 6-24 inch | 35+ HP"},{"name": "Hydraulic Earth Auger", "specs": "Hydraulic | Bit dia: 6-36 inch | Heavy duty"}]},
    {"name": "Disc Plough", "category": "Farm Machinery", "description": "Robust disc plough for primary tillage in hard and stony soils. Excellent for turning and inverting soil with minimal clogging.",
     "benefits": ["Handles hard and stony soils effectively", "Minimal clogging during operation", "Deep soil turning for better nutrient mixing"],
     "models": [{"name": "2-Disc Plough", "specs": "2 discs | 26 inch dia | 35-45 HP"},{"name": "3-Disc Plough", "specs": "3 discs | 26 inch dia | 45-65 HP"},{"name": "Reversible Disc Plough", "specs": "2 discs | Reversible | Hydraulic | 45+ HP"}]},
    {"name": "Brush Cutter", "category": "Farm Machinery", "description": "Versatile brush cutter for clearing thick grass, weeds, and light brush. Essential for maintaining farm boundaries and clearing overgrown areas.",
     "benefits": ["Clears thick grass and weeds efficiently", "Lightweight with anti-vibration design", "Multiple attachment options for versatility"],
     "models": [{"name": "Backpack Brush Cutter", "specs": "43cc | 2-stroke | Nylon head + blade"},{"name": "Side-hung Brush Cutter", "specs": "52cc | 2-stroke | Metal blade"},{"name": "Heavy Duty Brush Cutter", "specs": "63cc | 4-stroke | Professional grade"}]},
    {"name": "Bio Thresher", "category": "Farm Machinery", "description": "Efficient bio thresher for separating grain from stalks and husks. Suitable for various crops with adjustable speed and output settings.",
     "benefits": ["Separates grain cleanly with minimal loss", "Adjustable speed for different crops", "Available in electric and diesel variants"],
     "models": [{"name": "Mini Thresher", "specs": "5 HP | Electric/Diesel | 200 kg/hr"},{"name": "Standard Thresher", "specs": "10 HP | Multi-crop | 500 kg/hr"},{"name": "Heavy Duty Thresher", "specs": "15 HP | PTO driven | 1000 kg/hr"}]},
    {"name": "Power Sprayer", "category": "Farm Machinery", "description": "High-pressure power sprayer for uniform application of pesticides, herbicides, and fertilizers. Ensures effective crop protection with minimal wastage.",
     "benefits": ["Uniform spray coverage reduces chemical wastage", "High-pressure output for large field areas", "Multiple nozzle options for different applications"],
     "models": [{"name": "Knapsack Sprayer", "specs": "16L tank | Manual | Brass nozzle"},{"name": "Battery Sprayer", "specs": "16L | 12V battery | 4-5 hr runtime"},{"name": "HTP Power Sprayer", "specs": "100L+ | Engine driven | High pressure"}]},
    {"name": "Fertilizer Broadcaster", "category": "Farm Machinery", "description": "Precision fertilizer broadcaster for even distribution of granular fertilizers across fields. Adjustable spread pattern and application rate.",
     "benefits": ["Even fertilizer distribution across fields", "Adjustable spread pattern and rate", "Saves fertilizer and reduces input costs"],
     "models": [{"name": "Manual Broadcaster", "specs": "Hand-operated | 20kg hopper | 5-8m spread"},{"name": "Tractor Mounted Broadcaster", "specs": "PTO driven | 200kg hopper | 12-18m spread"},{"name": "Centrifugal Broadcaster", "specs": "PTO driven | 400kg hopper | 18-24m spread"}]},
    {"name": "Powder Duster", "category": "Farm Machinery", "description": "Effective powder duster for application of dry pesticide and fungicide powders. Lightweight and easy to operate for crop protection.",
     "benefits": ["Effective dry powder application", "Lightweight and portable design", "Ideal for small to medium field coverage"],
     "models": [{"name": "Hand Duster", "specs": "Bellows type | 1kg capacity | Manual"},{"name": "Rotary Duster", "specs": "5kg capacity | Crank operated | Wide reach"},{"name": "Power Duster", "specs": "10kg | Engine driven | High output"}]},

    # Garden Equipment
    {"name": "Chainsaw", "category": "Garden Equipment", "description": "Professional-grade chainsaw for efficient tree felling, pruning, and wood cutting. Equipped with anti-vibration system for comfortable operation.",
     "benefits": ["Powerful cutting for trees and heavy wood", "Anti-vibration system for user comfort", "Quick chain tensioning for easy maintenance"],
     "models": [{"name": "Mini Chainsaw", "specs": "12 inch bar | 25cc | Lightweight"},{"name": "Standard Chainsaw", "specs": "16 inch bar | 45cc | All-purpose"},{"name": "Professional Chainsaw", "specs": "20 inch bar | 62cc | Heavy duty"}]},
    {"name": "Tree Pruner", "category": "Garden Equipment", "description": "Telescopic tree pruner for high-reach pruning without ladders. Sharp blades ensure clean cuts for healthy tree maintenance.",
     "benefits": ["Reach high branches without a ladder", "Clean cuts promote healthy tree growth", "Adjustable telescopic handle"],
     "models": [{"name": "Manual Tree Pruner", "specs": "Telescopic | 6-12ft reach | Rope operated"},{"name": "Electric Tree Pruner", "specs": "Telescopic | 8-14ft | Battery powered"},{"name": "Pole Saw Pruner", "specs": "Petrol | 10-16ft | Chain saw head"}]},
    {"name": "Wheelbarrow", "category": "Garden Equipment", "description": "Sturdy wheelbarrow for transporting soil, compost, plants, and garden materials. Ergonomic design with pneumatic tire for easy maneuverability.",
     "benefits": ["Heavy load capacity for garden materials", "Pneumatic tire for smooth movement", "Rust-resistant and durable build"],
     "models": [{"name": "Standard Wheelbarrow", "specs": "65L capacity | Steel tray | Single wheel"},{"name": "Heavy Duty Wheelbarrow", "specs": "100L capacity | Galvanized | Pneumatic tire"},{"name": "Double Wheel Barrow", "specs": "85L capacity | Two wheels | Stable"}]},
    {"name": "Hedge Trimmer", "category": "Garden Equipment", "description": "Powerful hedge trimmer for shaping and maintaining hedges, shrubs, and ornamental plants with precision and ease.",
     "benefits": ["Precision cutting for neat hedge shapes", "Dual-action blades reduce vibration", "Available in corded, cordless, and petrol variants"],
     "models": [{"name": "Electric Hedge Trimmer", "specs": "18 inch blade | 500W | Corded"},{"name": "Battery Hedge Trimmer", "specs": "22 inch blade | 40V Li-ion | Cordless"},{"name": "Petrol Hedge Trimmer", "specs": "24 inch blade | 26cc | Professional"}]},
    {"name": "Lawn Mower", "category": "Garden Equipment", "description": "Efficient lawn mower for maintaining a well-groomed lawn. Adjustable cutting height and collection bag for a clean finish.",
     "benefits": ["Adjustable cutting height for different grass lengths", "Built-in collection bag for clean operation", "Easy to start and maneuver"],
     "models": [{"name": "Manual Reel Mower", "specs": "14 inch cut | Push type | No fuel"},{"name": "Electric Lawn Mower", "specs": "16 inch cut | 1400W | Corded"},{"name": "Petrol Lawn Mower", "specs": "20 inch cut | Self-propelled | 4-stroke"}]},
    {"name": "Shovel", "category": "Garden Equipment", "description": "Durable garden shovel for digging, lifting, and moving soil, compost, and other materials.",
     "benefits": ["Strong steel blade for tough digging", "Comfortable grip for extended use", "Multiple blade shapes for different tasks"],
     "models": [{"name": "Round Point Shovel", "specs": "Steel blade | Wooden handle"},{"name": "Square Point Shovel", "specs": "Flat blade | Fiberglass handle"},{"name": "Drain Spade", "specs": "Narrow blade | Long handle"}]},
    {"name": "Hoe", "category": "Garden Equipment", "description": "Versatile garden hoe for weeding, cultivating, and shaping soil. Essential hand tool for every gardener.",
     "benefits": ["Effective for weeding and soil shaping", "Lightweight and easy to handle", "Durable steel blade construction"],
     "models": [{"name": "Draw Hoe", "specs": "Standard | Steel blade | Wooden handle"},{"name": "Dutch Hoe", "specs": "Push-pull action | Sharp blade"},{"name": "Stirrup Hoe", "specs": "Oscillating blade | Ergonomic"}]},
    {"name": "Bud Cutter", "category": "Garden Equipment", "description": "Precision bud cutter for clean cutting of plant buds and small stems. Essential for grafting and propagation.",
     "benefits": ["Clean precise cuts for healthy propagation", "Sharp stainless steel blades", "Compact and easy to carry"],
     "models": [{"name": "Standard Bud Cutter", "specs": "Stainless steel | Straight blade"},{"name": "Professional Bud Cutter", "specs": "Carbon steel | Curved blade | Ergonomic"}]},
    {"name": "Rake", "category": "Garden Equipment", "description": "Multi-purpose garden rake for leveling soil, removing debris, and preparing seedbeds.",
     "benefits": ["Effective soil leveling and debris removal", "Available in multiple tine configurations", "Durable and lightweight construction"],
     "models": [{"name": "Bow Rake", "specs": "14 tines | Steel head | Leveling"},{"name": "Leaf Rake", "specs": "22 tines | Fan shape | Lightweight"},{"name": "Landscape Rake", "specs": "36 inch | Aluminum | Grading"}]},
    {"name": "Fork", "category": "Garden Equipment", "description": "Strong garden fork for loosening soil, turning compost, and digging root vegetables.",
     "benefits": ["Loosens compacted soil effectively", "Ideal for turning compost piles", "Forged steel tines for lasting performance"],
     "models": [{"name": "Digging Fork", "specs": "4 tines | Forged steel | D-handle"},{"name": "Border Fork", "specs": "4 tines | Compact | Tight spaces"},{"name": "Compost Fork", "specs": "5 tines | Long handle | Turning"}]},
    {"name": "Grafting Knife", "category": "Garden Equipment", "description": "Sharp grafting knife with precision blade for making clean cuts during grafting operations.",
     "benefits": ["Precision blade for clean grafting cuts", "Folding design for safe storage", "Available with bark lifter option"],
     "models": [{"name": "Standard Grafting Knife", "specs": "Stainless steel | Folding | Single blade"},{"name": "Budding Knife", "specs": "With bark lifter | Carbon steel"},{"name": "Professional Grafting Set", "specs": "Multiple blades | Leather case"}]},
    {"name": "Manual Weeder", "category": "Garden Equipment", "description": "Ergonomic hand weeder for removing weeds without disturbing surrounding plants.",
     "benefits": ["Removes weeds from root level", "Ergonomic design reduces hand fatigue", "Compact for tight garden spaces"],
     "models": [{"name": "Hand Weeder", "specs": "Forked tip | Steel | Short handle"},{"name": "Stand-up Weeder", "specs": "No bending | Long handle | Foot pedal"},{"name": "Cape Cod Weeder", "specs": "L-shaped blade | Precision"}]},
    {"name": "Trowel", "category": "Garden Equipment", "description": "Essential garden trowel for planting, transplanting, and potting with comfortable grip.",
     "benefits": ["Perfect for planting and transplanting", "Marked depth guide for precision", "Sturdy blade for various soil types"],
     "models": [{"name": "Standard Trowel", "specs": "6 inch blade | Steel | Comfortable grip"},{"name": "Transplanting Trowel", "specs": "Narrow blade | Marked depth"},{"name": "Ergonomic Trowel", "specs": "Wide blade | Cushioned grip"}]},
    {"name": "Sickle", "category": "Garden Equipment", "description": "Traditional sickle for harvesting crops and cutting grass with minimal effort.",
     "benefits": ["Efficient grass and crop harvesting", "Curved blade for natural cutting motion", "Lightweight and easy to handle"],
     "models": [{"name": "Plain Sickle", "specs": "Smooth edge | Carbon steel | Light"},{"name": "Serrated Sickle", "specs": "Serrated edge | Stainless steel"}]},
    {"name": "Secateur", "category": "Garden Equipment", "description": "High-quality secateur for precise pruning of stems and branches up to 25mm diameter.",
     "benefits": ["Clean bypass cuts for healthy plant growth", "Ergonomic handle reduces hand strain", "Hardened steel blades for long life"],
     "models": [{"name": "Bypass Secateur", "specs": "Max cut: 20mm | SK5 steel | Ergonomic"},{"name": "Anvil Secateur", "specs": "Max cut: 25mm | Hardened steel"},{"name": "Ratchet Secateur", "specs": "Max cut: 25mm | Ratchet mechanism"}]},
    {"name": "Bypass Pruner", "category": "Garden Equipment", "description": "Professional bypass pruner for clean cuts on live wood and green stems.",
     "benefits": ["Clean cuts on live branches", "Precision-ground blade for smooth operation", "Spring-loaded for easy repeated use"],
     "models": [{"name": "Standard Bypass Pruner", "specs": "Max cut: 20mm | Steel | Spring-loaded"},{"name": "Professional Bypass Pruner", "specs": "Max cut: 25mm | Teflon coated"}]},
    {"name": "Anvil Pruner", "category": "Garden Equipment", "description": "Robust anvil pruner designed for cutting dry and dead wood with extra force.",
     "benefits": ["Extra cutting force for dry and dead wood", "Ratchet mechanism reduces effort", "Durable build for heavy use"],
     "models": [{"name": "Standard Anvil Pruner", "specs": "Max cut: 22mm | Carbon steel"},{"name": "Ratchet Anvil Pruner", "specs": "Max cut: 28mm | 3-step ratchet"}]},
    {"name": "Hedge Shear", "category": "Garden Equipment", "description": "Long-handled hedge shear for trimming and shaping hedges with precision.",
     "benefits": ["Even trimming for neat hedge appearance", "Long handles for comfortable reach", "Precision blades for clean cuts"],
     "models": [{"name": "Standard Hedge Shear", "specs": "8 inch blade | Steel | Wooden handle"},{"name": "Wavy Blade Hedge Shear", "specs": "10 inch | Wavy blade | Non-slip"},{"name": "Telescopic Hedge Shear", "specs": "Adjustable length | Lightweight"}]},
    {"name": "Grafting Machine", "category": "Garden Equipment", "description": "Professional grafting machine for fast and consistent grafting with high success rates.",
     "benefits": ["Consistent V/U/Omega cuts for high graft success", "Fast operation for large-scale nurseries", "Easy blade replacement"],
     "models": [{"name": "Manual Grafting Tool", "specs": "3 blade types | V/U/Omega | Hand-held"},{"name": "Professional Grafting Kit", "specs": "With tape & knife | Complete set"}]},
    {"name": "Nursery Bags", "category": "Garden Equipment", "description": "UV-stabilized nursery bags for plant propagation and seedling growth in various sizes.",
     "benefits": ["UV-treated for extended outdoor durability", "Promotes healthy root development", "Available in multiple sizes"],
     "models": [{"name": "Small Nursery Bags", "specs": "4x6 inch | Pack of 100 | UV treated"},{"name": "Medium Nursery Bags", "specs": "6x8 inch | Pack of 100 | Black poly"},{"name": "Large Nursery Bags", "specs": "8x12 inch | Pack of 50 | Heavy duty"}]},
    {"name": "Flower Pots", "category": "Garden Equipment", "description": "Durable flower pots in various sizes and materials for indoor and outdoor gardening.",
     "benefits": ["Drainage holes for healthy root growth", "Available in plastic, terracotta, and ceramic", "Suitable for indoor and outdoor use"],
     "models": [{"name": "Plastic Pots Set", "specs": "6/8/10 inch | Assorted colors | With tray"},{"name": "Terracotta Pots", "specs": "Various sizes | Natural clay"},{"name": "Ceramic Pots", "specs": "Decorative | Glazed finish"}]},
    {"name": "Grow Bags", "category": "Garden Equipment", "description": "Breathable grow bags for container gardening promoting air pruning for healthier plants.",
     "benefits": ["Breathable fabric promotes root air pruning", "Lightweight and reusable", "Ideal for urban and terrace gardening"],
     "models": [{"name": "Small Grow Bags", "specs": "12x12 inch | 200 GSM | Pack of 10"},{"name": "Medium Grow Bags", "specs": "15x15 inch | 250 GSM | UV treated"},{"name": "Large Grow Bags", "specs": "24x24 inch | 300 GSM | Heavy duty"}]},
    {"name": "Vermibeds", "category": "Garden Equipment", "description": "Ready-to-use vermibeds for efficient vermicomposting and organic compost production.",
     "benefits": ["Produces high-quality organic compost", "Easy setup with stand and liner", "Converts kitchen and garden waste efficiently"],
     "models": [{"name": "Small Vermibed", "specs": "4x2 ft | 200 GSM | With stand"},{"name": "Medium Vermibed", "specs": "6x3 ft | 250 GSM | HDPE liner"},{"name": "Large Vermibed", "specs": "8x4 ft | 300 GSM | Commercial"}]},
    {"name": "Lopping Shear", "category": "Garden Equipment", "description": "Long-reach lopping shear for cutting thick branches up to 50mm with reduced effort.",
     "benefits": ["Cuts branches up to 50mm diameter", "Compound leverage reduces cutting effort", "Extended handles for better reach"],
     "models": [{"name": "Bypass Lopper", "specs": "Max cut: 35mm | 24 inch handles"},{"name": "Anvil Lopper", "specs": "Max cut: 45mm | 28 inch handles | Ratchet"},{"name": "Telescopic Lopper", "specs": "Max cut: 50mm | Extendable handles"}]},
    {"name": "Vertical Garden", "category": "Garden Equipment", "description": "Modular vertical garden system for space-efficient gardening on walls and balconies.",
     "benefits": ["Maximizes growing space in small areas", "Self-watering options available", "Perfect for herbs, flowers, and vegetables"],
     "models": [{"name": "Wall Mount System", "specs": "4 tier | 12 pockets | Self-watering"},{"name": "Free-standing Tower", "specs": "5 tier | 20 pockets | 360 degree"},{"name": "Modular Panel System", "specs": "Stackable | Per panel: 6 pockets"}]},
    {"name": "Root Trays", "category": "Garden Equipment", "description": "Specialized root trays for seedling propagation and easy transplanting.",
     "benefits": ["Optimal cell design for root development", "Reusable and easy to clean", "Available in various cell counts"],
     "models": [{"name": "50-Cell Root Tray", "specs": "50 cells | Reusable | Standard depth"},{"name": "98-Cell Root Tray", "specs": "98 cells | Seedling starter"},{"name": "200-Cell Root Tray", "specs": "200 cells | Micro propagation"}]},

    # Agricultural Inputs
    {"name": "Bone Meal", "category": "Agricultural Inputs", "description": "Premium bone meal fertilizer rich in phosphorus and calcium for strong root development.",
     "benefits": ["High phosphorus content for root strength", "Slow-release organic nutrition", "Promotes flowering and fruiting"],
     "models": [{"name": "Standard Bone Meal", "specs": "N-P-K: 3-15-0 | 5kg pack"},{"name": "Steamed Bone Meal", "specs": "N-P-K: 1-13-0 | 25kg pack"}]},
    {"name": "De-oiled Cakes", "category": "Agricultural Inputs", "description": "Organic de-oiled cakes for soil enrichment and natural pest deterrent.",
     "benefits": ["Rich nitrogen source for plant growth", "Natural pest and nematode deterrent", "Improves soil microbial activity"],
     "models": [{"name": "Neem Cake", "specs": "Organic | 5kg/25kg | Pest deterrent"},{"name": "Castor Cake", "specs": "High NPK | 25kg"},{"name": "Groundnut Cake", "specs": "Protein-rich | 25kg"}]},
    {"name": "Blood Meal", "category": "Agricultural Inputs", "description": "High-nitrogen blood meal for fast-acting soil amendment and leafy plant growth.",
     "benefits": ["Quick-release nitrogen boost", "Excellent for leafy greens", "Organic and natural fertilizer"],
     "models": [{"name": "Standard Blood Meal", "specs": "N: 12-13% | 5kg pack | Quick release"}]},
    {"name": "Vermicompost", "category": "Agricultural Inputs", "description": "Premium vermicompost rich in beneficial microorganisms for improved soil health.",
     "benefits": ["Rich in plant-available nutrients", "Improves soil structure and water retention", "Boosts beneficial soil microorganisms"],
     "models": [{"name": "Standard Vermicompost", "specs": "5kg pack | Sieved | Ready to use"},{"name": "Bulk Vermicompost", "specs": "25kg/50kg bags | Farm grade"},{"name": "Premium Vermicompost", "specs": "10kg | Enriched | Extra nutrients"}]},
    {"name": "Manure", "category": "Agricultural Inputs", "description": "Well-decomposed organic manure for comprehensive soil conditioning and nutrient availability.",
     "benefits": ["Improves soil structure and fertility", "Enhances water retention capacity", "Provides slow-release nutrients"],
     "models": [{"name": "Cow Dung Manure", "specs": "Composted | 25kg"},{"name": "Poultry Manure", "specs": "Dried | 25kg | High nutrient"},{"name": "FYM (Farm Yard Manure)", "specs": "Mixed | 50kg"}]},
    {"name": "Cocopeat", "category": "Agricultural Inputs", "description": "Premium cocopeat growing medium with excellent water retention for seed starting and potting.",
     "benefits": ["Superior water retention and aeration", "pH neutral and eco-friendly", "Ideal for hydroponics and potting mixes"],
     "models": [{"name": "Cocopeat Block", "specs": "5kg block | Expands to 60-70L"},{"name": "Cocopeat Disc", "specs": "Pack of 10 | Pre-buffered"},{"name": "Cocopeat Grow Bag", "specs": "Pre-filled | Ready to plant"}]},
    {"name": "LECA Balls", "category": "Agricultural Inputs", "description": "Lightweight expanded clay aggregate balls for drainage, hydroponics, and decorative mulching.",
     "benefits": ["Prevents waterlogging with excellent drainage", "Reusable and long-lasting", "Ideal for hydroponics and terrace gardens"],
     "models": [{"name": "Small LECA", "specs": "4-8mm | 5L pack | Hydroponics"},{"name": "Medium LECA", "specs": "8-16mm | 10L pack | Drainage layer"},{"name": "Large LECA", "specs": "16-25mm | 25L pack | Mulching"}]},
    {"name": "Artificial Soils", "category": "Agricultural Inputs", "description": "Customized artificial soil mixes for container gardening and specialized cultivation.",
     "benefits": ["Engineered for optimal plant growth", "Sterile and weed-free", "Available for specific plant types"],
     "models": [{"name": "Potting Mix", "specs": "All-purpose | 10kg | Ready to use"},{"name": "Seed Starting Mix", "specs": "Fine texture | 5kg | Sterile"},{"name": "Cactus & Succulent Mix", "specs": "Well-draining | 5kg"}]},
    {"name": "Fish Meal", "category": "Agricultural Inputs", "description": "Organic fish meal fertilizer rich in nitrogen, phosphorus, and trace minerals.",
     "benefits": ["Rich in nitrogen and trace minerals", "Promotes vigorous plant growth", "Boosts soil microbial activity"],
     "models": [{"name": "Standard Fish Meal", "specs": "N-P-K: 10-6-2 | 5kg pack | Organic"}]},

    # Greenhouse
    {"name": "Green Net / Polyfilms", "category": "Greenhouse", "description": "UV-stabilized shade nets and polyfilms for optimal light diffusion and temperature control.",
     "benefits": ["UV-stabilized for long outdoor life", "Controls light and temperature effectively", "Available in multiple shade percentages"],
     "models": [{"name": "35% Shade Net", "specs": "Green | UV treated | Per sqm"},{"name": "50% Shade Net", "specs": "Green/Black | Heavy duty"},{"name": "75% Shade Net", "specs": "Black | Maximum shade"},{"name": "Polyfilm 200 micron", "specs": "Clear/Milky | UV stabilized"}]},
    {"name": "Greenhouse Accessories", "category": "Greenhouse", "description": "Complete range of accessories for greenhouse construction and maintenance.",
     "benefits": ["Compatible with standard greenhouse structures", "Durable materials for long-term use", "Easy installation and replacement"],
     "models": [{"name": "Zigzag Wire & Channel", "specs": "Aluminum | For polyfilm fixing"},{"name": "GI Pipe & Fittings", "specs": "Galvanized | Various sizes"},{"name": "Greenhouse Clips & Clamps", "specs": "UV stable | Polycarb/Metal"}]},
    {"name": "Mulch Films", "category": "Greenhouse", "description": "Agricultural mulch films for weed suppression, moisture retention, and soil temperature regulation.",
     "benefits": ["Suppresses weeds without chemicals", "Retains soil moisture effectively", "Regulates soil temperature for better growth"],
     "models": [{"name": "Black Mulch Film", "specs": "25 micron | 1.2m wide"},{"name": "Silver-Black Mulch", "specs": "30 micron | 1.2m wide | Reflective"},{"name": "Biodegradable Mulch", "specs": "Compostable | 1m wide"}]},
    {"name": "Walk-in Tunnels", "category": "Greenhouse", "description": "Cost-effective walk-in tunnel structures for seasonal crop protection.",
     "benefits": ["Affordable protected cultivation solution", "Easy to install and relocate", "Extends growing season significantly"],
     "models": [{"name": "Small Tunnel", "specs": "3m x 6m | GI frame | Single door"},{"name": "Medium Tunnel", "specs": "4m x 8m | GI frame | Double door"},{"name": "Large Tunnel", "specs": "5m x 15m | Steel frame | Ventilated"}]},
    {"name": "Small Greenhouse", "category": "Greenhouse", "description": "Compact greenhouse structures for nurseries, research, and small-scale protected cultivation.",
     "benefits": ["Complete climate control for sensitive plants", "Ideal for nurseries and research", "Ventilation and covering included"],
     "models": [{"name": "Hobby Greenhouse", "specs": "2m x 3m | Polycarbonate"},{"name": "Nursery Greenhouse", "specs": "4m x 6m | Polyfilm | GI frame"},{"name": "Research Greenhouse", "specs": "6m x 10m | Multi-span"}]},
    {"name": "Propagation Sheets", "category": "Greenhouse", "description": "Clear propagation sheets for maintaining humidity during seed germination.",
     "benefits": ["Maintains optimal humidity levels", "Allows light transmission for growth", "UV treated for extended life"],
     "models": [{"name": "Clear Propagation Sheet", "specs": "Transparent | 100 micron"},{"name": "Frosted Sheet", "specs": "Light diffusing | 150 micron"}]},
    {"name": "Trellis Nets", "category": "Greenhouse", "description": "High-strength trellis nets for vertical crop support in greenhouses.",
     "benefits": ["Strong support for climbing vegetables", "Improves air circulation around plants", "Reusable across multiple seasons"],
     "models": [{"name": "Standard Trellis Net", "specs": "15cm mesh | 1.5m x 10m"},{"name": "Heavy Duty Trellis", "specs": "20cm mesh | 2m x 50m | UV treated"},{"name": "Cucumber/Tomato Net", "specs": "25cm mesh | 1.7m x 100m"}]},

    # Irrigation
    {"name": "Pop-up Sprinklers", "category": "Irrigation", "description": "Automatic pop-up sprinklers that retract flush with ground for clean landscape.",
     "benefits": ["Retract flush when not in use", "Adjustable spray patterns", "Low maintenance and durable"],
     "models": [{"name": "Fixed Pattern Pop-up", "specs": "4 inch rise | 90/180/360 degree"},{"name": "Adjustable Pop-up", "specs": "6 inch rise | 0-360 adjustable"},{"name": "Gear Driven Pop-up", "specs": "4 inch rise | 6-12m radius"}]},
    {"name": "Garden Sprinklers", "category": "Irrigation", "description": "Versatile garden sprinklers for uniform water distribution across lawns and gardens.",
     "benefits": ["Multiple spray patterns available", "Uniform water distribution", "Easy to install and reposition"],
     "models": [{"name": "Impulse Sprinkler", "specs": "Metal | Full/Part circle"},{"name": "Oscillating Sprinkler", "specs": "16 nozzles | Rectangular pattern"},{"name": "Turret Sprinkler", "specs": "6 patterns | Stationary"}]},
    {"name": "Foggers", "category": "Irrigation", "description": "High-pressure foggers for greenhouse humidity control and cooling with ultra-fine mist.",
     "benefits": ["Ultra-fine mist for precise humidity control", "Cools greenhouse temperature effectively", "Anti-drip nozzles prevent overwetting"],
     "models": [{"name": "Single Nozzle Fogger", "specs": "0.5mm orifice | 4 bar | 360 degree"},{"name": "4-Nozzle Fogger", "specs": "Cross pattern | Anti-drip"},{"name": "Dry Fog System", "specs": "Ultra-fine | <10 micron"}]},
    {"name": "Rain Guns", "category": "Irrigation", "description": "Long-range rain guns for irrigating large agricultural fields with high water output.",
     "benefits": ["Covers large field areas efficiently", "Adjustable trajectory and range", "Durable brass and metal construction"],
     "models": [{"name": "Small Rain Gun", "specs": "20-30m range | 1 inch inlet"},{"name": "Medium Rain Gun", "specs": "30-50m range | 1.5 inch"},{"name": "Large Rain Gun", "specs": "50-70m range | 2 inch"}]},
    {"name": "Mini Sprinklers", "category": "Irrigation", "description": "Micro irrigation mini sprinklers for precise watering of individual plants and nursery beds.",
     "benefits": ["Low flow rate reduces water wastage", "Precise watering for individual plants", "Multiple spray patterns available"],
     "models": [{"name": "Micro Jet", "specs": "40-100 LPH | Spike mount | 2-3m radius"},{"name": "Spinner Type", "specs": "60-150 LPH | Rotating | 3-4m radius"},{"name": "Fan Jet", "specs": "35-80 LPH | Strip pattern"}]},
    {"name": "Pumps", "category": "Irrigation", "description": "Reliable water pumps for agricultural and garden irrigation in multiple configurations.",
     "benefits": ["Energy-efficient and reliable operation", "Available in submersible and surface types", "Suitable for various head and flow requirements"],
     "models": [{"name": "Submersible Pump", "specs": "1 HP | Single phase | 15m head"},{"name": "Centrifugal Pump", "specs": "2 HP | Self-priming | 25m head"},{"name": "Monoblock Pump", "specs": "3 HP | High flow | 30m head"}]},
    {"name": "Bell Fountain Sprinkler", "category": "Irrigation", "description": "Decorative bell fountain sprinkler combining irrigation with visual appeal.",
     "benefits": ["Aesthetic water display for gardens", "Functional irrigation with decorative design", "Available in multiple heights and materials"],
     "models": [{"name": "Small Fountain", "specs": "1m height | Brass | 1/2 inch"},{"name": "Medium Fountain", "specs": "1.5m height | Stainless steel"},{"name": "Multi-tier Fountain", "specs": "2m height | 3-tier | 1 inch"}]},
    {"name": "Drip Irrigation", "category": "Irrigation", "description": "Complete drip irrigation systems delivering water directly to plant roots, saving up to 60% water.",
     "benefits": ["Saves up to 60% water vs flood irrigation", "Direct root-zone delivery reduces waste", "Complete kits with filters, valves, and fittings"],
     "models": [{"name": "Inline Drip Kit", "specs": "16mm | 2LPH | For row crops"},{"name": "Online Dripper Kit", "specs": "Individual drippers | Adjustable"},{"name": "Complete Drip System", "specs": "With filter, valves & fittings"}]},
    {"name": "Valves", "category": "Irrigation", "description": "Durable irrigation valves for flow control in manual and automatic configurations.",
     "benefits": ["Precise flow control and system management", "Available in manual and automatic types", "Compatible with all standard pipe sizes"],
     "models": [{"name": "Ball Valve", "specs": "PVC/PP | 1/2 to 4 inch"},{"name": "Solenoid Valve", "specs": "Electric | 1-2 inch | Automatic"},{"name": "Air Release Valve", "specs": "Kinetic | 1-3 inch"}]},
    {"name": "Irrigation Accessories", "category": "Irrigation", "description": "Supporting accessories including filters, joiners, pipes, and fittings for complete irrigation setup.",
     "benefits": ["Complete accessory range for any system", "Durable materials for outdoor conditions", "Easy to install and maintain"],
     "models": [{"name": "Disc Filter", "specs": "1-2 inch | 120 mesh | Backwash"},{"name": "Sand Filter", "specs": "Manual/Auto | 24-48 inch"},{"name": "HDPE Pipe & Fittings", "specs": "20-110mm | PN4-PN6"}]},

    # Miscellaneous
    {"name": "Chakki", "category": "Miscellaneous", "description": "Traditional stone grinding mill for grains and spices in manual and electric variants.",
     "benefits": ["Preserves natural grain nutrition", "Available in manual and electric variants", "Suitable for domestic and commercial use"],
     "models": [{"name": "Manual Stone Chakki", "specs": "12 inch stone | Hand operated"},{"name": "Electric Atta Chakki", "specs": "1 HP | 10-15 kg/hr"},{"name": "Commercial Chakki", "specs": "3 HP | 30-50 kg/hr"}]},
    {"name": "Snake Rescue Kit", "category": "Miscellaneous", "description": "Professional snake rescue kit for safe handling and relocation from farms and residential areas.",
     "benefits": ["Safe and humane snake handling", "Complete kit with tongs, hooks, and bags", "Essential for rural and agricultural zones"],
     "models": [{"name": "Basic Rescue Kit", "specs": "Tongs + Hook + Bag"},{"name": "Professional Kit", "specs": "Tongs + Hook + Tube + Bags"},{"name": "Advanced Kit", "specs": "Full set + Protective gear"}]},
    {"name": "Azola Beds", "category": "Miscellaneous", "description": "Ready-to-use azola beds for producing protein-rich azola as animal feed and green manure.",
     "benefits": ["Produces protein-rich animal feed supplement", "Doubles as green manure for organic farming", "Low maintenance and high yield"],
     "models": [{"name": "Small Azola Bed", "specs": "4x2 ft | Silpaulin | With frame"},{"name": "Medium Azola Bed", "specs": "6x4 ft | HDPE | With stand"},{"name": "Large Azola Bed", "specs": "8x4 ft | Commercial"}]},
    {"name": "Milk Can", "category": "Miscellaneous", "description": "Food-grade stainless steel and aluminum milk cans for safe dairy storage and transport.",
     "benefits": ["Food-grade material ensures safety", "Sealed lid prevents spillage", "Durable for daily commercial use"],
     "models": [{"name": "10L Milk Can", "specs": "Aluminum | With lid"},{"name": "20L Milk Can", "specs": "Stainless steel | Sealed lid"},{"name": "40L Milk Can", "specs": "SS304 | Heavy duty"}]},
    {"name": "Sieve", "category": "Miscellaneous", "description": "Agricultural sieves for grading and sorting seeds, grains, and soil.",
     "benefits": ["Accurate grading for seeds and grains", "Available in multiple mesh sizes", "Durable frame construction"],
     "models": [{"name": "Hand Sieve", "specs": "12 inch | Various mesh"},{"name": "Rotary Sieve", "specs": "Manual | Multi-mesh"},{"name": "Vibrating Sieve", "specs": "Electric | Industrial"}]},
    {"name": "Crocodile Rescue Kit", "category": "Miscellaneous", "description": "Specialized crocodile rescue and handling equipment for wildlife management.",
     "benefits": ["Professional-grade handling equipment", "Safe restraint and capture tools", "Used by forest departments and rescue teams"],
     "models": [{"name": "Standard Rescue Kit", "specs": "Catch pole + Restraint + Tape"},{"name": "Professional Kit", "specs": "Complete handling equipment set"}]},
    {"name": "Monkey Rescue Kit", "category": "Miscellaneous", "description": "Humane monkey rescue kit for safe capture and relocation from farms and orchards.",
     "benefits": ["Humane capture and relocation design", "Collapsible trap for easy transport", "Essential for orchard and farm protection"],
     "models": [{"name": "Trap Cage Kit", "specs": "Humane trap | Collapsible"},{"name": "Net Capture Kit", "specs": "Capture net + Gloves + Carrier"}]},
    {"name": "Leopard Rescue Net", "category": "Miscellaneous", "description": "Heavy-duty leopard rescue net for wildlife rescue operations in rural areas.",
     "benefits": ["High-strength nylon construction", "Professional grade for large animals", "Used by forest departments nationwide"],
     "models": [{"name": "Standard Rescue Net", "specs": "15x15 ft | High-strength nylon"},{"name": "Heavy Duty Net", "specs": "20x20 ft | Kevlar reinforced"}]},
]

CONTACT_INFO = {
    "name": "Navya Enterprises",
    "phone": "+91-9414104098",
    "email": "navyaenterprises73@gmail.com",
    "address": "44F Block, Subcity Centre, Opposite Income-tax Department, Udaipur, Rajasthan 313001",
    "website": "www.navyaenterprises.info",
    "business_timing": "Mon - Sat: 11:00 AM - 7:00 PM"
}

CATEGORIES = ["Farm Machinery", "Garden Equipment", "Agricultural Inputs", "Greenhouse", "Irrigation", "Miscellaneous"]

async def seed_products():
    # Always re-seed to update images and data
    await db.products.drop()
    products_to_insert = []
    for p in PRODUCTS_DATA:
        img = IMG.get(p["name"], "/products/bund_maker.png")
        is_popular = p["name"] in POPULAR_NAMES
        models_with_img = []
        for m in p.get("models", []):
            models_with_img.append({
                "name": m["name"],
                "image": img,
                "specs": m.get("specs", "")
            })
        products_to_insert.append({
            "id": str(uuid.uuid4()),
            "name": p["name"],
            "category": p["category"],
            "description": p["description"],
            "image": img,
            "popular": is_popular,
            "benefits": p.get("benefits", []),
            "models": models_with_img
        })
    await db.products.insert_many(products_to_insert)
    logging.info(f"Seeded {len(products_to_insert)} products with real images")

@app.on_event("startup")
async def startup():
    await seed_products()

@api_router.get("/")
async def root():
    return {"message": "Navya Enterprises API"}

@api_router.get("/products", response_model=List[Product])
async def get_products(category: str = None, popular: bool = None):
    query = {}
    if category:
        query["category"] = category
    if popular is not None:
        query["popular"] = popular
    products = await db.products.find(query, {"_id": 0}).to_list(200)
    return products

@api_router.get("/products/categories")
async def get_categories():
    return CATEGORIES

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api_router.get("/contact-info", response_model=ContactInfo)
async def get_contact_info():
    return CONTACT_INFO

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
