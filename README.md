# GPU for Bangladeshi Gamers (Back-end)
You are a Bangladeshi gamer on the hunt to buy a good graphics card for your budget. But without researching the graphics card market, you may be missing out on
the better-performing graphics card that could be bought for less money than the one you are planning to buy! This erratic behavior of the market is partly 
because of the recent increase in the US Dollar prices, and partly due to the rebound from the chip shortage experienced during the Pandemic. Market-research, however,
is time-consuming, and the plethora of options may actually make you more confused. Thus, this data project was created as a live analysis of the GPU (Graphics Processing Unit) market in Bangladesh, and aims to recommend gamers the best graphics cards for their budget.

In order to achieve this, data was collected across the websites of 9 most prominent hardware retailers in Bangladesh using web-scraping. Thereupon the data was
cleaned and loaded onto a database, as well as an Excel file named 'gpu_of_interest.xlsx', which can be found in the output folder. For now, the data is available only
through this Excel file, containing two sheets named 'lowest_price', 'Sheet1' and 'lowest_prices_tiered'. The 'lowest_price' sheet contains the lowest prices for each
GPU in the market since November 29, 2022; and 'Sheet1' contains the data relating to all 'GPUs of interest' collected at the latest date of data collection. "GPU's of
interest" here refers to the list of graphics card that are, in my opinion, worth spending any money on -- so GPUs like the GT 1030 does not make the list. 

In order to make proper GPU recommendation, a several tier score values are assigned to each of the GPU's of interest. You can find more about tier scores <a href="https://github.com/Saminyead/gpu_for_bd_gamers/blob/master/docs/tier_score.md">here</a>.
In short, tier scores are a measure for the performance and value offered by a graphics card. Thus, the higher the tier score of a graphics card - the higher its
performance and value. Thus, dividing the price of the graphics card by their tier score would show how much value it offers per unit money. So, if two graphics
card were to be priced similarly, the one with the higher tier score would be recommended.

If you wish to utilize this model to buy a graphics card for yourself, then check out my [web application](https://gpu4bdgamers.streamlit.app). I hope you will
find it useful.
