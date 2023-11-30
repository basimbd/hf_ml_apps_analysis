from src.utils.common_utils import PROJECT_DIR
import src.utils.model_utils as model_utils
import src.utils.space_utils as space_utils
import pandas as pd
from os import path, makedirs
import shutil
import src.visual.charts_drawer as charts_drawer

if path.exists(f"{PROJECT_DIR}/output"):
    shutil.rmtree(f"{PROJECT_DIR}/output")
makedirs(f"{PROJECT_DIR}/output")


def get_spaces_df(model_type: str):
    """
    Given a model type (text-classification or text-generation) as a parameter,
    fetches all the spaces using that model_type and saves to a CSV file.
    :param model_type:
    :return a DataFrame of spaces using model_type:
    """
    model_list = model_utils.get_model_list(model_type)
    spaces_df = space_utils.get_all_spaces(model_list)
    print(f"==========Total {model_type} spaces: {spaces_df.shape[0]}==========")
    spaces_df.to_csv(f"{PROJECT_DIR}/output/{model_type}-spaces.csv", sep=",", encoding="utf-8", index=False)
    return spaces_df


def get_spaces_and_their_sizes(model_type: str, spaces_df: pd.DataFrame = None):
    """
    Given a model_type, and the spaces using that model, this function returns the code size
    i.e., Non-comment Lines of Code (NLOC) count.
    :param model_type:
    :param spaces_df:
    :return a dictionary where the keys are the space repo_id, and the value is the NLOC count:
    """
    if spaces_df is None:
        spaces_df = get_spaces_df(model_type)
    spaces_size_dict = space_utils.save_and_get_spaces_sizes(list(spaces_df.values), model_type)
    print(f'==========analyzed {model_type} spaces: {len(spaces_size_dict)}==========')

    avg_space_size = sum(spaces_size_dict.values())/len(spaces_size_dict)
    print(f'==========Avg {model_type} space size: {avg_space_size}==========')
    return spaces_size_dict


# Fetch and save all spaces and their code size.
tc_spaces_size_dict = get_spaces_and_their_sizes("text-classification")
tg_spaces_size_dict = get_spaces_and_their_sizes("text-generation")
# Draw and save charts based on the above fetched data.
charts_drawer.draw_space_comparison_box()
charts_drawer.draw_nloc_comparison_bar_chart()
