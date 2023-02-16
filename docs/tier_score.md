Tier scores are a measure of the performance and value offered by a Graphics Card. There are 3 types of Tier Score in our model, and the basis for them all is the Base Tier 
Score (base_tier_score). The 2 other tier scores based on it are Net Tier Score (net_tier_score) and Non-RT Net Tier Score (non_rt_net_score). Given below are descriptions of
how they are calculated and what they signify:

Base Tier Score:
Base Tier Score is the performance of a Graphics Card relative to the GeForce GTX 1050 Ti, i.e. how much faster it is compared to the GTX 1050 Ti — the least powerful card in
our list of GPU's of interest. It indicates how much more average FPS could be achieved compared to a GTX 1050 Ti across a variety of different games. This is considering
that the GPU's are not bottlenecked by CPU during gaming, and the games are run on the same graphics setting on each of the cards. Also, all ray tracing and hardware specific
upscaling (e.g. DLSS) are turned off. Mathematically, the Base Tier Score can be expressed as:
						base_tier_score = performance of the gpu of interest / performance of the GTX 1050 Ti

To give an example of how it works, the Base Tier Score of the GTX 1660 Ti is 2.15. That means, the GTX 1650 GDDR6 will have 2.15 times higher average FPS across a variety of 
games compared to the GTX 1050 Ti. Also, by this definition, the Base Tier Score of the GTX 1050 Ti will always be 1.

The data for the GPU performance is obtained from Techpowerup's GPU database. The database contains the relative performance of almost all graphics card up to the latest launch.
Following the page for the <a href="https://www.techpowerup.com/gpu-specs/geforce-gtx-1050-ti.c2885">GTX 1050 Ti</a>, a bar graph can be found that indicates all the  relative
performance of all graphics car with a percentage point. This is the relative performance of the cards compared to the GTX 1050 Ti. For example, the GTX 1660 Ti has 215% — meaning
the 1660 Ti has 215% the performance of the GTX 1050 Ti. The GTX 1050 Ti is rated at 100%. As a result, dividing 215% by 100% would result in 2.15, which is the tier score of
the 1660 Ti.

Net Tier Score:
The Net Tier Score is the tier score obtained when the Base Tier Score is adjusted for a GPU's notable positive and negative special traits. Some positive and negative weight scores
are assigned to these positive and negative special traits respectively, which are then divided by 100 to obtain Positive and Negative Score Multipliers respectively. The reason for 
dividing them by 100 is because the weights are meant to be expressed as percentages of the Base Tier Score. The Score Multipliers are then added together to obtain the Overall 
Tier Score Multiplier, which is then multiplied with the Base Tier Score to obtain the Overall Additional Score. Thereafter, Overall Additional Score is added to the Base Tier Score 
to obtain the Net Tier Score. Mathematically:
							overall_score_multiplier = positive_score_multiplier + negative_score_multiplier
								overall_additional_score = base_tier_score * overall_score_multiplier
									net_tier_score = base_tier_score + overall_additional_score

Examples of some of the positive special traits include 2nd generation ray tracing and DLSS for the GeForce RTX 3060 Ti; and the low power consumption of 75 watts for the GTX 
1650. Examples of the notable negative traits include the persistent driver issues of the Intel Arc GPU's (Intel has made a lot of improvements, and they said they would improve
further); and the absence of hardware encoding, along with a host of other issues for the Radeon RX 6500 XT. The idea behind the weight scores is that, gamers would be willing
to pay a higher (or lower for a negative trait) amount of money for a GPU with that trait compared to a GPU with similar specifications but without that trait. For example,
the weight score of 1st generation ray tracing is 5. Thus, the assumption here is that buyers would be willing to pay a 5% higher price for a GPU with 1st generation ray tracing 
than a GPU with similar specs but has no ray tracing. Thus, 1st generation ray tracing is said to increase the value of the GPU by 5%, thereby giving it a net tier score 5% higher
than the base tier score. 

A list of these special positive and negative traits and their weight scores can be found in the 'comment_table' sheet of the <a>tier_score.xlsx</a> Excel file in the 'docs'
folder of this repository. The comment_code column contains a short-hand code for each of the positive and negative traits. The comment_desc column contains a description for
each trait, and the weight_score column contains the weight scores assigned to each of the trait.

The sheet named 'tier_score_sheet' in the tier_score.xlsx file contains the Tier Scores, the positive and negative traits they possess, and their calculated net_tier_score.

Non-RT Net Tier Score:
There are some people who do not consider ray tracing to be such an important trait, that it deserves a premium over similar-specification non-raytracing cards. It is for them
that this tier score is created. Basically, Non-RT Net Tier Score is calculated in the exact same way as Net Tier Score with one exception — the weight scores assigned to first, 
second and third generation ray tracing is 0. All other positive and negative weight scores are kept exactly the same.