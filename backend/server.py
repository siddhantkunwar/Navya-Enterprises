from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# --- Models ---

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
    models: List[ProductModel] = []

class ContactInfo(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    website: str
    business_timing: str

# --- Seed Data ---

PRODUCTS_DATA = [
    # Farm Machinery
    {"name": "Bund Maker", "category": "Farm Machinery", "description": "Heavy-duty bund maker designed for efficient land leveling and water management in agricultural fields. Ideal for creating precise bunds and ridges.", "popular": True,
     "models": [{"name": "Standard Bund Maker", "specs": "Working width: 4ft | Suitable for: 35-50 HP tractors"},{"name": "Heavy Duty Bund Maker", "specs": "Working width: 5ft | Suitable for: 50-75 HP tractors"},{"name": "Hydraulic Bund Maker", "specs": "Working width: 6ft | Hydraulic operated | 50+ HP"}]},
    {"name": "Seed Drill", "category": "Farm Machinery", "description": "Precision seed drill for accurate seed placement and spacing. Ensures uniform germination and optimal crop yield across various soil types.", "popular": True,
     "models": [{"name": "9-Row Seed Drill", "specs": "9 rows | Row spacing: 9 inch | Manual"},{"name": "11-Row Seed Drill", "specs": "11 rows | Row spacing: 9 inch | Automatic"},{"name": "13-Row Seed Drill", "specs": "13 rows | Row spacing: 7.5 inch | Multi-crop"}]},
    {"name": "Rotavator", "category": "Farm Machinery", "description": "High-performance rotavator for thorough soil preparation. Breaks and mixes soil effectively, creating an ideal seedbed for planting.", "popular": True,
     "models": [{"name": "Light Rotavator", "specs": "Working width: 4ft | 35-45 HP | 36 blades"},{"name": "Medium Rotavator", "specs": "Working width: 5ft | 45-55 HP | 42 blades"},{"name": "Heavy Rotavator", "specs": "Working width: 6ft | 55-75 HP | 48 blades"}]},
    {"name": "Cultivator", "category": "Farm Machinery", "description": "Durable cultivator for secondary tillage operations. Effectively loosens soil, controls weeds, and prepares fields for sowing.", 
     "models": [{"name": "Spring Loaded Cultivator", "specs": "9 tynes | Spring loaded | 35-50 HP"},{"name": "Rigid Cultivator", "specs": "11 tynes | Rigid frame | 45-65 HP"},{"name": "Duck Foot Cultivator", "specs": "9 tynes | Duck foot blades | Weed control"}]},
    {"name": "Power Weeder", "category": "Farm Machinery", "description": "Compact and efficient power weeder for inter-row weeding operations. Reduces manual labor and improves weeding efficiency in row crops.", "popular": True,
     "models": [{"name": "Mini Power Weeder", "specs": "2.5 HP | Petrol | Width: 12 inch"},{"name": "Standard Power Weeder", "specs": "5 HP | Diesel | Width: 18 inch"},{"name": "Heavy Duty Power Weeder", "specs": "7 HP | Diesel | Width: 24 inch"}]},
    {"name": "Earth Auger", "category": "Farm Machinery", "description": "Powerful earth auger for digging holes for tree planting, fencing, and foundation work. Quick and efficient drilling in various soil conditions.",
     "models": [{"name": "Hand-held Earth Auger", "specs": "52cc | 2-stroke | Bit dia: 4-12 inch"},{"name": "Tractor Mounted Auger", "specs": "PTO driven | Bit dia: 6-24 inch | 35+ HP"},{"name": "Hydraulic Earth Auger", "specs": "Hydraulic | Bit dia: 6-36 inch | Heavy duty"}]},
    {"name": "Disc Plough", "category": "Farm Machinery", "description": "Robust disc plough for primary tillage in hard and stony soils. Excellent for turning and inverting soil with minimal clogging.",
     "models": [{"name": "2-Disc Plough", "specs": "2 discs | 26 inch dia | 35-45 HP"},{"name": "3-Disc Plough", "specs": "3 discs | 26 inch dia | 45-65 HP"},{"name": "Reversible Disc Plough", "specs": "2 discs | Reversible | Hydraulic | 45+ HP"}]},
    {"name": "Brush Cutter", "category": "Farm Machinery", "description": "Versatile brush cutter for clearing thick grass, weeds, and light brush. Essential for maintaining farm boundaries and clearing overgrown areas.", "popular": True,
     "models": [{"name": "Backpack Brush Cutter", "specs": "43cc | 2-stroke | Nylon head + blade"},{"name": "Side-hung Brush Cutter", "specs": "52cc | 2-stroke | Metal blade"},{"name": "Heavy Duty Brush Cutter", "specs": "63cc | 4-stroke | Professional grade"}]},
    {"name": "Bio Thresher", "category": "Farm Machinery", "description": "Efficient bio thresher for separating grain from stalks and husks. Suitable for various crops with adjustable speed and output settings.",
     "models": [{"name": "Mini Thresher", "specs": "5 HP | Electric/Diesel | 200 kg/hr"},{"name": "Standard Thresher", "specs": "10 HP | Multi-crop | 500 kg/hr"},{"name": "Heavy Duty Thresher", "specs": "15 HP | PTO driven | 1000 kg/hr"}]},
    {"name": "Power Sprayer", "category": "Farm Machinery", "description": "High-pressure power sprayer for uniform application of pesticides, herbicides, and fertilizers. Ensures effective crop protection with minimal wastage.",
     "models": [{"name": "Knapsack Sprayer", "specs": "16L tank | Manual | Brass nozzle"},{"name": "Battery Sprayer", "specs": "16L | 12V battery | 4-5 hr runtime"},{"name": "HTP Power Sprayer", "specs": "100L+ | Engine driven | High pressure"}]},
    {"name": "Fertilizer Broadcaster", "category": "Farm Machinery", "description": "Precision fertilizer broadcaster for even distribution of granular fertilizers across fields. Adjustable spread pattern and application rate.",
     "models": [{"name": "Manual Broadcaster", "specs": "Hand-operated | 20kg hopper | 5-8m spread"},{"name": "Tractor Mounted Broadcaster", "specs": "PTO driven | 200kg hopper | 12-18m spread"},{"name": "Centrifugal Broadcaster", "specs": "PTO driven | 400kg hopper | 18-24m spread"}]},
    {"name": "Powder Duster", "category": "Farm Machinery", "description": "Effective powder duster for application of dry pesticide and fungicide powders. Lightweight and easy to operate for crop protection.",
     "models": [{"name": "Hand Duster", "specs": "Bellows type | 1kg capacity | Manual"},{"name": "Rotary Duster", "specs": "5kg capacity | Crank operated | Wide reach"},{"name": "Power Duster", "specs": "10kg | Engine driven | High output"}]},

    # Garden Equipment
    {"name": "Chainsaw", "category": "Garden Equipment", "description": "Professional-grade chainsaw for efficient tree felling, pruning, and wood cutting. Equipped with anti-vibration system for comfortable operation.", "popular": True,
     "models": [{"name": "Mini Chainsaw", "specs": "12 inch bar | 25cc | Lightweight"},{"name": "Standard Chainsaw", "specs": "16 inch bar | 45cc | All-purpose"},{"name": "Professional Chainsaw", "specs": "20 inch bar | 62cc | Heavy duty"}]},
    {"name": "Tree Pruner", "category": "Garden Equipment", "description": "Telescopic tree pruner for high-reach pruning without ladders. Sharp blades ensure clean cuts for healthy tree maintenance.",
     "models": [{"name": "Manual Tree Pruner", "specs": "Telescopic | 6-12ft reach | Rope operated"},{"name": "Electric Tree Pruner", "specs": "Telescopic | 8-14ft | Battery powered"},{"name": "Pole Saw Pruner", "specs": "Petrol | 10-16ft | Chain saw head"}]},
    {"name": "Wheelbarrow", "category": "Garden Equipment", "description": "Sturdy wheelbarrow for transporting soil, compost, plants, and garden materials. Ergonomic design with pneumatic tire for easy maneuverability.",
     "models": [{"name": "Standard Wheelbarrow", "specs": "65L capacity | Steel tray | Single wheel"},{"name": "Heavy Duty Wheelbarrow", "specs": "100L capacity | Galvanized | Pneumatic tire"},{"name": "Double Wheel Barrow", "specs": "85L capacity | Two wheels | Stable"}]},
    {"name": "Hedge Trimmer", "category": "Garden Equipment", "description": "Powerful hedge trimmer for shaping and maintaining hedges, shrubs, and ornamental plants with precision and ease.", "popular": True,
     "models": [{"name": "Electric Hedge Trimmer", "specs": "18 inch blade | 500W | Corded"},{"name": "Battery Hedge Trimmer", "specs": "22 inch blade | 40V Li-ion | Cordless"},{"name": "Petrol Hedge Trimmer", "specs": "24 inch blade | 26cc | Professional"}]},
    {"name": "Lawn Mower", "category": "Garden Equipment", "description": "Efficient lawn mower for maintaining a well-groomed lawn. Adjustable cutting height and collection bag for a clean finish.", "popular": True,
     "models": [{"name": "Manual Reel Mower", "specs": "14 inch cut | Push type | No fuel"},{"name": "Electric Lawn Mower", "specs": "16 inch cut | 1400W | Corded"},{"name": "Petrol Lawn Mower", "specs": "20 inch cut | Self-propelled | 4-stroke"}]},
    {"name": "Shovel", "category": "Garden Equipment", "description": "Durable garden shovel for digging, lifting, and moving soil, compost, and other materials. Comfortable grip for extended use.",
     "models": [{"name": "Round Point Shovel", "specs": "Steel blade | Wooden handle | All-purpose"},{"name": "Square Point Shovel", "specs": "Flat blade | Fiberglass handle | Scooping"},{"name": "Drain Spade", "specs": "Narrow blade | Long handle | Trenching"}]},
    {"name": "Hoe", "category": "Garden Equipment", "description": "Versatile garden hoe for weeding, cultivating, and shaping soil. Essential hand tool for every gardener and nursery professional.",
     "models": [{"name": "Draw Hoe", "specs": "Standard | Steel blade | Wooden handle"},{"name": "Dutch Hoe", "specs": "Push-pull action | Sharp blade | Weeding"},{"name": "Stirrup Hoe", "specs": "Oscillating blade | Ergonomic | Precision weeding"}]},
    {"name": "Bud Cutter", "category": "Garden Equipment", "description": "Precision bud cutter for clean and accurate cutting of plant buds and small stems. Essential for grafting and propagation work.",
     "models": [{"name": "Standard Bud Cutter", "specs": "Stainless steel | Straight blade"},{"name": "Professional Bud Cutter", "specs": "Carbon steel | Curved blade | Ergonomic"}]},
    {"name": "Rake", "category": "Garden Equipment", "description": "Multi-purpose garden rake for leveling soil, removing debris, and preparing seedbeds. Available in various tine configurations.",
     "models": [{"name": "Bow Rake", "specs": "14 tines | Steel head | Leveling"},{"name": "Leaf Rake", "specs": "22 tines | Fan shape | Lightweight"},{"name": "Landscape Rake", "specs": "36 inch | Aluminum | Grading"}]},
    {"name": "Fork", "category": "Garden Equipment", "description": "Strong garden fork for loosening soil, turning compost, and digging root vegetables. Forged steel tines for lasting performance.",
     "models": [{"name": "Digging Fork", "specs": "4 tines | Forged steel | D-handle"},{"name": "Border Fork", "specs": "4 tines | Compact | Tight spaces"},{"name": "Compost Fork", "specs": "5 tines | Long handle | Turning"}]},
    {"name": "Grafting Knife", "category": "Garden Equipment", "description": "Sharp grafting knife with precision blade for making clean cuts during grafting operations. Essential tool for plant propagation.",
     "models": [{"name": "Standard Grafting Knife", "specs": "Stainless steel | Folding | Single blade"},{"name": "Budding Knife", "specs": "With bark lifter | Carbon steel"},{"name": "Professional Grafting Set", "specs": "Multiple blades | Leather case"}]},
    {"name": "Manual Weeder", "category": "Garden Equipment", "description": "Ergonomic hand weeder for removing weeds from gardens and nursery beds. Designed for easy root extraction without disturbing surrounding plants.",
     "models": [{"name": "Hand Weeder", "specs": "Forked tip | Steel | Short handle"},{"name": "Stand-up Weeder", "specs": "No bending | Long handle | Foot pedal"},{"name": "Cape Cod Weeder", "specs": "L-shaped blade | Precision | One-handed"}]},
    {"name": "Trowel", "category": "Garden Equipment", "description": "Essential garden trowel for planting, transplanting, and potting. Comfortable grip with sturdy blade for various soil types.",
     "models": [{"name": "Standard Trowel", "specs": "6 inch blade | Steel | Comfortable grip"},{"name": "Transplanting Trowel", "specs": "Narrow blade | Marked depth | Precision"},{"name": "Ergonomic Trowel", "specs": "Wide blade | Cushioned grip | Heavy duty"}]},
    {"name": "Sickle", "category": "Garden Equipment", "description": "Traditional sickle for harvesting crops and cutting grass. Curved blade design for efficient cutting with minimal effort.",
     "models": [{"name": "Plain Sickle", "specs": "Smooth edge | Carbon steel | Light"},{"name": "Serrated Sickle", "specs": "Serrated edge | Stainless steel | All-purpose"}]},
    {"name": "Secateur", "category": "Garden Equipment", "description": "High-quality secateur for precise pruning of stems and branches up to 25mm diameter. Bypass mechanism ensures clean, healthy cuts.", "popular": True,
     "models": [{"name": "Bypass Secateur", "specs": "Max cut: 20mm | SK5 steel | Ergonomic"},{"name": "Anvil Secateur", "specs": "Max cut: 25mm | Hardened steel | Dead wood"},{"name": "Ratchet Secateur", "specs": "Max cut: 25mm | Ratchet mechanism | Low effort"}]},
    {"name": "Bypass Pruner", "category": "Garden Equipment", "description": "Professional bypass pruner for clean cuts on live wood and green stems. Precision-ground blade for smooth pruning operations.",
     "models": [{"name": "Standard Bypass Pruner", "specs": "Max cut: 20mm | Steel | Spring-loaded"},{"name": "Professional Bypass Pruner", "specs": "Max cut: 25mm | Teflon coated | Adjustable"}]},
    {"name": "Anvil Pruner", "category": "Garden Equipment", "description": "Robust anvil pruner designed for cutting dry and dead wood. The anvil mechanism provides extra cutting force for tough branches.",
     "models": [{"name": "Standard Anvil Pruner", "specs": "Max cut: 22mm | Carbon steel"},{"name": "Ratchet Anvil Pruner", "specs": "Max cut: 28mm | 3-step ratchet | Easy cut"}]},
    {"name": "Hedge Shear", "category": "Garden Equipment", "description": "Long-handled hedge shear for trimming and shaping hedges and shrubs. Precision blades ensure clean, even cuts for neat appearance.",
     "models": [{"name": "Standard Hedge Shear", "specs": "8 inch blade | Steel | Wooden handle"},{"name": "Wavy Blade Hedge Shear", "specs": "10 inch | Wavy blade | Non-slip"},{"name": "Telescopic Hedge Shear", "specs": "Adjustable length | Lightweight | Comfort grip"}]},
    {"name": "Grafting Machine", "category": "Garden Equipment", "description": "Professional grafting machine for fast and consistent grafting operations. Creates precise V-cut, U-cut, and omega cuts for high success rates.",
     "models": [{"name": "Manual Grafting Tool", "specs": "3 blade types | V/U/Omega | Hand-held"},{"name": "Professional Grafting Kit", "specs": "With tape & knife | Complete set"}]},
    {"name": "Nursery Bags", "category": "Garden Equipment", "description": "UV-stabilized nursery bags for plant propagation and seedling growth. Available in various sizes for different plant requirements.",
     "models": [{"name": "Small Nursery Bags", "specs": "4x6 inch | Pack of 100 | UV treated"},{"name": "Medium Nursery Bags", "specs": "6x8 inch | Pack of 100 | Black poly"},{"name": "Large Nursery Bags", "specs": "8x12 inch | Pack of 50 | Heavy duty"}]},
    {"name": "Flower Pots", "category": "Garden Equipment", "description": "Durable flower pots in various sizes and materials for indoor and outdoor gardening. Drainage holes ensure healthy root development.",
     "models": [{"name": "Plastic Pots Set", "specs": "6/8/10 inch | Assorted colors | With tray"},{"name": "Terracotta Pots", "specs": "Various sizes | Natural clay | Breathable"},{"name": "Ceramic Pots", "specs": "Decorative | Glazed finish | Indoor/Outdoor"}]},
    {"name": "Grow Bags", "category": "Garden Equipment", "description": "Breathable grow bags for container gardening and urban farming. Promotes air pruning of roots for healthier plant growth.",
     "models": [{"name": "Small Grow Bags", "specs": "12x12 inch | 200 GSM | Pack of 10"},{"name": "Medium Grow Bags", "specs": "15x15 inch | 250 GSM | UV treated"},{"name": "Large Grow Bags", "specs": "24x24 inch | 300 GSM | Heavy duty"}]},
    {"name": "Vermibeds", "category": "Garden Equipment", "description": "Ready-to-use vermibeds for efficient vermicomposting. Ideal for producing high-quality organic compost from kitchen and garden waste.",
     "models": [{"name": "Small Vermibed", "specs": "4x2 ft | 200 GSM | With stand"},{"name": "Medium Vermibed", "specs": "6x3 ft | 250 GSM | HDPE liner"},{"name": "Large Vermibed", "specs": "8x4 ft | 300 GSM | Commercial"}]},
    {"name": "Lopping Shear", "category": "Garden Equipment", "description": "Long-reach lopping shear for cutting thick branches up to 50mm. Compound leverage system reduces cutting effort significantly.",
     "models": [{"name": "Bypass Lopper", "specs": "Max cut: 35mm | 24 inch handles | Aluminum"},{"name": "Anvil Lopper", "specs": "Max cut: 45mm | 28 inch handles | Ratchet"},{"name": "Telescopic Lopper", "specs": "Max cut: 50mm | Extendable handles | Compound"}]},
    {"name": "Vertical Garden", "category": "Garden Equipment", "description": "Modular vertical garden system for space-efficient gardening. Perfect for growing herbs, flowers, and vegetables on walls and balconies.",
     "models": [{"name": "Wall Mount System", "specs": "4 tier | 12 pockets | Self-watering"},{"name": "Free-standing Tower", "specs": "5 tier | 20 pockets | 360 degree"},{"name": "Modular Panel System", "specs": "Stackable | Per panel: 6 pockets | Expandable"}]},
    {"name": "Root Trays", "category": "Garden Equipment", "description": "Specialized root trays for seedling propagation and nursery operations. Designed for optimal root development and easy transplanting.",
     "models": [{"name": "50-Cell Root Tray", "specs": "50 cells | Reusable | Standard depth"},{"name": "98-Cell Root Tray", "specs": "98 cells | Seedling starter | Shallow"},{"name": "200-Cell Root Tray", "specs": "200 cells | Micro propagation | Deep cells"}]},

    # Agricultural Inputs
    {"name": "Bone Meal", "category": "Agricultural Inputs", "description": "Premium quality bone meal fertilizer rich in phosphorus and calcium. Promotes strong root development and flowering in all plant types.",
     "models": [{"name": "Standard Bone Meal", "specs": "N-P-K: 3-15-0 | 5kg pack"},{"name": "Steamed Bone Meal", "specs": "N-P-K: 1-13-0 | 25kg pack | Slow release"}]},
    {"name": "De-oiled Cakes", "category": "Agricultural Inputs", "description": "Organic de-oiled cakes (neem, castor, groundnut) for soil enrichment. Excellent source of nitrogen and natural pest deterrent.", "popular": True,
     "models": [{"name": "Neem Cake", "specs": "Organic | 5kg/25kg | Pest deterrent"},{"name": "Castor Cake", "specs": "High NPK | 25kg | Soil enrichment"},{"name": "Groundnut Cake", "specs": "Protein-rich | 25kg | Multi-purpose"}]},
    {"name": "Blood Meal", "category": "Agricultural Inputs", "description": "High-nitrogen blood meal for fast-acting soil amendment. Excellent for leafy greens and nitrogen-hungry plants.",
     "models": [{"name": "Standard Blood Meal", "specs": "N: 12-13% | 5kg pack | Quick release"}]},
    {"name": "Vermicompost", "category": "Agricultural Inputs", "description": "Premium vermicompost produced from earthworm processing. Rich in beneficial microorganisms and plant-available nutrients for improved soil health.", "popular": True,
     "models": [{"name": "Standard Vermicompost", "specs": "5kg pack | Sieved | Ready to use"},{"name": "Bulk Vermicompost", "specs": "25kg/50kg bags | Farm grade"},{"name": "Premium Vermicompost", "specs": "10kg | Enriched | Extra nutrients"}]},
    {"name": "Manure", "category": "Agricultural Inputs", "description": "Well-decomposed organic manure for comprehensive soil conditioning. Improves soil structure, water retention, and nutrient availability.",
     "models": [{"name": "Cow Dung Manure", "specs": "Composted | 25kg | All-purpose"},{"name": "Poultry Manure", "specs": "Dried | 25kg | High nutrient"},{"name": "FYM (Farm Yard Manure)", "specs": "Mixed | 50kg | Bulk"}]},
    {"name": "Cocopeat", "category": "Agricultural Inputs", "description": "Premium cocopeat growing medium for excellent water retention and aeration. Ideal for seed starting, potting mixes, and hydroponic systems.", "popular": True,
     "models": [{"name": "Cocopeat Block", "specs": "5kg block | Expands to 60-70L"},{"name": "Cocopeat Disc", "specs": "Pack of 10 | Individual pots | Pre-buffered"},{"name": "Cocopeat Grow Bag", "specs": "Pre-filled | Ready to plant | UV stable"}]},
    {"name": "LECA Balls", "category": "Agricultural Inputs", "description": "Lightweight expanded clay aggregate (LECA) balls for drainage, hydroponics, and decorative mulching. Promotes root aeration and prevents waterlogging.",
     "models": [{"name": "Small LECA", "specs": "4-8mm | 5L pack | Hydroponics"},{"name": "Medium LECA", "specs": "8-16mm | 10L pack | Drainage layer"},{"name": "Large LECA", "specs": "16-25mm | 25L pack | Mulching"}]},
    {"name": "Artificial Soils", "category": "Agricultural Inputs", "description": "Customized artificial soil mixes for specific growing requirements. Engineered blends for container gardening, raised beds, and specialized cultivation.",
     "models": [{"name": "Potting Mix", "specs": "All-purpose | 10kg | Ready to use"},{"name": "Seed Starting Mix", "specs": "Fine texture | 5kg | Sterile"},{"name": "Cactus & Succulent Mix", "specs": "Well-draining | 5kg | Sandy blend"}]},
    {"name": "Fish Meal", "category": "Agricultural Inputs", "description": "Organic fish meal fertilizer rich in nitrogen, phosphorus, and trace minerals. Promotes vigorous plant growth and soil microbial activity.",
     "models": [{"name": "Standard Fish Meal", "specs": "N-P-K: 10-6-2 | 5kg pack | Organic"}]},

    # Greenhouse
    {"name": "Green Net / Polyfilms", "category": "Greenhouse", "description": "UV-stabilized green shade nets and polyfilms for greenhouse covering. Provides optimal light diffusion and temperature control for protected cultivation.", "popular": True,
     "models": [{"name": "35% Shade Net", "specs": "Green | UV treated | Per sqm"},{"name": "50% Shade Net", "specs": "Green/Black | Heavy duty | Per sqm"},{"name": "75% Shade Net", "specs": "Black | Maximum shade | Per sqm"},{"name": "Polyfilm 200 micron", "specs": "Clear/Milky | UV stabilized | Per sqm"}]},
    {"name": "Greenhouse Accessories", "category": "Greenhouse", "description": "Complete range of greenhouse accessories including clips, joints, channels, and fasteners for greenhouse construction and maintenance.",
     "models": [{"name": "Zigzag Wire & Channel", "specs": "Aluminum | For polyfilm fixing"},{"name": "GI Pipe & Fittings", "specs": "Galvanized | Various sizes"},{"name": "Greenhouse Clips & Clamps", "specs": "UV stable | Polycarb/Metal"}]},
    {"name": "Mulch Films", "category": "Greenhouse", "description": "Agricultural mulch films for weed suppression, moisture retention, and soil temperature regulation. Available in various colors for different applications.",
     "models": [{"name": "Black Mulch Film", "specs": "25 micron | 1.2m wide | Weed control"},{"name": "Silver-Black Mulch", "specs": "30 micron | 1.2m wide | Reflective"},{"name": "Biodegradable Mulch", "specs": "Compostable | 1m wide | Eco-friendly"}]},
    {"name": "Walk-in Tunnels", "category": "Greenhouse", "description": "Cost-effective walk-in tunnel structures for protected cultivation. Easy to install and maintain, suitable for seasonal crop protection.",
     "models": [{"name": "Small Tunnel", "specs": "3m x 6m | GI frame | Single door"},{"name": "Medium Tunnel", "specs": "4m x 8m | GI frame | Double door"},{"name": "Large Tunnel", "specs": "5m x 15m | Steel frame | Ventilated"}]},
    {"name": "Small Greenhouse", "category": "Greenhouse", "description": "Compact greenhouse structures for nurseries, research, and small-scale protected cultivation. Complete with ventilation and covering materials.", "popular": True,
     "models": [{"name": "Hobby Greenhouse", "specs": "2m x 3m | Polycarbonate | Aluminum frame"},{"name": "Nursery Greenhouse", "specs": "4m x 6m | Polyfilm | GI frame"},{"name": "Research Greenhouse", "specs": "6m x 10m | Multi-span | Climate control"}]},
    {"name": "Propagation Sheets", "category": "Greenhouse", "description": "Clear propagation sheets for maintaining humidity and warmth during seed germination and cutting propagation in nursery environments.",
     "models": [{"name": "Clear Propagation Sheet", "specs": "Transparent | 100 micron | Per meter"},{"name": "Frosted Sheet", "specs": "Light diffusing | 150 micron | UV treated"}]},
    {"name": "Trellis Nets", "category": "Greenhouse", "description": "High-strength trellis nets for vertical crop support in greenhouses. Ideal for climbing vegetables, flowers, and vine crops.",
     "models": [{"name": "Standard Trellis Net", "specs": "15cm mesh | 1.5m x 10m | PP"},{"name": "Heavy Duty Trellis", "specs": "20cm mesh | 2m x 50m | UV treated"},{"name": "Cucumber/Tomato Net", "specs": "25cm mesh | 1.7m x 100m | Green"}]},

    # Irrigation
    {"name": "Pop-up Sprinklers", "category": "Irrigation", "description": "Automatic pop-up sprinklers for lawn and garden irrigation. Retract flush with ground when not in use for clean landscape appearance.",
     "models": [{"name": "Fixed Pattern Pop-up", "specs": "4 inch rise | 90/180/360 degree"},{"name": "Adjustable Pop-up", "specs": "6 inch rise | 0-360 adjustable | 4-5m radius"},{"name": "Gear Driven Pop-up", "specs": "4 inch rise | Gear driven | 6-12m radius"}]},
    {"name": "Garden Sprinklers", "category": "Irrigation", "description": "Versatile garden sprinklers for effective and uniform water distribution. Multiple spray patterns for lawns, flower beds, and vegetable gardens.",
     "models": [{"name": "Impulse Sprinkler", "specs": "Metal | Full/Part circle | Spike mount"},{"name": "Oscillating Sprinkler", "specs": "16 nozzles | Rectangular pattern | Adjustable"},{"name": "Turret Sprinkler", "specs": "6 patterns | Stationary | Wide coverage"}]},
    {"name": "Foggers", "category": "Irrigation", "description": "High-pressure foggers for greenhouse humidity control and cooling. Creates ultra-fine mist for optimal growing conditions.", "popular": True,
     "models": [{"name": "Single Nozzle Fogger", "specs": "0.5mm orifice | 4 bar | 360 degree"},{"name": "4-Nozzle Fogger", "specs": "Cross pattern | Anti-drip | Hanging type"},{"name": "Dry Fog System", "specs": "Ultra-fine | <10 micron | No wetting"}]},
    {"name": "Rain Guns", "category": "Irrigation", "description": "Long-range rain guns for irrigation of large agricultural fields. High water output with adjustable trajectory and coverage area.",
     "models": [{"name": "Small Rain Gun", "specs": "20-30m range | 1 inch inlet | Plastic"},{"name": "Medium Rain Gun", "specs": "30-50m range | 1.5 inch | Brass nozzle"},{"name": "Large Rain Gun", "specs": "50-70m range | 2 inch | Full metal"}]},
    {"name": "Mini Sprinklers", "category": "Irrigation", "description": "Micro irrigation mini sprinklers for precise watering of individual plants, tree basins, and nursery beds. Low flow rate with uniform distribution.",
     "models": [{"name": "Micro Jet", "specs": "40-100 LPH | Spike mount | 2-3m radius"},{"name": "Spinner Type", "specs": "60-150 LPH | Rotating | 3-4m radius"},{"name": "Fan Jet", "specs": "35-80 LPH | Strip pattern | Bed irrigation"}]},
    {"name": "Pumps", "category": "Irrigation", "description": "Reliable water pumps for agricultural and garden irrigation. Available in submersible, centrifugal, and monoblock configurations.", "popular": True,
     "models": [{"name": "Submersible Pump", "specs": "1 HP | Single phase | 15m head"},{"name": "Centrifugal Pump", "specs": "2 HP | Self-priming | 25m head"},{"name": "Monoblock Pump", "specs": "3 HP | High flow | 30m head"}]},
    {"name": "Bell Fountain Sprinkler", "category": "Irrigation", "description": "Decorative bell fountain sprinkler for aesthetic water display in gardens and parks. Combines irrigation functionality with visual appeal.",
     "models": [{"name": "Small Fountain", "specs": "1m height | Brass | 1/2 inch inlet"},{"name": "Medium Fountain", "specs": "1.5m height | Stainless steel | 3/4 inch"},{"name": "Multi-tier Fountain", "specs": "2m height | 3-tier | 1 inch inlet"}]},
    {"name": "Drip Irrigation", "category": "Irrigation", "description": "Complete drip irrigation systems for efficient water delivery directly to plant roots. Saves water up to 60% compared to flood irrigation.", "popular": True,
     "models": [{"name": "Inline Drip Kit", "specs": "16mm | 2LPH | For row crops | 1000 sqm"},{"name": "Online Dripper Kit", "specs": "Individual drippers | Adjustable | Trees"},{"name": "Complete Drip System", "specs": "With filter, valves & fittings | Custom area"}]},
    {"name": "Valves", "category": "Irrigation", "description": "Durable irrigation valves for flow control and system management. Available in manual and automatic configurations for all pipe sizes.",
     "models": [{"name": "Ball Valve", "specs": "PVC/PP | 1/2 to 4 inch | Manual"},{"name": "Solenoid Valve", "specs": "Electric | 1-2 inch | Automatic"},{"name": "Air Release Valve", "specs": "Kinetic | 1-3 inch | Pressure rated"}]},
    {"name": "Irrigation Accessories", "category": "Irrigation", "description": "Supporting irrigation accessories including filters, joiners, end caps, mainline pipes, and fittings for complete system setup.",
     "models": [{"name": "Disc Filter", "specs": "1-2 inch | 120 mesh | Backwash"},{"name": "Sand Filter", "specs": "Manual/Auto | 24-48 inch | Heavy duty"},{"name": "HDPE Pipe & Fittings", "specs": "20-110mm | PN4-PN6 | Per meter"}]},

    # Miscellaneous
    {"name": "Chakki", "category": "Miscellaneous", "description": "Traditional stone grinding mill (chakki) for grinding grains, spices, and agricultural produce. Available in manual and electric variants.",
     "models": [{"name": "Manual Stone Chakki", "specs": "12 inch stone | Hand operated | Traditional"},{"name": "Electric Atta Chakki", "specs": "1 HP | 10-15 kg/hr | Domestic"},{"name": "Commercial Chakki", "specs": "3 HP | 30-50 kg/hr | Heavy duty"}]},
    {"name": "Snake Rescue Kit", "category": "Miscellaneous", "description": "Professional snake rescue kit for safe handling and relocation of snakes from agricultural areas, farms, and residential zones.", "popular": True,
     "models": [{"name": "Basic Rescue Kit", "specs": "Tongs + Hook + Bag | Standard"},{"name": "Professional Kit", "specs": "Tongs + Hook + Tube + Bags | Complete"},{"name": "Advanced Kit", "specs": "Full set + Protective gear | Premium"}]},
    {"name": "Azola Beds", "category": "Miscellaneous", "description": "Ready-to-use azola cultivation beds for producing protein-rich azola as animal feed supplement and green manure for organic farming.",
     "models": [{"name": "Small Azola Bed", "specs": "4x2 ft | Silpaulin | With frame"},{"name": "Medium Azola Bed", "specs": "6x4 ft | HDPE | With stand"},{"name": "Large Azola Bed", "specs": "8x4 ft | Commercial | High output"}]},
    {"name": "Milk Can", "category": "Miscellaneous", "description": "Food-grade stainless steel and aluminum milk cans for safe storage and transport of milk and other dairy products.",
     "models": [{"name": "10L Milk Can", "specs": "Aluminum | With lid | Lightweight"},{"name": "20L Milk Can", "specs": "Stainless steel | Sealed lid | Food grade"},{"name": "40L Milk Can", "specs": "SS304 | Heavy duty | Commercial"}]},
    {"name": "Sieve", "category": "Miscellaneous", "description": "Agricultural sieves for grading and sorting seeds, grains, and soil. Various mesh sizes available for different screening requirements.",
     "models": [{"name": "Hand Sieve", "specs": "12 inch | Various mesh | Wooden frame"},{"name": "Rotary Sieve", "specs": "Manual | Multi-mesh | Grain grading"},{"name": "Vibrating Sieve", "specs": "Electric | Industrial | High capacity"}]},
    {"name": "Crocodile Rescue Kit", "category": "Miscellaneous", "description": "Specialized crocodile rescue and handling equipment for wildlife management near water bodies and agricultural zones.",
     "models": [{"name": "Standard Rescue Kit", "specs": "Catch pole + Restraint + Tape"},{"name": "Professional Kit", "specs": "Complete handling equipment set"}]},
    {"name": "Monkey Rescue Kit", "category": "Miscellaneous", "description": "Humane monkey rescue and trapping kit for managing primate intrusion in farms and orchards. Designed for safe capture and relocation.",
     "models": [{"name": "Trap Cage Kit", "specs": "Humane trap | Collapsible | Bait setup"},{"name": "Net Capture Kit", "specs": "Capture net + Gloves + Carrier"}]},
    {"name": "Leopard Rescue Net", "category": "Miscellaneous", "description": "Heavy-duty leopard rescue net for wildlife rescue operations in rural and agricultural areas. Used by forest departments and rescue teams.",
     "models": [{"name": "Standard Rescue Net", "specs": "15x15 ft | High-strength nylon | 4 inch mesh"},{"name": "Heavy Duty Net", "specs": "20x20 ft | Kevlar reinforced | Professional"}]},
]

CONTACT_INFO = {
    "name": "Navya Enterprises",
    "phone": "+91-9414104098",
    "email": "navyaenterprises73@gmail.com",
    "address": "44F Block, Subcity Centre, Opposite Income-tax Department, Udaipur, Rajasthan 313001",
    "website": "www.navyaenterprises.info",
    "business_timing": "Mon - Sat: 10:00 AM - 7:00 PM"
}

CATEGORIES = ["Farm Machinery", "Garden Equipment", "Agricultural Inputs", "Greenhouse", "Irrigation", "Miscellaneous"]

# Dummy images per category
CATEGORY_IMAGES = {
    "Farm Machinery": "https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=600&h=400&fit=crop",
    "Garden Equipment": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=400&fit=crop",
    "Agricultural Inputs": "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=600&h=400&fit=crop",
    "Greenhouse": "https://images.unsplash.com/photo-1770982699065-4d631e37186f?w=600&h=400&fit=crop",
    "Irrigation": "https://images.unsplash.com/photo-1769927954927-13ffa6b7756c?w=600&h=400&fit=crop",
    "Miscellaneous": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=600&h=400&fit=crop",
}

async def seed_products():
    count = await db.products.count_documents({})
    if count > 0:
        return
    
    products_to_insert = []
    for i, p in enumerate(PRODUCTS_DATA):
        cat = p["category"]
        base_img = CATEGORY_IMAGES.get(cat, "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=600&h=400&fit=crop")
        models_with_img = []
        for m in p.get("models", []):
            models_with_img.append({
                "name": m["name"],
                "image": base_img,
                "specs": m.get("specs", "")
            })
        products_to_insert.append({
            "id": str(uuid.uuid4()),
            "name": p["name"],
            "category": cat,
            "description": p["description"],
            "image": base_img,
            "popular": p.get("popular", False),
            "models": models_with_img
        })
    
    await db.products.insert_many(products_to_insert)
    logging.info(f"Seeded {len(products_to_insert)} products")

@app.on_event("startup")
async def startup():
    await seed_products()

# --- Routes ---

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
        from fastapi import HTTPException
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
