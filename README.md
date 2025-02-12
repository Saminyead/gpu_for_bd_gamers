# GPU for Bangladeshi Gamers (Back-end)
You are a Bangladeshi gamer on the hunt to buy a good graphics card for your budget. But without researching the graphics card market, you may be missing out on
the better-performing graphics card that could be bought for less money than the one you are planning to buy! This erratic behavior of the market is partly 
because of the recent increase in the US Dollar prices, and partly due to the rebound from the chip shortage experienced during the Pandemic. Market-research, however,
is time-consuming, and the plethora of options may actually make you more confused. Thus, this data project was created as a live analysis of the GPU (Graphics Processing Unit) market in Bangladesh, and aims to recommend gamers the best graphics cards for their budget.

In order to achieve this, data is collected across the websites of 9 most prominent hardware retailers in Bangladesh using web-scraping. Then the data is
cleaned and loaded onto a database. Only information on GPU's which have performance equal or better than the GTX 1050 Ti are considered "GPU of Interest", and only
pricing information about them are collected. This is because, for gaming, usually integrated graphics serve a better purpose when one is looking to buy a graphics card
in that performance range, hence it is generally better to avoid them.

In order to make proper GPU recommendation, a several tier score values are assigned to each of the GPU's of interest. You can find more about tier scores <a href="https://github.com/Saminyead/gpu_for_bd_gamers/blob/master/docs/tier_score.md">here</a>.
In short, tier scores are a measure for the performance and value offered by a graphics card. Thus, the higher the tier score of a graphics card - the higher its
performance and value. Thus, dividing the price of the graphics card by their tier score would show how much value it offers per unit money. So, if two graphics
card were to be priced similarly, the one with the higher tier score would be recommended.

If you wish to utilize this model to buy a graphics card for yourself, then check out my [web application](https://gpu4bdgamers.streamlit.app). I hope you will
find it useful.
