import subprocess
import pandas as pd
from os.path import abspath, dirname

HUGGING_FACE_HOST_URL = 'https://huggingface.co'
PROJECT_DIR = dirname(dirname(dirname(abspath(__file__))))


def run_shell_command(command, check=True):
    return subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE).stdout.decode()


def dict_to_csv(dictionary: dict, path: str, columns=None):
    if columns is None:
        columns = ["repo_id", "size"]
    pd.DataFrame(data=dictionary.items(), columns=columns).to_csv(path, sep=",", encoding="utf-8", index=False)
