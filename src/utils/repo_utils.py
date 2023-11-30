import subprocess
import platform
from src.utils.common_utils import HUGGING_FACE_HOST_URL


def git_clone(repo_id):
    repo_url = HUGGING_FACE_HOST_URL+f'/spaces/{repo_id}'
    try:
        subprocess.run(f'GIT_LFS_SKIP_SMUDGE=1 git clone --quiet --filter=blob:limit=1m {repo_url}', shell=True, check=True)
    except subprocess.CalledProcessError as err:
        print(f'Returned: {err.returncode}. Failed to clone repo: {repo_url}')


def delete_directory(folder):
    try:
        if platform.system() == 'Linux':
            subprocess.run(['rm', f'{folder}/', '-rf'], check=True)
        elif platform.system() == 'Windows':
            subprocess.run(['rd', '/s', '/q', f'{folder}'], check=True)
    except subprocess.CalledProcessError as err:
        print(f'Returned: {err.returncode}. Failed to delete directory: {folder}/')
