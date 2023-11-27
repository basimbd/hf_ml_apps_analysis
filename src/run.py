from utils import model_utils, space_utils
import pandas as pd

tc_model_list = model_utils.get_model_list('text-classification')
tg_model_list = model_utils.get_model_list('text-generation')

tc_spaces_df = space_utils.get_all_spaces(tc_model_list)
tg_spaces_df = space_utils.get_all_spaces(tg_model_list)

common_spaces_df = pd.DataFrame(tc_spaces_df.loc[tc_spaces_df['id'].isin(tg_spaces_df['id']), :])
common_spaces_df.reset_index(drop=True, inplace=True)

print(f"TC spaces: {tc_spaces_df.shape[0]}")
print(f"TG spaces: {tg_spaces_df.shape[0]}")
print(f"Common spaces: {common_spaces_df.shape[0]}")
