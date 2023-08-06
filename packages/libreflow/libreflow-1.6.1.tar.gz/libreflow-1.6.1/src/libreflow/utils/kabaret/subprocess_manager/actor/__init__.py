import kabaret.subprocess_manager as ksm
from kabaret.subprocess_manager.actor import SubprocessManagerCmds
from kabaret.app._actor import Cmd
import libreflow.utils.kabaret as kutils

from .. import runner_factory


@SubprocessManagerCmds.cmd
class List_Runner_Infos(Cmd):
    """
    Returns an ordered list of dicts with keys:
        (
            label,
            name,
            icon,
            version,
            is_running,
            log_path,
            pid
        )
    """
    def _decode(self):
        pass

    def _execute(self):
        return self.actor().get_runner_infos()


@SubprocessManagerCmds.cmd
class Launch_Runner_Instance(Cmd):
    """
    Launches the runner subprocess.
    """
    def _decode(self, runner_index):
        self._runner_index = runner_index

    def _execute(self):
        runner = self.actor().get_runner(
            self._runner_index
        )
        runner.run()


@SubprocessManagerCmds.cmd
class Terminate_Runner_Instance(Cmd):
    """
    Terminates the runner subprocess.
    """
    def _decode(self, runner_index):
        self._runner_index = runner_index

    def _execute(self):
        runner = self.actor().get_runner(
            self._runner_index
        )
        runner.terminate()


@SubprocessManagerCmds.cmd
class Kill_Runner_Instance(Cmd):
    """
    Kill the runner subprocess.
    """
    def _decode(self, runner_index):
        self._runner_index = runner_index

    def _execute(self):
        runner = self.actor().get_runner(
            self._runner_index
        )
        runner.kill()


class SubprocessManager(ksm.actor.SubprocessManager):

    def __init__(self, session):
        super(SubprocessManager, self).__init__(session)
        self._factories = ksm.runner_factory.Factories()
        self._subprocess_manager = runner_factory.SubprocessManager()

        # Add default factories:
        self._factories.ensure_factory(ksm.runners.get_system_factory())
    
    def get_runner_infos(self):
        """
        Return a list of dict with keys:
            label, name, icon, version, is_running, log_path
        """
        return self._subprocess_manager.get_runner_infos()
    
    def get_runner(self, index):
        return self._subprocess_manager.get_runner(index)
    
    # def get_runner_from_pid(self, pid):
    #     """
    #     Returns the runner which launched the process
    #     with the given `pid`.
    #     """
    #     return self._subprocess_manager.get_runner(pid)
