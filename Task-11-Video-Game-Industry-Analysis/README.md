\# Video Game Industry Analysis



\## Overview



This project analyzes video game sales data to identify market trends, top-performing genres, platforms, publishers, games, and regional markets.



The project also compares the performance of \*\*PlayStation 4 (PS4)\*\* and \*\*Xbox One\*\* using platform-specific datasets.



The analysis was developed as part of the \*\*VOLTIX Internship Program — Data Analysis Track\*\* using Python and Power BI.



\---



\## Objectives



\- Understand the structure and quality of the video game datasets.

\- Clean and prepare the datasets for analysis.

\- Explore sales by genre, platform, publisher, game, year, and region.

\- Analyze the relationship between critic scores and global sales.

\- Compare PS4 and Xbox One performance.

\- Create an interactive Power BI dashboard.

\- Extract insights and provide recommendations based on the analysis.



\---



\## Dataset



The project uses three datasets:



\- `Video\_Games\_Sales\_as\_at\_22\_Dec\_2016.csv`

\- `PS4\_GamesSales.csv`

\- `XboxOne\_GameSales.csv`



The main dataset contains information about video games, including:



\- Game name

\- Platform

\- Release year

\- Genre

\- Publisher

\- Regional sales

\- Global sales

\- Critic score

\- User score

\- Developer

\- Rating



The PS4 and Xbox One datasets are analyzed separately for platform-specific comparisons.



\---



\## Data Cleaning



The datasets were cleaned using Python.



The cleaning process included:



\- Handling missing values.

\- Converting numerical columns to appropriate data types.

\- Converting release years to numeric values.

\- Handling invalid sales values.

\- Converting `User\_Score` values such as `tbd` to missing values.

\- Replacing missing publisher, developer, and rating values with `Unknown`.

\- Removing exact duplicate records.

\- Exporting cleaned datasets as CSV files.



\### Cleaned datasets



\- `video\_games\_sales\_cleaned.csv`

\- `ps4\_games\_sales\_cleaned.csv`

\- `xboxone\_games\_sales\_cleaned.csv`



\---



\## Exploratory Data Analysis



The exploratory analysis was performed using Python.



The analysis covers:



\- Genre distribution

\- Sales by genre

\- Sales by platform

\- Sales by publisher

\- Top-selling games

\- Sales trends by year

\- Regional sales

\- Critic score vs. global sales

\- PS4 vs. Xbox One comparison



\---



\# Visualizations



\## Genre Distribution



!\[Genre Distribution](visualizations/genre\_distribution.png)



This visualization shows the distribution of games across different genres. \*\*Action\*\* is the most common genre in the dataset.



\---



\## Global Sales by Genre



!\[Sales by Genre](visualizations/sales\_by\_genre.png)



Action generates the highest global sales among genres, followed by Sports and Shooter.



\---



\## Global Sales by Platform



!\[Sales by Platform](visualizations/sales\_by\_platform.png)



The visualization compares total global sales across gaming platforms. \*\*PS2\*\* is the highest-selling platform in the main dataset.



\---



\## Global Sales by Publisher



!\[Sales by Publisher](visualizations/sales\_by\_publisher.png)



The analysis shows that \*\*Nintendo\*\* is the highest-selling publisher in the main dataset.



\---



\## Top 10 Best-Selling Games



!\[Top 10 Games](visualizations/top\_10\_games.png)



The visualization highlights the ten best-selling games in the dataset. \*\*Wii Sports\*\* is the highest-selling title.



\---



\## Global Sales Trend



!\[Sales Trend](visualizations/sales\_trend.png)



The sales trend shows the evolution of global video game sales over time. The highest observed annual sales occur in \*\*2008\*\*.



> Note: The dataset is a December 2016 snapshot, so the later decline should not be interpreted as a complete or current industry trend.



\---



\## Regional Sales



!\[Regional Sales](visualizations/regional\_sales.png)



North America represents the largest regional market in the dataset, followed by Europe and Japan.



\---



\## Critic Score vs. Global Sales



!\[Rating vs Sales](visualizations/rating\_vs\_sales.png)



The relationship between critic scores and global sales is positive but relatively weak, indicating that critic scores alone do not strongly determine commercial performance.



\---



\# Power BI Dashboard



The interactive dashboard was developed using \*\*Microsoft Power BI\*\*.



\## Page 1 — Video Game Market Overview



The first dashboard provides an overview of the global video game market.



\### Key Performance Indicators



\- \*\*Total Games:\*\* 11,562

\- \*\*Total Global Sales:\*\* 8,917.88 million

\- \*\*Top Genre:\*\* Action

\- \*\*Top Platform:\*\* PS2

\- \*\*Top Publisher:\*\* Nintendo



\### Dashboard Visuals



\- Global Sales Trend by Year

\- Global Sales by Genre

\- Global Sales by Region

\- Top 10 Best-Selling Games

\- Interactive filters for:

&#x20; - Year

&#x20; - Genre

&#x20; - Platform

&#x20; - Publisher

&#x20; - Rating



\---



\## Page 2 — PS4 vs Xbox One Market Comparison



The second dashboard compares the PS4 and Xbox One platforms.



\### Key Performance Indicators



\- \*\*PS4 Games:\*\* 1,034

\- \*\*Xbox One Games:\*\* 613

\- \*\*PS4 Global Sales:\*\* 595.64 million

\- \*\*Xbox One Global Sales:\*\* 269.03 million



\### Comparison Visuals



