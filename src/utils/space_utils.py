import huggingface_hub as hf
import pandas as pd
from src.utils.repo_utils import git_clone, delete_directory
from src.utils.common_utils import run_shell_command, dict_to_csv, PROJECT_DIR
from src.utils.lizard_utils import get_nloc_count


def get_space_info_fields_as_list():
    return ['id', 'author', 'sha', 'last_modified', 'private', 'gated', 'disabled', 'host', 'subdomain', 'likes', 'sdk',
            'tags', 'siblings', 'card_data', 'runtime', 'models', 'datasets']


def get_spaces_by_model(model):
    return list(hf.list_spaces(models=model, full=True))


def get_all_spaces(model_list):
    spaces_df = pd.DataFrame(columns=get_space_info_fields_as_list())
    for model in model_list:
        spaces_df = pd.concat([spaces_df, pd.DataFrame(get_spaces_by_model(model.id))], ignore_index=True)
    spaces_df.drop_duplicates(subset=['id'], inplace=True, ignore_index=True)
    return spaces_df


def get_spaces_sizes(space_list):
    ID_INDEX, AUTHOR_INDEX = 0, 1

    space_size_dict = {}

    for space in space_list:
        repo_id, author = space[ID_INDEX], space[AUTHOR_INDEX]

        if not repo_id or not bool(repo_id.strip()):
            continue

        repo_folder = repo_id.replace(f'{author}/', '', 1)
        git_clone(repo_id)

        # only take repo that have more than 1 commit.
        if int(run_shell_command(f'cd {repo_folder} && git rev-list --count main')) > 1:
            space_size_dict[repo_id] = get_nloc_count(repo_folder)
        delete_directory(repo_folder)
    return space_size_dict


def save_and_get_spaces_sizes(space_list: list, model_type: str):
    SLICE_SIZE = 100
    slicer_position = 0

    space_size_dict = {}

    while slicer_position <= len(space_list):
        temp_dict = get_spaces_sizes(space_list[slicer_position:(slicer_position+SLICE_SIZE)])
        space_size_dict.update(temp_dict)
        dict_to_csv(space_size_dict, f"{PROJECT_DIR}/output/{model_type}-space-sizes.csv")
        slicer_position += SLICE_SIZE
    return space_size_dict
