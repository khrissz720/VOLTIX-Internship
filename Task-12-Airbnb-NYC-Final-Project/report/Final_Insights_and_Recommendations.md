# Final Insights & Recommendations — Airbnb NYC

**Data scope:** only the supplied `AB_NYC_2019.csv`; historical 2019 snapshot.

## 1. Supply concentration
- **Finding:** Manhattan has the most listings (21,661).
- **Meaning:** supply is geographically concentrated; competitive conditions may differ by borough and neighbourhood.
- **Recommendation:** benchmark within neighbourhood and room type, not only city-wide.

## 2. Geographic price differences
- **Finding:** highest borough median is Manhattan ($150); lowest is Bronx ($65).
- **Meaning:** location is associated with different advertised prices, but this is not proof of causation.
- **Recommendation:** compare medians and distributions by neighbourhood and room type.

## 3. Room-type segmentation
- **Finding:** Entire home/apt is the most common room type (25,409 listings).
- **Recommendation:** use separate benchmarks and dashboard filters for each room type.

## 4. Price quality and skew
- **Finding:** median price is $106; 2,972 listings are above the IQR upper fence and 11 have a zero price.
- **Meaning:** averages can be distorted by a long upper tail and questionable values.
- **Recommendation:** report medians/percentiles, inspect flagged rows, and retain source values until validated.

## 5. Reviews are not ratings or occupancy
- **Finding:** Pearson correlation between price and review count is -0.048.
- **Meaning:** this describes a linear association only; review counts depend on exposure and other factors.
- **Recommendation:** do not infer rating, occupancy, or profitability from review counts.

## 6. Important data limitation
- The dataset has no guest-rating score, actual bookings, realized revenue, or occupancy. The requested rating-price relationship cannot be tested directly.
- The data is from 2019, so it should not be presented as current market pricing.

## Decision summary
Prioritize neighbourhood- and room-type-level price benchmarks, monitor data-quality flags, and communicate medians alongside means. Treat the findings as descriptive evidence, not causal proof or a current-market forecast.
