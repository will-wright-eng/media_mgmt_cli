import os
import shutil
from pathlib import Path
from zipfile import ZipFile
from typing import List

import yaml


def zip_single_file(filename: str) -> str:
    pathname = str(Path.cwd())
    zip_file = filename.split(".")[0] + ".zip"
    with ZipFile(zip_file, "w") as zipf:
        zipf.write(os.path.join(pathname, filename), arcname=filename)
    return zip_file


def zip_process(file_or_dir: str) -> str:
    p = Path.cwd()
    try:
        # if dir
        dir_name = str(p / file_or_dir)
        zip_path = shutil.make_archive(dir_name, "zip", dir_name)
        return zip_path.split("/")[-1]
    except NotADirectoryError as e:
        # if file
        return zip_single_file(file_or_dir)


def clean_string(string: str) -> str:
    string = "".join(e for e in string if e.isalnum() or e == " " or e == "/")
    string = string.replace("  ", " ").replace("  ", " ").replace(" ", "_")
    return string


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def keyword_in_string(keyword, file):
    if file.lower().find(keyword.lower()) != -1:
        # print ("Contains given substring ")
        return True
    else:
        # print ("Doesn't contains given substring")
        return False


def files_in_media_dir() -> List[str]:
    media_dir = os.getenv("LOCAL_MEDIA_DIR")
    tmp = os.listdir(media_dir)
    tmp = [
        os.listdir(os.path.join(media_dir, folder)) if os.path.isdir(os.path.join(media_dir, folder)) else [folder]
        for folder in tmp
    ]
    return [item for sublist in tmp for item in sublist]


# def create_directories(folders, logger=None):
#     """create_directory docstring"""
#     for folder in folders:
#         try:
#             os.mkdir(folder)
#         except FileExistsError as e:
#             if logger:
#                 logger.info(e)
#             else:
#                 print(e)


# def move_file(file_name, move_to):
#     cwd = Path.cwd()
#     create_directory([str(cwd / move_to)])
#     os.rename(str(cwd / file_name), str(cwd / move_to / file_name))
#     return True


# def load_configs(source):
#     with open(source, "r") as stream:
#         try:
#             data = yaml.safe_load(stream)
#         except Exception as exc:
#             print(exc)
#     return data
