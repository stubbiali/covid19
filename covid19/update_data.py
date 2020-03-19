# -*- coding: utf-8 -*-
import os
import subprocess

from covid19 import config


root_dir = "/Users/subbiali/Desktop/covid19"
data_dir = os.path.join(root_dir, "data")


def update_italy():
    if not os.path.isdir(config.repo_italy_dir):
        print("Cloning the repo containing the Italian data ...")

        with open(config.repo_italy_logfile, "w") as logfile:
            clone = subprocess.run(
                ["git", "clone", config.repo_italy_remote, config.repo_italy_dir],
                stdout=logfile, stderr=logfile
            )
            if clone.returncode:
                print("Clone failed. Please see {}.".format(config.repo_italy_logfile))
                return
            else:
                print("Clone completed successfully.")
    else:
        os.chdir(config.repo_italy_dir)

        print("Updating the Italian data ...")

        with open(config.repo_italy_logfile, "w") as logfile:
            pull = subprocess.run(["git", "pull"], stdout=logfile, stderr=logfile)
            if pull.returncode:
                print("Update failed. Please see {}.".format(config.repo_italy_logfile))
                return
            else:
                print("Update completed successfully.")


def update_world():
    if not os.path.isdir(config.repo_italy_dir):
        print("Cloning the repo containing the global data ...")

        with open(config.repo_world_logfile, "w") as logfile:
            clone = subprocess.run(
                ["git", "clone", config.repo_italy_remote, config.repo_world_dir],
                stdout=logfile, stderr=logfile
            )
            if clone.returncode:
                print("Clone failed. Please see {}.".format(config.repo_world_logfile))
                return
            else:
                print("Clone completed successfully.")
    else:
        os.chdir(config.repo_world_dir)

        print("Updating the global data ...")

        with open(config.repo_world_logfile, "w") as logfile:
            pull = subprocess.run(["git", "pull"], stdout=logfile, stderr=logfile)
            if pull.returncode:
                print("Update failed. Please see {}.".format(config.repo_world_logfile))
                return
            else:
                print("Update completed successfully.")


if __name__ == "__main__":
    update_italy()
    update_world()
