media_mgmt_cli
A simple CLI to manage media in S3

## Table of Contents
1. [Summary](README.md#summary)
2. [Resources](README.md#resources)

### Workflows

upload
	-> search to confirm (check local size is equal to S3 object size) 
	-> optional delete local object

search global 
	-> restore from glacier 
	-> check status 
	-> copy to local once restored

### CLI Features

agrs --operation: 
	uplaod_local (defaults to all in directory), 
	search_global, 
	download, 
	multifile_download

**upload**
- ideal format for naming (title, year, format)
- uplaod individual movies, not collections of movies (TV shows break this rule)

### Process notes

- `pip freeze > requirements.txt`
- `pip install --editable .`

### Resources used

- [boto3 S3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#s3)

## TODO
- add check to see if key already exists, if so then compare size of each
- add wraper that treats `aws s3` as a simple service to upload, download, search_keyword, get_status (storage tier & recovery status), and recover (from glacier)

`<bucket>`

`<keyword>`
```bash
aws s3 ls <bucket>/media_uploads/ | grep "<keyword>"
```

`<filename>`
- recovery tier = Expedited
- recovery days = 10
```bash
aws s3api restore-object --bucket <bucket> --key media_uploads/<filename> --restore-request '{"Days":10,"GlacierJobParameters":{"Tier":"Expedited"}}'

#eg
aws s3api restore-object --bucket <bucket> --key media_uploads/Harry_Potter.zip --restore-request '{"Days":10,"GlacierJobParameters":{"Tier":"Expedited"}}'
```

`<check_status>`
```bash
#eg
aws s3api head-object --bucket <bucket> --key media_uploads/<filename>
```

`<download>`
```bash
#eg
aws s3 cp s3://<bucket>/media_uploads/<filename> <filename>
```

### CLI tookkits

- https://docs.python-guide.org/scenarios/cli/
- https://click.palletsprojects.com/en/8.0.x/
- https://pythonhosted.org/pyCLI/
- https://realpython.com/command-line-interfaces-python-argparse/
- https://medium.com/@shamir.stav_83310/lets-create-a-cli-with-python-part-1-ae4fe9e0258b

### best practices

- virtual environment
```bash
python -m venv ./venv
source venv/bin/activate
```
- yml configs
- logging
- unit tests (and integration tests)