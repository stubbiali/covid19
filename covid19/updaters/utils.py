# -*- coding: utf-8 -*-
import os
import subprocess


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


