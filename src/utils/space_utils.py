import huggingface_hub as hf
import pandas as pd

from src.utils import repo_utils
from src.utils.common_utils import run_shell_command
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
        repo_utils.git_clone(repo_id)

        # only take repo that have more than 1 commit.
        if int(run_shell_command(f'cd {repo_folder} && git rev-list --count main')) > 1:
            space_size_dict[repo_id] = get_nloc_count(repo_folder)
        repo_utils.delete_directory(repo_folder)
