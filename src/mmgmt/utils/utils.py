"""
utility functions for general use
Author: William Wright
"""

import os
import yaml


def create_directory(folders, logger=None):
    """create_directory docstring"""
    for folder in folders:
        try:
            os.mkdir(folder)
        except FileExistsError as e:
            if logger:
                logger.info(e)
            else:
                print(e)


def zip_process(cwd, file_name):
    zip_dir = os.path.join(cwd, file_name)
    zip_file = os.path.join(cwd, file_name.replace(".", "_").replace(" ", "_"))
    return shutil.make_archive(zip_file, "zip", zip_dir)


def import_configs():
    config = configparser.ConfigParser()
    config.read("project.cfg")
    config_s3 = dict(config.items("s3_info"))
    config_dir = dict(config.items("dir_info"))
    return (
        config_s3["bucket"],
        config_s3["key_path"],
        config_dir["media_dir"],
        config_dir["move_to"],
    )


def move_uploaded_file(cwd, file_name, move_to):
    utilf.create_directory([cwd + "/" + move_to], logger)
    os.rename(cwd + "/" + file_name, cwd + "/" + move_to + "/" + file_name)


def load_configs(target):
    with open(target, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except Exception as exc:
            print(exc)
    return data


def say_hello():
    print("hi")


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()
