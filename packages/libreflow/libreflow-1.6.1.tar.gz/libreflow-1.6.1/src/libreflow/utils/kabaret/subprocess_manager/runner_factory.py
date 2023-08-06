import os
import subprocess
import pathlib
import time
from datetime import datetime

import logging

import kabaret.subprocess_manager as ksm

logger = logging.getLogger(__name__)


class Runner(ksm.runner_factory.Runner):
    
    def __init__(self, version=None, label=None, extra_argv=[], extra_env={}):
        super(Runner, self).__init__(
            version=version,
            label=label,
            extra_argv=extra_argv,
            extra_env=extra_env,
        )
        self._last_run_time = None

    def run(self):
        cmd = [self.executable()]
        cmd.extend(self.argv())

        env = self.env()

        os_flags = {}

        # Disowning processes in linux/mac
        if hasattr(os, "setsid"):
            os_flags["preexec_fn"] = os.setsid

        # Disowning processes in windows
        if hasattr(subprocess, "STARTUPINFO"):
            # Detach the process
            os_flags["creationflags"] = subprocess.CREATE_NEW_CONSOLE

            # Hide the process console
            startupinfo = subprocess.STARTUPINFO()
            if self.show_terminal():
                flag = "/C"
                if self.keep_terminal():
                    flag = "/K"
                cmd = ["cmd", flag] + cmd
            else:
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            os_flags["startupinfo"] = startupinfo

        logger.info("Running Subprocess: %r", cmd)
        
        if not os.path.exists(self._get_log_dir()):
            os.mkdir(self._get_log_dir())
        
        # Store run time used to compute log paths
        self._last_run_time = time.time()

        with open(self.get_log_path(), 'w+') as log_fd:
            self._popen = subprocess.Popen(
                cmd,
                env=env,
                stdout=log_fd,
                stderr=log_fd,
                **os_flags,
            )
    
    def _get_log_dir(self):
        return str(pathlib.Path.home()) + "/.libreflow/log/"

    def get_log_path(self):
        dt = datetime.fromtimestamp(self._last_run_time)
        dt = dt.astimezone().strftime("%Y-%m-%dT%H-%M-%S%z")
        
        path = os.path.join(
            self._get_log_dir(),
            '%s_%s.log' % (self.runner_name(), dt),
        )
        return path
    
    def has_run(self):
        return self._last_run_time is not None
    
    def pid(self):
        return self._popen.pid
    
    def terminate(self):
        self._popen.terminate()
    
    def kill(self):
        self._popen.kill()

    def is_running(self):
        return self._popen.poll() is None
    
    def return_code(self):
        return self._popen.returncode


class SubprocessManager(object):
    """
    The SubprocessManager manages a list of Runner instances.
    
    From original kabaret.subprocess_manager.runner_factory.SubprocessManager
    """

    def __init__(self):
        super(SubprocessManager, self).__init__()
        self._runners = []

    def get_runner_infos(self):
        """
        Return a list of dict with keys:
            label, name, icon, version, is_running, log_path
        """
        infos = []
        for i, runner in enumerate(self._runners):
            if runner.has_run():
                infos.append(
                    dict(
                        label=runner.label,
                        name=runner.runner_name(),
                        icon=runner.runner_icon(),
                        version=runner.version,
                        is_running=runner.is_running(),
                        log_path=runner.get_log_path(),
                        pid=runner.pid(),
                        index=i,
                    )
                )
        
        return infos
    
    def get_runner(self, index):
        """
        Returns data of the runner indexed with
        the given `index`, as a dict with keys:
            label, name, icon, version, is_running, log_path
        """
        return self._runners[index]


    def run(self, runner):
        self._runners.append(runner)
        runner.run()
