import subprocess
import pandas as pd
from io import StringIO
from common_utils import run_shell_command


def get_exclusion_directories():
    return ['dataset', 'datasets', 'data', 'test', 'tests']


def create_directory_exclusion_command(folder):
    return " ".join([f'-x"{folder}/{directory}/*"' for directory in get_exclusion_directories()])


def run_lizard(folder):
    command = f'lizard {folder}/ {create_directory_exclusion_command(folder)} --csv'
    try:
        result = run_shell_command(command)
        return result
    except subprocess.CalledProcessError as err:
        print(f'Returned: {err.returncode}. Failed to run command: {command}')


def get_nloc_count(folder):
    NLOC_INDEX = 0
    lizard_output = run_lizard(folder)
    if bool(lizard_output.strip()):
        return sum(pd.read_csv(StringIO(lizard_output), sep=',', header=None)[NLOC_INDEX])
    else:
        return 0
