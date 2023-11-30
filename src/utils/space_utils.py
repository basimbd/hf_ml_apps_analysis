import huggingface_hub as hf
import pandas as pd
from src.utils.repo_utils import git_clone, delete_directory
from src.utils.common_utils import run_shell_command, dict_to_csv, PROJECT_DIR
from src.utils.lizard_utils import get_nloc_count


def get_space_info_fields_as_list():
    """
    returns the field names of SpaceInfo object. It is used to map a SpaceInfo object to DataFrame header.
    :return:
    """
    return ['id', 'author', 'sha', 'last_modified', 'private', 'gated', 'disabled', 'host', 'subdomain', 'likes', 'sdk',
            'tags', 'siblings', 'card_data', 'runtime', 'models', 'datasets']


def get_spaces_by_model(model):
    """
    Given a single model, fetches all the spaces using this model.
    :param model:
    :return List of SpaceInfo objects:
    """
    return list(hf.list_spaces(models=model, full=True))


def get_all_spaces(model_list):
    """
    Given a list of models, fetch all the spaces using all those models.
    :param model_list:
    :return a DataFrame of the spaces using the models in the model_list:
    """
    spaces_df = pd.DataFrame(columns=get_space_info_fields_as_list())
    for model in model_list:
        spaces_df = pd.concat([spaces_df, pd.DataFrame(get_spaces_by_model(model.id))], ignore_index=True)
    # A single space can use multiple models. And therefore, can be included multiple times (one time for each model).
    # So, it is necessary that the duplicates are removed and only one instance of a space is kept.
    spaces_df.drop_duplicates(subset=['id'], inplace=True, ignore_index=True)
    return spaces_df


def get_spaces_sizes(space_list):
    """
    Given a list of spaces, calculate the NLOC count for each of the space.
    :param space_list:
    :return A dictionary where key is the space repo_id, and value is the NLOC count:
    """
    ID_INDEX, AUTHOR_INDEX = 0, 1

    space_size_dict = {}

    for space in space_list:
        repo_id, author = space[ID_INDEX], space[AUTHOR_INDEX]

        # check if repo_id is not blank.
        if not repo_id or not bool(repo_id.strip()):
            continue

        repo_folder = repo_id.replace(f'{author}/', '', 1)
        git_clone(repo_id)

        # only take repo that have more than 1 commit.
        if int(run_shell_command(f'cd {repo_folder} && git rev-list --count main')) > 1:
            space_size_dict[repo_id] = get_nloc_count(repo_folder)
        delete_directory(repo_folder)       # after running lizard, the repo is removed.
    return space_size_dict


def save_and_get_spaces_sizes(space_list: list, model_type: str):
    # SLICE_SIZE variable means that the program will save the CSV in 100 batch size.
    # In other words, after analyzing every 100 spaces, will save the NLOC count to a CSV.
    SLICE_SIZE = 100
    slicer_position = 0

    space_size_dict = {}

    while slicer_position <= len(space_list):
        temp_dict = get_spaces_sizes(space_list[slicer_position:(slicer_position+SLICE_SIZE)])
        space_size_dict.update(temp_dict)
        dict_to_csv(space_size_dict, f"{PROJECT_DIR}/output/{model_type}-space-sizes.csv")
        slicer_position += SLICE_SIZE
    return space_size_dict
