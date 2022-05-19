# config.py
# ## pseudo code for environment variable check
# --> objective is to generate a dictionary of environment variables
# either from aws secrets, local os, or command line inputs

# export AWS_BUCKET=<'insert media bucket'>
# export AWS_MEDIA_BUCKET=<'insert media bucket'>
# export AWS_BUCKET_PATH=<'insert file prefix'>
# export LOCAL_MEDIA_DIR=<'insert /path/to/media_dir/'>
# export EDITOR=vi

import os
from click import echo

# what all is needed to get the CLI up and working locally
env_vars = [
    "AWS_BUCKET",
    "AWS_MEDIA_BUCKET",
    "AWS_BUCKET_PATH",
    "LOCAL_MEDIA_DIR",
    "EDITOR",
]

# AWS secrets
def get_secrets() -> dict:
    """retrieve secrets from aws using boto3"""
    # create connection to AWS secrets resource
    # s3_resour = boto3.resource("s3")
    # s3_client = boto3.client("s3")
    return resp


def write_secrets(env_vars: dict):
    """write secrets to aws"""
    return resp


# # examples
# env_var = os.environ.get('ENV', 'DEFAULT_VALUE')
# env_var_exists = 'ENV' in os.environ

# check
def check_local():
    present = []
    not_present = []
    for var in env_vars:
        if var not in os.environ:
            not_present.append(var)
            # get env vars from AWS secrets
        else:
            present.append(var)
    return present, not_present


def determine_action():
    action = input(
        f"""Vars missing from local env vars: {', '.join(not_preesent)}

How would you like to proceed?
[1] manually enter environment variables (w/ option to push to AWS Secrets)
[2] retrieve from AWS Secrets
[3] export and retry config setup
"""
    )
    if action in (1, 2, 3):
        return action
    else:
        echo("invalid entry... try again")
        return determine_action()


present, not_present = check_local()
# what would you like to do?
if len(present) == len(env_vars):
    # all required vars are present
    pass
else:
    # more needed
    action = determine_action()
