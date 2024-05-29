import pandas as pd
from openpyxl import load_workbook
import logging
from dotenv import load_dotenv

from gpu4bdgamers.logger import setup_logging


LOG_FILE = 'overall_tier_score.log'
TIER_SCORE_EXCEL_FILE = 'tier_score.xlsx'

def df_overall_tier_score(
        log_file:str=LOG_FILE,
        tier_score_excel_file:str=TIER_SCORE_EXCEL_FILE
) -> pd.DataFrame:
    setup_logging(log_filename=log_file)

    # fetching the tier_score and comment tables

    tier_score_table = pd.read_excel(io=tier_score_excel_file,sheet_name='tier_score_sheet',usecols='A:G')
    # for some reason it's reading a bunch of blank rows towards the bottom
    overall_tier_score_df = tier_score_table.dropna(axis=0,how='all')
    comment_table = pd.read_excel(io=tier_score_excel_file,sheet_name='comment_table')

    logging.info(f'overall_tier_score_df dataframe created with {len(overall_tier_score_df)} rows')
    logging.info(f'comment_table dataframe created with {len(comment_table)} rows')

    # replace NaN values in positive_comment_code with empty string

    # tier_score are calculated on the comment codes; which are split into individual code using the split method; and NaN values cannot be split
    overall_tier_score_df['positive_comment_code'].fillna('',inplace=True)
    overall_tier_score_df['negative_comment_code'].fillna('',inplace=True)

    logging.info('Nan values in comment code columns replaced with empty string')

    # function to calculate additional score multiplier
    def get_additional_score_multiplier(desc,comment_table_df=comment_table):
        """calculates the multiplier for the additional score from the comment codes

        Args:
            desc (string): all the comment codes for a particular GPU
            comment_table_df (dataframe object, optional): the comment table to use from which reference values for the comment code will be taken from. Defaults to comment_table.

        Returns:
            float: the multiplier for additiona score calculated based on the comment code
        """
        list_desc = desc.split()
        add_score = 0
        for indi_desc in list_desc:
            temp_df = comment_table_df[comment_table_df['comment_code']==indi_desc].reset_index(drop=True)
            add_score = add_score + temp_df['weight_score'][0]
        return add_score/100


    # adding the columns to be calculated

    overall_tier_score_df['positive_score_multiplier'] = overall_tier_score_df['positive_comment_code'].apply(get_additional_score_multiplier)
    logging.info('mutliplier column for positive comment code added')
    overall_tier_score_df['negative_score_multiplier'] = overall_tier_score_df['negative_comment_code'].apply(get_additional_score_multiplier)
    logging.info('mutliplier column for negative comment code added')

    overall_tier_score_df['overall_score_multiplier'] = overall_tier_score_df['positive_score_multiplier'] + overall_tier_score_df['negative_score_multiplier']
    overall_tier_score_df['overall_additional_score'] = overall_tier_score_df['overall_score_multiplier'] * overall_tier_score_df['base_tier_score']
    logging.info('overall_score_multiplier column added')

    overall_tier_score_df['net_tier_score'] = overall_tier_score_df['base_tier_score'] + overall_tier_score_df['overall_additional_score']
    logging.info('net_tier_score column added')

    # to calculate the non-rt overall tier scores

    non_rt_comment_table = comment_table
    non_rt_comment_table.loc[non_rt_comment_table.comment_code.str.contains('rt'),'weight_score'] = 0

    for index, row in non_rt_comment_table.loc[non_rt_comment_table.comment_code.str.contains('rt')].iterrows():
        logging.info(f'{row.comment_code} score set to {row.weight_score} in non_rt_comment_table')


    # non-rt score positive score multiplier has to get scores from non_rt_comment_table
    overall_tier_score_df['non_rt_positive_score_multiplier'] = overall_tier_score_df['positive_comment_code'].apply(get_additional_score_multiplier,args=(non_rt_comment_table,))
    overall_tier_score_df['non_rt_additional_score'] = (overall_tier_score_df['non_rt_positive_score_multiplier'] + overall_tier_score_df['negative_score_multiplier']) * overall_tier_score_df['base_tier_score']

    overall_tier_score_df['non_rt_net_score'] = overall_tier_score_df['base_tier_score'] + overall_tier_score_df['non_rt_additional_score']
    logging.info(f'non-rt net scores calculated, overall_tier_score_df has {len(overall_tier_score_df.columns)} columns')


    # writing overall_tier_score_df to tier_score excel file
    with pd.ExcelWriter(path=tier_score_excel_file,mode='a',engine='openpyxl',if_sheet_exists='replace') as overall_tier_score_writer:
        overall_tier_score_df.to_excel(excel_writer=overall_tier_score_writer,sheet_name='overall_tier_scores')
        overall_tier_score_writer.close

    return overall_tier_score_df


if __name__=="__main__":
    df_overall_tier_score()