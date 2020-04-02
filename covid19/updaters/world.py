# -*- coding: utf-8 -*-
from covid19 import config
from covid19.updater import Updater, registry
from covid19.updaters.utils import update_repo


@registry(name="world")
class UpdaterWorld(Updater):
    def run(self):
        update_repo(
            config.repo_world_dir, config.repo_world_branch, config.repo_world_logfile
        )


if __name__ == "__main__":
    _ = UpdaterWorld()
    _ = Updater.factory("world")
    from covid19.updater import ledger
    assert "world" in ledger
