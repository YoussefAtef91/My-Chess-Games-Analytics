# Overview
This personal project aims to analyze 22,000 chess games played on Lichess between May 2020 and March 2023. The project utilizes data science techniques to extract, transform, and analyze the games in order to gain insights into historical performance and identify areas for improvement.

# Methodology:
* Data Extraction: The LichessAPI class was utilized to extract my games in PGN (Portable Game Notation) format.
* Data Transformation: The Wrangle class was used to transforme the PGN file into a tabular format suitable for analysis.
* Data Cleaning: Pre-processing techniques were applied to clean the data, including handling missing values and removing duplicates.
* Analysis: Various data analysis techniques were employed to answer specific questions about my historical chess performance. This includes metrics such as win rate, opening preferences, and performance over time.
Insights and Recommendations: Based on the analysis results, insights were drawn to identify patterns, strengths, and weaknesses in my gameplay. Recommendations for improvement were also provided.

# Key Questions Explored:
1. What is the distribution of the number of games played over time? Do I tend to play more or less at certain times?
2. What is the ditribution of my games' results over time? Do I have more wins or losses at certain times?
3. What is the distribution of my rating's difference overtime? Do I tend to gain or lose more points at certain times?
4. How does my ELO rating evolve over time, and are there any patterns or fluctuations in my rating?
5. What is the distribution of my opponents' ELO ratings? Do I tend to play against higher-rated or lower-rated opponents?
6. What are the most common openings that I play? Do I have more success with certain openings?
7. Do I tend to perform better with certain colors of pieces (e.g., white or black)?
8. What is the distribution of game terminations? Do I tend to win more games by checkmate/resignation or by time forfeit?
9. Are there any correlations between the game result and opponent ELO rating or opponent title?

# Dependencies:
* Python 3.x
* pandas
* scipy
* matplotlib
* plotly
* converter
