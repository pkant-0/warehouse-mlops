"""
Simple Dataset Generator
Creates inventory_dataset.csv for the Inventory Risk Assessment benchmark.

This script generates realistic warehouse inventory data with:
- 100 inventory items across multiple categories
- Realistic demand patterns with variability
- Historical stockout data
- Location and cost information

Just run: python generate_inventory_data.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

print("📊 Generating Inventory Dataset...")
print("-" * 50)

# Number of items to generate
num_items = 100

# Generate item IDs
item_ids = [f'ITM{10000 + i}' for i in range(num_items)]

# Categories for items
categories = ['Electronics', 'Pharma', 'Groceries', 'Apparel', 'Automotive']

# Generate dataset
data = {
    'item_id': item_ids,
    'category': np.random.choice(categories, num_items),
    'stock_level': np.random.randint(5, 500, num_items),
    'reorder_point': np.random.randint(20, 100, num_items),
    'daily_demand': np.random.uniform(10, 100, num_items).round(2),
    'demand_std_dev': np.random.uniform(1, 20, num_items).round(2),
    'lead_time_days': np.random.randint(2, 14, num_items),
    'holding_cost_per_unit_day': np.random.uniform(0.1, 5, num_items).round(2),
    'last_restock_date': [
        (datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime('%Y-%m-%d') 
        for _ in range(num_items)
    ],
    'stockout_count_last_month': np.random.randint(0, 10, num_items),
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_file = 'inventory_dataset.csv'
df.to_csv(output_file, index=False)

print(f"✓ Dataset created: {output_file}")
print(f"✓ Total items: {len(df)}")
print(f"✓ Categories: {', '.join(df['category'].unique())}")
print(f"✓ File size: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

print("\n📋 Dataset Preview (first 5 rows):")
print(df.head())

print("\n✓ Ready to use in benchmark!")