\- PS4 vs Xbox One Global Sales

\- Global Sales by Genre

\- Top 10 Publishers

\- Global Sales Trend

\- Number of Games Released by Year



Within these datasets, PS4 global sales are approximately \*\*2.21 times higher\*\* than Xbox One global sales.



\---



\# Key Insights



\### Genre Performance



Action is the most common genre, with \*\*3,370 games\*\*, and also generates the highest global sales at approximately \*\*1,745.27 million units\*\*.



Sports is the second most common genre and generates approximately \*\*1,332.00 million units\*\*, while Shooter generates approximately \*\*1,052.94 million units\*\*.



\### Platform Performance



PS2 is the highest-selling platform in the main dataset, with approximately \*\*1,255.64 million units\*\* in global sales.



Other historically important platforms include Xbox 360, PS3, Wii, DS, and the original PlayStation.



\### Publisher Performance



Nintendo is the highest-selling publisher, with approximately \*\*1,788.81 million units\*\* in global sales.



It is followed by:



1\. Nintendo — 1,788.81 M

2\. Electronic Arts — 1,116.96 M

3\. Activision — 731.16 M



\### Best-Selling Game



\*\*Wii Sports\*\* is the highest-selling game in the dataset, with approximately \*\*82.53 million units\*\*.



\### Sales Trend



Global sales reached the highest observed annual value in \*\*2008\*\*, with approximately \*\*671.79 million units\*\*.



\### Regional Performance



North America is the largest regional market:



\- North America — 4,400.84 M

\- Europe — 2,424.14 M

\- Japan — 1,297.40 M

\- Other Regions — 791.26 M



\### Critic Scores



The correlation between Critic Score and Global Sales is approximately \*\*0.2455\*\*, representing a weak positive relationship.



This suggests that critic scores alone are not a strong predictor of commercial success.



\---



\# PS4 vs Xbox One Insights



The PS4 dataset contains \*\*1,034 games\*\* and approximately \*\*595.64 million units\*\* in global sales.



The Xbox One dataset contains \*\*613 games\*\* and approximately \*\*269.03 million units\*\*.



Within these datasets, PS4 global sales are approximately \*\*2.21 times higher\*\* than Xbox One global sales.



\### PS4



The leading genres by global sales are:



\- Action — 136.85 M

\- Shooter — 134.99 M

\- Sports — 92.85 M

\- Role-Playing — 62.82 M



The highest-selling publisher is \*\*Activision\*\*, with approximately \*\*72.44 million units\*\*.



\### Xbox One



The leading genres by global sales are:



\- Shooter — 92.21 M

\- Action — 50.51 M

\- Sports — 42.43 M

\- Racing — 17.97 M



The highest-selling publisher is \*\*Microsoft Studios\*\*, with approximately \*\*44.61 million units\*\*.



\---



\# Recommendations



\### 1. Prioritize High-Demand Genres



Publishers and developers should consider high-performing genres such as Action, Sports, Shooter, and Role-Playing when evaluating market opportunities.



\### 2. Adapt Strategies to Platform Characteristics



Genre and publisher performance differs between PS4 and Xbox One. Marketing, distribution, and release strategies should therefore be adapted to each platform.



\### 3. Focus on Strong Regional Markets



North America represents the largest sales region. Regional marketing and localization strategies should consider differences between North America, Europe, Japan, and other markets.



\### 4. Do Not Rely on Critic Scores Alone



Since the relationship between critic scores and global sales is relatively weak, commercial decisions should consider multiple factors, including:



\- Genre

\- Platform

\- Publisher

\- Historical sales

\- Regional performance

\- User feedback



\### 5. Study Successful Franchises and Publishers



The concentration of high-selling games and publishers provides useful benchmarks for evaluating future projects and understanding successful market strategies.



\### 6. Consider Data Limitations



The main dataset is a \*\*December 2016 snapshot\*\* and contains missing values in several fields.



Future analysis could incorporate:



\- More recent sales data

\- Digital sales

\- Player engagement

\- Pricing

\- Marketing expenditure

\- Post-launch performance



\---



\# Project Structure



```text

Task-11-Video-Game-Industry-Analysis/

│

├── data/

│   ├── PS4\_GamesSales.csv

│   ├── Video\_Games\_Sales\_as\_at\_22\_Dec\_2016.csv

│   ├── XboxOne\_GameSales.csv

│   ├── video\_games\_sales\_cleaned.csv

│   ├── ps4\_games\_sales\_cleaned.csv

│   └── xboxone\_games\_sales\_cleaned.csv

│

├── analysis/

│   ├── video\_game\_analysis.py

│   └── video\_game\_eda.py

│

├── visualizations/

│   ├── genre\_distribution.png

│   ├── sales\_by\_genre.png

│   ├── sales\_by\_platform.png

│   ├── sales\_by\_publisher.png

│   ├── top\_10\_games.png

│   ├── sales\_trend.png

│   ├── regional\_sales.png

│   ├── rating\_vs\_sales.png

│   │

│   ├── genre\_game\_count.csv

│   ├── sales\_by\_genre.csv

│   ├── sales\_by\_platform.csv

│   ├── sales\_by\_publisher.csv

│   ├── top\_20\_games.csv

│   ├── sales\_by\_year.csv

│   ├── regional\_sales.csv

│   ├── ps4\_vs\_xbox\_one.csv

│   └── kpi\_summary.csv

│

├── Insights-and-Recommendations.docx

├── Video-Game-Industry-Analysis.pbix

└── README.md

