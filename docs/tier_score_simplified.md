This document contains a simplified explanation of the Tier Score system. For full details, check out tier_score.md <a href="https://github.com/Saminyead/gpu_for_bd_gamers/blob/master/docs/tier_score.md">here</a>.

Tier Scores are a way to measure the performance of graphics cards. Three types of Tier Scores have been developed - Base Tier Score, Net Tier Score, and Non-RT Tier Score.
Base Tier Score measures raw performance value, while Net and Non-RT Tier Scores measure weighted performance values.

Think of it like this: if you're comparing the speed of different cars, you might use miles per hour as your baseline measurement. But if you're also interested in factors
like fuel efficiency or cargo space, you might use a weighted measurement that takes those factors into account. The same idea applies to graphics cards and Tier Scores.

Base Tier Score is like miles per hour - it's a straightforward measurement of how fast a graphics card can go. Net and Non-RT Tier Scores are like weighted measurements 
that take other factors into account, such as power consumption or ray tracing performance.

<H3>Base Tier Score</H3>
The Base Tier Score is obtained by comparing the performance of a graphics card to the performance of the GeForce GTX 1050 Ti, which is the least powerful card in our list
of GPUs of interest. It measures how many times more average FPS a GPU can output, relative to the GeForce GTX 1050 Ti across a variety of different games. Which means, 
it is expressed as a ratio where a score of 1 means the card has the same performance as the GTX 1050 Ti, and a score higher than 1 means the card is faster.


For example, if the Base Tier Score of a graphics card is 2.15, it means that the card can output an average FPS that's 2.15 times higher than the GTX 1050 Ti across
different games. It's important to note that this calculation assumes that the graphics card is not bottlenecked by the CPU during gaming, and that the games 
are run on the same graphics setting on each of the cards. Additionally, all ray tracing and hardware-specific upscaling (such as DLSS) are turned off.

<H3>Net Tier Score</H3>
The Net Tier Score is a measure of the weighted performance of a graphics card, adjusting the Base Tier Score for positive and negative special traits. Each trait is 
assigned a weight score, based on the assumption that gamers are willing to pay a higher (or lower for negative traits) amount of money for a GPU with that trait. For 
example, a weight score of 5 is assigned to 1st generation ray tracing, which means that a GPU with this trait is assumed to increase its value by 5% compared to
a GPU with similar specs but no ray tracing. 

The weight scores are then used to calculate Positive and Negative Score Multipliers, which are added together to obtain the Overall Tier Score Multiplier. This is then 
multiplied with the Base Tier Score to obtain the Overall Additional Score, which is added to the Base Tier Score to obtain the Net Tier Score. Mathematically, it looks
like the following:

                                  overall_score_multiplier = positive_score_multiplier + negative_score_multiplier
                                            overall_additional_score = base_tier_score * overall_score_multiplier
                                          net_tier_score = base_tier_score + overall_additional_score

Examples of positive traits include ray tracing and DLSS, while notable negative traits include persistent driver issues or the absence of hardware encoding.
A list of these traits and their weight scores can be found in the 'comment_table' sheet of the <a href="https://github.com/Saminyead/gpu_for_bd_gamers/blob/master/tier_score.xlsx">
  tier_score.xlsx</a> file.
  
<H3>Non-RT Tier Score</H3>
The Non-RT Tier Score is designed for buyers who don't think that ray tracing is a feature worth paying more for. It's calculated the same way as the Net Tier Score, except
that the weight scores for first, second, and third generation ray tracing are zero. All other positive and negative weight scores are the same.
