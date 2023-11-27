import huggingface_hub as hf
import pandas as pd


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
