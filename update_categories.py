#!/usr/bin/env python3
"""
Script to update categories.yaml with productCount for each child category.
Counts YAML files in the corresponding directories.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple

def get_yaml_files(directory_path: Path) -> Tuple[int, List[str]]:
    """Get the count and list of YAML file names in a directory."""
    if not directory_path.exists() or not directory_path.is_dir():
        return 0, []
    
    yaml_files = sorted(list(directory_path.glob("*.yaml")) + list(directory_path.glob("*.yml")))
    # Get just the filenames, sorted alphabetically
    file_names = sorted([f.name for f in yaml_files])
    return len(file_names), file_names

def find_directory(base_path: Path, category_id: str, child_name: str) -> Path:
    """
    Find the directory for a child category.
    Tries multiple variations: exact match, lowercase, capitalized, etc.
    """
    # Try different case variations
    variations = [
        child_name,
        child_name.lower(),
        child_name.capitalize(),
        child_name.upper(),
    ]
    
    # For controllers, try both the category_id and child_name
    if category_id == "control":
        base_dir = base_path / "control"
    elif category_id == "detection":
        base_dir = base_path / "detection"
    elif category_id == "comms":
        base_dir = base_path / "comms"
    elif category_id == "software":
        base_dir = base_path / "software"
    elif category_id == "cctv":
        base_dir = base_path / "cctv"
    else:
        base_dir = base_path / category_id
    
    # Try each variation
    for variation in variations:
        potential_path = base_dir / variation
        if potential_path.exists() and potential_path.is_dir():
            return potential_path
    
    # If no match found, return the lowercase path (may not exist)
    return base_dir / child_name.lower()

def update_categories_with_counts(categories: List[Dict], base_path: Path) -> List[Dict]:
    """Update categories structure with productCount for each child."""
    updated_categories = []
    
    for category in categories:
        updated_category = category.copy()
        category_id = category.get("id", "")
        
        # Update children if they exist
        if "children" in category and category["children"]:
            updated_children = []
            
            for child in category["children"]:
                # Handle both string and dict children
                if isinstance(child, str):
                    child_id = child.lower()
                    child_name = child
                    # Try to capitalize properly
                    if child_id == "atc":
                        child_name = "ATC"
                    elif child_id == "2070":
                        child_name = "2070"
                    elif child_id == "170":
                        child_name = "170"
                    elif child_id == "radar":
                        child_name = "Radar"
                    elif child_id == "thermal":
                        child_name = "Thermal"
                    elif child_id == "video":
                        child_name = "Video"
                    elif child_id == "hybrid":
                        child_name = "Hybrid"
                    elif child_id == "lidar":
                        child_name = "Lidar"
                    elif child_id == "ptz":
                        child_name = "PTZ"
                    else:
                        child_name = child.capitalize()
                    
                    child_dict = {
                        "id": child_id,
                        "name": child_name
                    }
                else:
                    # Already a dict
                    child_dict = child.copy()
                    child_id = child_dict.get("id", child_dict.get("name", "").lower())
                    child_name = child_dict.get("name", child_id.capitalize())
                
                # Find and get YAML files
                child_dir = find_directory(base_path, category_id, child_id)
                product_count, product_files = get_yaml_files(child_dir)
                
                child_dict["productCount"] = product_count
                if product_files:  # Only add productFiles if there are files
                    child_dict["productFiles"] = product_files
                updated_children.append(child_dict)
            
            updated_category["children"] = updated_children
        
        updated_categories.append(updated_category)
    
    return updated_categories

def main():
    """Main function to update categories.yaml."""
    script_dir = Path(__file__).parent
    categories_file = script_dir / "categories.yaml"
    
    # Read the current categories.yaml
    with open(categories_file, 'r') as f:
        data = yaml.safe_load(f)
    
    if "categories" not in data:
        print("Error: 'categories' key not found in YAML file")
        return
    
    # Update categories with product counts
    updated_categories = update_categories_with_counts(data["categories"], script_dir)
    
    # Create updated data structure
    updated_data = {"categories": updated_categories}
    
    # Write back to file
    with open(categories_file, 'w') as f:
        yaml.dump(updated_data, f, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Successfully updated {categories_file}")
    print(f"Updated {len(updated_categories)} categories with product counts")

if __name__ == "__main__":
    main()