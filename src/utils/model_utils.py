import huggingface_hub as hf


def get_model_filter(task_type):
    return hf.ModelFilter(task=task_type)


def get_model_list(task_type):
    return list(hf.list_models(filter=get_model_filter(task_type), sort='downloads', direction=-1, limit=20))
