import subprocess

HUGGING_FACE_HOST_URL = 'https://huggingface.co'


def run_shell_command(command, check=True):
    return subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE).stdout.decode()
