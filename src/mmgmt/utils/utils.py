import os
import yaml


def clean_string(string: str) -> str:
    string = "".join(e for e in string if e.isalnum() or e == " " or e == "/")
    string = string.replace("  ", " ").replace("  ", " ").replace(" ", "_")
    return string


def zip_process(file_or_dir: str) -> str:
    cwd = str(Path.cwd())
    zip_source = os.path.join(cwd, file_or_dir)
    zip_target = os.path.join(cwd, clean_string(file_or_dir))
    return shutil.make_archive(zip_target, "zip", zip_source)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


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
