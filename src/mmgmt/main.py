"""main.py docstring"""

import logging
import boto3

import modules.utils as utils
import modules.aws_utils as aws_utils

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

filename = "modules/config.yml"
configs = utils.load_configs(filename)["test"]
logger.info(configs)

s3_client = boto3.resource("s3")

# def main():
# 	res = s3_client.Object(configs['bucket'], configs['prefix']+'/test2.txt').put(Body=open('test.txt', 'rb'))
# 	logger.info(res)

if __name__ == "__main__":
    main()
