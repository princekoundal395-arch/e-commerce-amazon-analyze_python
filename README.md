# Amazon Sales Data - Cleaning & Visualization

## Problem Statement
Raw e-commerce sales data is often messy — inconsistent text, wrong data types, and unparsed dates. This project takes a raw Amazon-style sales dataset, cleans it properly with Pandas, and visualizes key business insights (revenue by category, payment method share, monthly sales trend, and price-vs-rating relationship) using Matplotlib.

## Tools Used
- Python
- Pandas (data cleaning & analysis)
- Matplotlib (visualization)

## Dataset
`amazon_csv_100.csv` — 100 e-commerce order records with columns like `user_id`, `product_id`, `category`, `subcategory`, `brand`, `price`, `discount`, `final_price`, `rating`, `review_count`, `stock`, `seller_id`, `seller_rating`, `purchase_date`, `shipping_time_days`, `location`, `device`, `payment_method`, `is_returned`, and `delivery_status`.

## Data Cleaning Steps
1. **Removed duplicate rows** (if any)
2. **Trimmed whitespace** from all text columns
3. **Converted `purchase_date`** from plain text into a proper datetime format (so it can be sorted/grouped by month)
4. **Forced numeric columns** (`price`, `discount`, `final_price`, `rating`, `review_count`, `stock`, `seller_rating`, `shipping_time_days`) to be numeric, catching any stray text/symbols
5. **Dropped unusable rows** that became empty/invalid after cleaning
6. **Sanity-checked values** — removed rows with negative prices or ratings outside the valid 0–5 range
7. Added a helper `purchase_month` column (e.g. `2025-03`) to support the monthly trend chart

> Good news: this particular dataset had **0 missing values** and **0 duplicates** to begin with — the cleaning steps mainly fixed data *types* (text → date/number) rather than removing bad rows.

## Charts Generated
- **Bar chart** — Total revenue by product category
- **Pie chart** — Share of orders by payment method
- **Line chart** — Monthly revenue trend over time
- **Scatter chart** — Price vs. Rating, colored by category

Each chart is shown one at a time using `plt.show()` — close a chart window to move on to the next one.

## Key Insights
- **Electronics dominates revenue**, contributing roughly ₹6.2 lakh of the ~₹9.4 lakh total — far more than any other category (Sports, Home, Clothing, Beauty combined contribute much less).
- **Overall average rating is 3.92**, suggesting decent but not excellent customer satisfaction.
- **Return rate is 12%**, which could be a starting point for deeper investigation (e.g., is one category or payment method driving more returns?).
- The **price vs. rating scatter** shows no strong relationship — expensive Electronics items appear across a wide range of ratings (3.0 to 5.0), so higher price doesn't guarantee a higher rating.
- The **monthly revenue trend** is volatile with sharp spikes (e.g. a big jump around Sept 2024), rather than steady/seasonal growth — worth investigating what drove that spike (bulk orders, a sale event, etc.).

## How to Run
1. Make sure `amazon_csv_100.csv` and `analyze_amazon_data.py` are in the same folder
2. Install requirements: `pip install pandas matplotlib`
3. Run: `python analyze_amazon_data.py`
4. The terminal will print cleaning steps + a summary, then each chart window will pop up one by one — **bar → pie → line → scatter**. Close a chart window to move on to the next one.

## Possible Next Steps
- Break down return rate by category, brand, or payment method
- Analyze delivery performance (`shipping_time_days` vs `delivery_status`)
- Compare seller ratings against product ratings
