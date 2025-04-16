import pandas as pd

# Read CSV
df = pd.read_csv('tax.csv')

# Filter taxable events (Sell or Trade)
taxable_events = df[df['Transaction Type'].str.lower().isin(['sell', 'trade'])].copy()

# Convert dates to datetime
taxable_events['Date Acquired'] = pd.to_datetime(taxable_events['Date Acquired'], errors='coerce')
taxable_events['Date of Disposition'] = pd.to_datetime(taxable_events['Date of Disposition'], errors='coerce')

# Group by Asset and aggregate
aggregation = {
    'Date Acquired': 'min',          # First acquisition date
    'Date of Disposition': 'max',    # Last sale date
    'Amount': 'sum',                 # Total quantity sold
    'Proceeds (USD)': 'sum',         # Total proceeds
    'Cost basis (USD)': 'sum',       # Total cost basis
    'Gains (Losses) (USD)': 'sum'    # Net gain/loss
}

grouped = taxable_events.groupby('Asset name', as_index=False).agg(aggregation)

# Rename columns for clarity
grouped = grouped.rename(columns={
    'Date Acquired': 'First Acquired',
    'Date of Disposition': 'Last Sold',
    'Amount': 'Total Quantity Sold',
    'Proceeds (USD)': 'Total Proceeds (USD)',
    'Cost basis (USD)': 'Total Cost Basis (USD)',
    'Gains (Losses) (USD)': 'Net Gain/Loss (USD)'
})

# Format dates
grouped['First Acquired'] = grouped['First Acquired'].dt.strftime('%Y-%m-%d')
grouped['Last Sold'] = grouped['Last Sold'].dt.strftime('%Y-%m-%d')

# Add total summary row
total_row = pd.DataFrame({
    'Asset name': ['TOTAL'],
    'First Acquired': [''],
    'Last Sold': [''],
    'Total Quantity Sold': [grouped['Total Quantity Sold'].sum()],
    'Total Proceeds (USD)': [grouped['Total Proceeds (USD)'].sum()],
    'Total Cost Basis (USD)': [grouped['Total Cost Basis (USD)'].sum()],
    'Net Gain/Loss (USD)': [grouped['Net Gain/Loss (USD)'].sum()]
})

# Combine grouped data with total row
final_summary = pd.concat([grouped, total_row], ignore_index=True)

# Display
print("\n--- TAX SUMMARY BY ASSET ---")
print(final_summary)

# Save to CSV
final_summary.to_csv('tax_summary_with_dates.csv', index=False)