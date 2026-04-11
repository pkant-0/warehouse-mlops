#!/usr/bin/env python3
"""
Inventory Dataset Generator
============================

This script creates a synthetic inventory dataset for the Supply Chain 
Risk Assessment benchmark.

It generates realistic warehouse inventory data with:
- Multiple product categories
- Stockout history
- Safety stock calculations
- Lead times and demand patterns

Author: Benchmark Creator
Date: April 2026
Beginner-Friendly Script
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility (so you get same results each time)
np.random.seed(42)
random.seed(42)

print("📦 Inventory Dataset Generator")
print("=" * 60)
print()

# ============================================================================
# STEP 1: Define Basic Parameters
# ============================================================================
print("Step 1: Setting up parameters...")

NUM_ITEMS = 150  # How many inventory items to create
CATEGORIES = ['Electronics', 'Pharma', 'Groceries', 'Apparel', 'Automotive']

# Create list to store all items
all_items = []

print(f"  ✓ Will create {NUM_ITEMS} items across {len(CATEGORIES)} categories")
print()

# ============================================================================
# STEP 2: Generate Individual Items
# ============================================================================
print("Step 2: Generating inventory items...")

for i in range(NUM_ITEMS):
    # Create unique item ID (ITM10001, ITM10002, etc.)
    item_id = f"ITM{10000 + i + 1}"
    
    # Randomly pick a category
    category = random.choice(CATEGORIES)
    
    # Generate realistic values for different categories
    if category == 'Pharma':
        # Pharma items: higher demand, tighter safety requirements
        daily_demand = round(np.random.uniform(15, 50), 2)
        demand_std_dev = round(daily_demand * 0.2, 2)  # 20% volatility
        lead_time_days = random.choice([2, 3, 4, 5])
        holding_cost = round(np.random.uniform(0.5, 2.5), 2)
    
    elif category == 'Electronics':
        # Electronics: medium demand, moderate costs
        daily_demand = round(np.random.uniform(8, 25), 2)
        demand_std_dev = round(daily_demand * 0.3, 2)  # 30% volatility
        lead_time_days = random.choice([5, 7, 10])
        holding_cost = round(np.random.uniform(1, 3), 2)
    
    elif category == 'Groceries':
        # Groceries: high demand, rapid turnover
        daily_demand = round(np.random.uniform(20, 60), 2)
        demand_std_dev = round(daily_demand * 0.25, 2)  # 25% volatility
        lead_time_days = random.choice([1, 2, 3])
        holding_cost = round(np.random.uniform(0.2, 1), 2)
    
    elif category == 'Apparel':
        # Apparel: seasonal, variable demand
        daily_demand = round(np.random.uniform(10, 40), 2)
        demand_std_dev = round(daily_demand * 0.4, 2)  # 40% volatility (seasonal)
        lead_time_days = random.choice([7, 14, 21])
        holding_cost = round(np.random.uniform(0.3, 1.5), 2)
    
    else:  # Automotive
        # Automotive: low frequency, high value
        daily_demand = round(np.random.uniform(2, 15), 2)
        demand_std_dev = round(daily_demand * 0.35, 2)  # 35% volatility
        lead_time_days = random.choice([3, 5, 7])
        holding_cost = round(np.random.uniform(2, 5), 2)
    
    # Calculate safety stock (protects against 99% of stockouts)
    safety_stock = (daily_demand * lead_time_days) + (2.33 * demand_std_dev * np.sqrt(lead_time_days))
    safety_stock = round(safety_stock, 2)
    
    # Reorder point (when to place new order)
    reorder_point = round(safety_stock * 1.2, 2)
    
    # Current stock level (some items may be low, some healthy)
    # 70% chance of healthy stock, 20% low stock, 10% critical
    stock_level = random.choices(
        [
            round(reorder_point * np.random.uniform(1.5, 3.0), 0),      # Healthy stock
            round(reorder_point * np.random.uniform(0.5, 1.0), 0),      # Low stock
            round(reorder_point * np.random.uniform(0, 0.5), 0)         # Critical stock
        ],
        weights=[0.7, 0.2, 0.1]
    )[0]
    stock_level = max(0, stock_level)  # Can't have negative stock
    
    # Historical stockouts (how many times this item ran out last month)
    # Items with low stock more likely to have stockout history
    if stock_level < reorder_point:
        stockout_count = random.choices([0, 1, 2, 3, 4, 5], weights=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03])[0]
    else:
        stockout_count = random.choices([0, 1, 2], weights=[0.8, 0.15, 0.05])[0]
    
    # Last restock date (when was this item last restocked)
    days_since_restock = random.randint(1, 60)
    last_restock = datetime.now() - timedelta(days=days_since_restock)
    last_restock_str = last_restock.strftime('%Y-%m-%d')
    
    # Create item dictionary
    item = {
        'item_id': item_id,
        'category': category,
        'stock_level': int(stock_level),
        'reorder_point': reorder_point,
        'daily_demand': daily_demand,
        'demand_std_dev': demand_std_dev,
        'lead_time_days': lead_time_days,
        'holding_cost_per_unit_day': holding_cost,
        'last_restock_date': last_restock_str,
        'stockout_count_last_month': stockout_count
    }
    
    all_items.append(item)

print(f"  ✓ Generated {len(all_items)} items")
print()

# ============================================================================
# STEP 3: Create DataFrame
# ============================================================================
print("Step 3: Creating DataFrame...")

df = pd.DataFrame(all_items)

# Show summary statistics
print(f"  ✓ DataFrame created: {df.shape[0]} rows, {df.shape[1]} columns")
print()

# ============================================================================
# STEP 4: Data Quality Checks
# ============================================================================
print("Step 4: Quality checks...")

# Check for nulls
null_count = df.isnull().sum().sum()
print(f"  ✓ Null values: {null_count} (should be 0)")

# Check data types
print(f"  ✓ Categories found: {df['category'].nunique()}")
print(f"    {', '.join(df['category'].unique())}")

# Show some statistics
print(f"  ✓ Stock levels:")
print(f"    - Min: {df['stock_level'].min()}, Max: {df['stock_level'].max()}, Mean: {df['stock_level'].mean():.1f}")
print(f"  ✓ Stockout count:")
print(f"    - Min: {df['stockout_count_last_month'].min()}, Max: {df['stockout_count_last_month'].max()}")

print()

# ============================================================================
# STEP 5: Save to CSV
# ============================================================================
print("Step 5: Saving dataset...")

# Save in current directory
filename = 'inventory_dataset.csv'
df.to_csv(filename, index=False)

# Get file size
import os
file_size = os.path.getsize(filename)
file_size_kb = file_size / 1024

print(f"  ✓ Saved to: {filename}")
print(f"  ✓ File size: {file_size_kb:.1f} KB")
print()

# ============================================================================
# STEP 6: Display Sample Data
# ============================================================================
print("Step 6: Sample data (first 5 items):")
print()
print(df.head().to_string())
print()

# ============================================================================
# STEP 7: Summary
# ============================================================================
print("=" * 60)
print("✓ Dataset generated successfully!")
print("=" * 60)
print()
print("Summary:")
print(f"  • Total items: {len(df)}")
print(f"  • Categories: {df['category'].nunique()}")
print(f"  • Items with stockout history: {(df['stockout_count_last_month'] > 0).sum()}")
print(f"  • Items below reorder point: {(df['stock_level'] < df['reorder_point']).sum()}")
print()
print(f"Ready to use! Upload '{filename}' to your Colab benchmark.")
print()
