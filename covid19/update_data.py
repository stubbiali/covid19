# -*- coding: utf-8 -*-
import os
import subprocess

from covid19 import config


def update_repo(repo_dir, repo_branch, repo_logfile):
    if not os.path.isdir(repo_dir):
        print("Clone the repo {} ...".format(repo_dir))

        with open(repo_logfile, "w") as logfile:
            clone = subprocess.run(
                ["git", "submodule", "update", repo_dir], stdout=logfile, stderr=logfile
            )
            if clone.returncode:
                print("Clone failed. Please see {}.".format(repo_logfile))
                return
            else:
                pass

    pwd = os.getcwd()

    os.chdir(repo_dir)

    print("Refresh the repo {} ...".format(repo_dir))

    with open(repo_logfile, "w") as logfile:
        checkout = subprocess.run(
            ["git", "checkout", repo_branch], stdout=logfile, stderr=logfile
        )
        if checkout.returncode:
            print(
                "Could not checkout the {} branch. Please see {}.".format(
                    repo_branch, repo_logfile
                )
            )
            os.chdir(pwd)
            return

        pull = subprocess.run(["git", "pull"], stdout=logfile, stderr=logfile)
        if pull.returncode:
            print(
                "Could not pull the {} branch. Please see {}.".format(
                    repo_branch, repo_logfile
                )
            )
            os.chdir(pwd)
            return
        else:
            os.chdir(pwd)


def update_italy():
    update_repo(
        config.repo_italy_dir, config.repo_italy_branch, config.repo_italy_logfile
    )


def update_switzerland():
    update_repo(
        config.repo_switzerland_dir,
        config.repo_switzerland_branch,
        config.repo_switzerland_logfile,
    )


def update_world():
    update_repo(
        config.repo_world_dir, config.repo_world_branch, config.repo_world_logfile
    )


def update_all():
    update_italy()
    update_switzerland()
    update_world()


if __name__ == "__main__":
    update_italy()
    update_switzerland()
    update_world()
