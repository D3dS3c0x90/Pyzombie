# src/core/just_one_time.py
from src.ui import inventory

def add_item_to_inventory(x, y, object, category, player, inventory_group, inventory_category_group, amount=1):
    item = inventory.Item(x, y, object, category, player, inventory_category_group, inventory_group)
    item.inc(amount)
