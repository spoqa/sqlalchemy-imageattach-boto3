# SQLAlchemy-ImageAttach-boto3

[![PyPI version badge](https://badgen.net/pypi/v/sqlalchemy-imageattach-boto3)](https://pypi.org/project/sqlalchemy-imageattach-boto3/)
[![PyPI license badge](https://badgen.net/pypi/license/sqlalchemy-imageattach-boto3)](LICENSE)

SQLAlchemy-ImageAttach AWS S3 Store with boto3

Since the `S3Store` of [SQLAlchemy-ImageAttach](https://github.com/dahlia/sqlalchemy-imageattach)
uses HTTP API and AWS Signature Version 4 to get/put images to S3, AWS access
key and secret key is required. But if an application does not have access key
(i.e. given access by AWS IAM Role), the application cannot use `S3Store`. So
SQLAlchemy-ImageAttach-boto3 offers `Boto3S3Store`, reimplemented `S3Store` with
[boto3](https://github.com/boto/boto3), so that the application can use various
credential sources that boto3 offers.


## Installation

Available on [PyPI](https://pypi.org/project/sqlalchemy-imageattach-boto3/):

```sh
$ pip install SQLAlchemy-ImageAttach-boto3
```
