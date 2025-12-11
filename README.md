# WhichITS Data

Repository containing product data for Intelligent Transportation Systems (ITS) equipment.

## Structure

Products are organized by category and subcategory:

- **Controllers** - Traffic signal controllers (ATC, 2070, 170)
- **Detection** - Vehicle detection systems (Radar, Thermal, Video, Hybrid, Lidar)
- **Communications** - Network equipment (Edge Switch, Core Switch, Wireless Radio)
- **Software** - ITS software solutions

Each product is defined in a YAML file within its respective category directory.

## Categories File

The `categories.yaml` file provides an overview of all categories, subcategories, product counts, and product file listings. This file is automatically updated by the `update_categories.py` script.

## Updating Categories

The categories file is automatically updated via GitHub Actions when product files are added or modified. You can also run the update script manually:

```bash
pip install -r requirements.txt
python3 update_categories.py
```

## Contributing

Add new products by creating YAML files in the appropriate category subdirectory. The categories file will be automatically updated on the next push.

