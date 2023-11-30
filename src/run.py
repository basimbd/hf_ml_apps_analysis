from utils.common_utils import PROJECT_DIR
import utils.model_utils as model_utils
import utils.space_utils as space_utils
import pandas as pd
from os import path, makedirs

if not path.exists(f"{PROJECT_DIR}/output"):
    makedirs(f"{PROJECT_DIR}/output")


def get_spaces_df(model_type: str):
    model_list = model_utils.get_model_list(model_type)
    spaces_df = space_utils.get_all_spaces(model_list)
    print(f"==========Total {model_type} spaces: {spaces_df.shape[0]}==========")
    spaces_df.to_csv(f"{PROJECT_DIR}/output/{model_type}-spaces.csv", sep=",", encoding="utf-8", index=False)
    return spaces_df


def get_spaces_and_their_sizes(model_type: str, spaces_df: pd.DataFrame = None):
    if spaces_df is None:
        spaces_df = get_spaces_df(model_type)
    spaces_size_dict = space_utils.save_and_get_spaces_sizes(list(spaces_df.values), model_type)
    print(f'==========analyzed {model_type} spaces: {len(spaces_size_dict)}==========')

    avg_space_size = sum(spaces_size_dict.values())/len(spaces_size_dict)
    print(f'==========Avg {model_type} space size: {avg_space_size}==========')
    return spaces_size_dict


tc_spaces_size_dict = get_spaces_and_their_sizes("text-classification")
tg_spaces_size_dict = get_spaces_and_their_sizes("text-generation")
