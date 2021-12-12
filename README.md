# Media Management CLI (mmgmt)

### Table of Contents
1. [Summary](#summary) 
2. [Setup](#setup) 
3. [References](#references) 

## Summary
- this is a hobby project created to ease managment of media assets between local and S3 storage

```bash
% mmgmt --help
Usage: mmgmt [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  delete
  download
  ls
  search
  upload
```

## Setup
- macosx
- conda environemnt: `conda create -n mmgmt python=3.8`
- I use `.envrc` files to manage environment variables between projects
```bash
export AWS_BUCKET=<'insert media bucket'>
export AWS_MEDIA_BUCKET=<'insert media bucket'>
export AWS_BUCKET_PATH=<'insert file prefix'>
export LOCAL_MEDIA_DIR=/path/to/media_dir/
export EDITOR=vi
```

## References
- [pip install -e .](https://stackoverflow.com/questions/35064426/when-would-the-e-editable-option-be-useful-with-pip-install)
- install miniconda: [link](https://docs.conda.io/en/latest/miniconda.html)
- [direnv](https://direnv.net/) for `.envrc` env vars
