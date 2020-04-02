# -*- coding: utf-8 -*-
from covid19 import config
from covid19.updater import Updater, registry
from covid19.updaters.utils import update_repo


@registry(name="italy")
class UpdaterItaly(Updater):
    def run(self):
        update_repo(
            config.repo_italy_dir, config.repo_italy_branch, config.repo_italy_logfile
        )


if __name__ == "__main__":
    _ = UpdaterItaly()
    _ = Updater.factory("italy")
    from covid19.updater import ledger
    assert "italy" in ledger
