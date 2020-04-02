# -*- coding: utf-8 -*-
from covid19 import config
from covid19.updater import Updater, registry
from covid19.updaters.utils import update_repo


@registry(name="switzerland")
class UpdaterSwitzerland(Updater):
    def run(self):
        update_repo(
            config.repo_switzerland_dir, config.repo_switzerland_branch, config.repo_switzerland_logfile
        )


if __name__ == "__main__":
    _ = UpdaterSwitzerland()
    _ = Updater.factory("switzerland")
    from covid19.updater import ledger
    assert "switzerland" in ledger
