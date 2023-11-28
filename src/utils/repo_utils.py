import subprocess
from common_utils import HUGGING_FACE_HOST_URL


def git_clone(repo_id):
    repo_url = HUGGING_FACE_HOST_URL+f'/spaces/{repo_id}'
    try:
        subprocess.run(['git', 'clone', repo_url], check=True)
    except subprocess.CalledProcessError as err:
        print(f'Returned: {err.returncode}. Failed to clone repo: {repo_url}')


def delete_directory(folder):
    try:
        subprocess.run(['rm', f'{folder}/', '-R'], check=True)
    except subprocess.CalledProcessError as err:
        print(f'Returned: {err.returncode}. Failed to delete directory: {folder}/')
