from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bsoup
import time
import re
import pandas as pd

driver = webdriver.Firefox()

# trying to create a tier list where the performance value of the gpu will be its performance 
# relative to the GTX 1050 Ti
url = "https://www.techpowerup.com/gpu-specs/geforce-gtx-1050-ti.c2885"
driver.get(url)
time.sleep(5)
page_html = driver.page_source

# getting the div that contains the relative gpu performance graph
gpu_div = driver.find_element(By.CLASS_NAME,'gpudb-relative-performance__bargraph')
# getting the elements pertaining to each gpu performance bar in the graph
gpu_list_techpowerup = gpu_div.find_elements(By.CLASS_NAME,'gpudb-relative-performance-entry')

gpu_list_techpowerup_text = [gpu_entry.text for gpu_entry in gpu_list_techpowerup]
# separating the performance value and gpu names of each entry
gpu_list_techpowerup_split = [gpu_entry_text.split('\n') for gpu_entry_text in gpu_list_techpowerup_text]
techpowerup_df = pd.DataFrame(data=gpu_list_techpowerup_split,columns=['performance','gpu_name_tpu'])

# the performance values have a '%' in them
techpowerup_df['performance'] = [re.findall(r'\d+',performance_value)[0] for performance_value in techpowerup_df['performance']]
techpowerup_df['performance'] = techpowerup_df['performance'].astype(int)

# gpu_name on the left column, and performance on the right
techpowerup_df = techpowerup_df[['gpu_name_tpu','performance']]

techpowerup_df.to_excel('techpowerup_tier_score.xlsx',sheet_name='tier_score_sheet',index=False)