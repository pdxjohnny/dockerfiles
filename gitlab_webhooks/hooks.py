import os
import sys
import git
import json
import docker
import shutil

import irc_client

# Directory to clone projects to
REPO_DIR = "repos"
# Directory to run docker builds in, deleted every build
BUILD_DIR = "builds"
# The address to connect to docker on
DOCKER_BIND = "unix://var/run/docker.sock"
# False for default
DOCKER_REGISTRY = "localhost:5000"
# False for no username
DOCKER_USERNAME = "pdxjohnny"
# True if your registry is insecure
INSECURE_REGISTRY = True
# Send output to irc, False or call irc_client.start
IRC = False

def init():
    if IRC:
        irc_client.start(IRC)

def git_fetch(repo):
    """
    Clones the repo specified into a bare repo which is fetched on pull
    """
    if not os.path.exists(repo["bare"]):
        write("Cloning...")
        git.Repo.clone_from(repo["url"], repo["bare"], bare=True)
        write("Cloned")
    else:
        write("Pulling...")
        bare_repo = git.Repo(repo["bare"])
        bare_repo.remotes.origin.fetch("master")
        write("Pulled")

def git_checkout(repo):
    """
    Clones from the bare repo, used for the build
    """
    if os.path.exists(repo["path"]):
        shutil.rmtree(repo["path"])
    git.Repo.clone_from(repo["bare"], repo["path"])

def docker_build(repo):
    """
    Builds the images using the Dockerfile at the root of the repo
    """
    client = docker.Client(base_url=DOCKER_BIND)
    if DOCKER_USERNAME:
        repo["tag"] = DOCKER_USERNAME + '/' + repo["tag"]
    if DOCKER_REGISTRY:
        repo["tag"] = DOCKER_REGISTRY + '/' + repo["tag"]
    write("Building \"{}\"...".format(repo["tag"]))
    stream = client.build(path=repo["path"], rm=True, tag=repo["tag"])
    print_stream(stream)
    write("Built")

def docker_push(repo):
    """
    Pushes a taged image to a registry
    """
    client = docker.Client(base_url=DOCKER_BIND)
    write("Pushing \"{}\"...".format(repo["tag"]))
    stream = client.push(repo["tag"], stream=True, \
        insecure_registry=INSECURE_REGISTRY)
    print_stream(stream)
    write("Pushed")
    return repo

def print_stream(stream):
    """
    Prints all lines in the docker output streams
    """
    for line in stream:
        line = json.loads(line)
        for prop in line:
            if isinstance(line[prop], str) or isinstance(line[prop], unicode):
                write(line[prop])

def write(message):
    if not '\r' in message and message[-1] != '\n':
        message += '\n'
    if IRC is not False:
        irc_client.write(message.rstrip())
    sys.stdout.write(message)

def push(hook):
    """
    Gets the newest version of the repo builds the docker images of it
    and pushes it to a registry
    """
    write("got push")
    repo = hook["repository"]
    repo["bare"] = os.path.join(REPO_DIR, repo["name"]) + ".git"
    git_fetch(repo)
    repo["path"] = os.path.join(BUILD_DIR, repo["name"])
    git_checkout(repo)
    repo["tag"] = repo["name"]
    docker_build(repo)
    docker_push(repo)
    write("finished push {}".format(repo["tag"]))
