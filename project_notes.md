# media_mgmt_cli
A simple CLI to manage media files locally and in S3

## Table of Contents
1. [Summary](README.md#summary)
2. [To Do](README.md#todo)
3. [Notes](README.md#notes)

## Summary
This is a summary

## TODO
### bugs
- correct upload command: adjust `.envrc` in media directory to have the correct `bucket` and `object_name`; add `object_name` env var to `media_mgmt_cli` `.envrc` for testing
- remove parenthesis from file names -- causes error when calling object name in zsh, treating the parens as an array
### search features
- search includes movies streaming via [tmdb](https://developers.themoviedb.org/3/search/search-movies) or [movie of the night](https://www.movieofthenight.com/about/api) free api service
- include torrents (bot that logs into revolutiontt and runs search, scrape and display results; eg [torrent search api](https://github.com/JimmyLaurent/torrent-search-api) or [this one](https://www.npmjs.com/package/torrent-search-api))
### upload features
- check to see if S3 object key already exists, if so then compare size of each
- checksum or hash to confirm file upload fully completed
### download features
- copy/paste from a search is arduious --> add feature, input("download from search list? [Y/n] "), assign numbers to each result in list, input("choose object to download (by number):"), wrapping object name in quotes
### database/storage
- symetrically encrypt file name with farnet key when storing on cloud (who has access?) ([renaming S3 objects](https://stackoverflow.com/questions/21184720/how-to-rename-files-and-folder-in-amazon-s3))
- metadata & caching: 
	- store results from each search in db -- add historical search feature
	- write run_id and meta information to mysql database as an alternative to search **OR** provision a postgres database on AWS and use postio to access --> write simple sqlalchemy class to interact with db
- transactions table(s)
	- `upload` | file_name | source | target | checksum_source | checksum_upload_verified (bool)| upload_date | file_type | file_count | dir_levels
	- `download` | source | file_name | download_date
	- `search`
	- `torrents` | tracker | download_date | 
- store torrent trackers (also, how the fuck do they work?)
- move all S3 media objects to Glacier flexible recovery storage
### setup media computer
- search and download files accross machines on local network
- [ssh into machine](https://superuser.com/questions/413718/how-to-connect-2-macs-via-ssh-on-a-home-network), list files in media directory, zip file, then [scp to local machine](https://stackoverflow.com/questions/68335/how-to-copy-a-file-to-a-remote-server-in-python-using-scp-or-ssh)

## Notes
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
	uplaod_local (defaults to all in cwd, unless --name specified), 
	search (default to --location = global), 
	download, 
	multifile_download

**upload**
- ideal format for naming (title, year, format)
- uplaod individual movies, not collections of movies (TV shows break this rule)

### Process notes
From the repo root directory:
- `pip freeze > requirements.txt`
- `pip install --editable .`

`which mmgmt` shows where the binary was installed

### Resources used
- [boto3 S3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#s3)

### more notes
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

- can you manage the torrent files and torrenting process through this same CLI? how do torrents work?
	- store tracker information / magnet link distributed hash table (DHT) within database
	- what does it take to host torrent tracker site? ([link](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiB9-eF5vLyAhVKITQIHYFIDJgQFnoECBgQAQ&url=http%3A%2F%2Ftroydm.github.io%2Fblog%2F2013%2F04%2F24%2Fhosting-your-own-remote-private-torrent-tracker&usg=AOvVaw23jlIHbjorXcJycyFY1Uql))

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
