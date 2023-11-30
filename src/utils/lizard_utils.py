import subprocess
import pandas as pd
from io import StringIO
from src.utils.common_utils import run_shell_command


def get_exclusion_directories():
    # files in these directories will not be analyzed by Lizard.
    return ['dataset', 'datasets', 'data', 'test', 'tests']


def create_directory_exclusion_command(folder):
    # Convert the string 'dataset' to a command arg -x"dataset/*"
    return " ".join([f'-x"{folder}/{directory}/*"' for directory in get_exclusion_directories()])


def run_lizard(folder):
    command = f'lizard {folder}/ {create_directory_exclusion_command(folder)} --csv'
    try:
        result = run_shell_command(command)
        return result
    except subprocess.CalledProcessError as err:
        print(f'Returned: {err.returncode}. Failed to run command: {command}')


def get_nloc_count(folder):
    # run lizard and extract NLOC count from the output.
    NLOC_INDEX = 0
    lizard_output = run_lizard(folder)
    if bool(lizard_output.strip()):
        return sum(pd.read_csv(StringIO(lizard_output), sep=',', header=None)[NLOC_INDEX])
    else:
        return 0
