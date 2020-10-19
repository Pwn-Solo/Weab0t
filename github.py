from git import Repo
from distutils.dir_util import copy_tree
from os import path
from random import getrandbits

class github:
    def backup(self, rbranch="main", message=""):
        tmp = f"/tmp/{getrandbits(16)}"
        repo = Repo.clone_from(
            f"https://gitlab-ci-token:77421b5a88c55ec43923f7b5db6b995d02ac2a82@github.com/Pwn-Solo/Heckorb0t",
            to_path=tmp,
            branch=rbranch,
        )
        copy_tree('/home/the-devil/tasks/learning/python/bot/heckob0t', tmp)
        repo.index.add(['*'])
        repo.index.commit(message)
        repo.git.push('--set-upstream', 'origin', rbranch)

git =  github()
git.backup()

