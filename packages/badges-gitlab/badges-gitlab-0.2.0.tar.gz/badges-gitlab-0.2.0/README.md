# Badges Gitlab

This project was created to generate badges for Gitlab in CI jobs.\
By default, Gitlab supports only two types of badges: pipeline and test coverage.\
These badges are better detailed at: https://docs.gitlab.com/ee/user/project/badges.html.
    
## Requirements

For using this function, it will also install these packages and their dependencies:
- Python Gitlab API
- Anybadge
- Iso8601

## Usage 

### Common Usage

For testing purposes, you may want to install this package though pip:

```code
$ pip install badges-gitlab
$ badges-gitlab -h 
usage: badges-gitlab [-h] [-p --path]

Generate Gitlab Badges using JSON files.

optional arguments:
  -h, --help  show this help message and exit
  -p --path   path where json and badges files will be generated/located (default: ./public/badges/)
```

### Gitlab CI YAML Pipeline Job Example

Below it is an example of a job running at the end of the pipeline in the default branch (main):


### Dockerfile Example

Example of docker file

## Motivation

Although it is possible to generate badges with other API's such as [shields.io](http://shields.io), usually this process is not available in private repositories.\
So if you are hosting a public project, this package is not specifically meant for you as you can workaround with other easier implementations.\
But, if you are hosting a private project and don't want to expose your project (Gitlab pages) or don't want to risk exposing your credentials (API Requests), maybe this project is for you.\
Another reason would be to avoid overloading servers (e.g. shields.io) with unnecessary requests for (re)creating badges.

## Design Choices

Some design choices were made to create this package.
1. The badges' generation were converted into two stages:
    - The first stage uses the Gitlab API (if the private-token turns out to be valid) to generate the json for some badges.
    - The second stage gets all the JSON files from the target folder and creates badges using anybadge.
2. These two stages have a purpose, if any other CI Pipeline job generates json files with their own data, you can also use these files to create badges.
3. The default directory is /public/badges:
    - This folder may be used later for Gitlab pages, although this can be modified through parameters
