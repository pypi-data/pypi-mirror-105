# This file is part of nvitop, the interactive NVIDIA-GPU process viewer.
# License: GNU GPL version 3.

# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
# pylint: disable=invalid-name

import datetime
import functools
import os
import threading
import time

import psutil
from cachetools.func import ttl_cache

from .utils import Snapshot, bytes2human, timedelta2human


if psutil.POSIX:
    def add_quotes(s):
        if s == '':
            return '""'
        if '$' not in s and '\\' not in s:
            if ' ' not in s:
                return s
            if '"' not in s:
                return '"{}"'.format(s)
        if "'" not in s:
            return "'{}'".format(s)
        return '"{}"'.format(s.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$'))
elif psutil.WINDOWS:
    def add_quotes(s):
        if s == '':
            return '""'
        if '%' not in s and '^' not in s:
            if ' ' not in s and '\\' not in s:
                return s
            if '"' not in s:
                return '"{}"'.format(s)
        return '"{}"'.format(s.replace('^', '^^').replace('"', '^"').replace('%', '^%'))
else:
    def add_quotes(s):
        return '"{}"'.format(s)


def auto_garbage_clean(default=None):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except psutil.Error:
                try:
                    with GpuProcess.INSTANCE_LOCK:
                        del GpuProcess.INSTANCES[(self.pid, self.device)]
                except KeyError:
                    pass
                try:
                    with HostProcess.INSTANCE_LOCK:
                        del HostProcess.INSTANCES[self.pid]
                except KeyError:
                    pass
                return default
        return wrapped

    return wrapper


class HostProcess(psutil.Process):
    INSTANCE_LOCK = threading.RLock()
    INSTANCES = {}

    def __new__(cls, pid=None):
        if pid is None:
            pid = os.getpid()

        try:
            return cls.INSTANCES[pid]
        except KeyError:
            pass

        instance = super().__new__(cls)
        instance.__init__(pid)
        with cls.INSTANCE_LOCK:
            cls.INSTANCES[pid] = instance
        return instance

    def __init__(self, pid=None):  # pylint: disable=super-init-not-called
        super()._init(pid, True)
        try:
            super().cpu_percent()
        except psutil.Error:
            pass

    cpu_percent = ttl_cache(ttl=1.0)(psutil.Process.cpu_percent)
    memory_percent = ttl_cache(ttl=1.0)(psutil.Process.memory_percent)

    if psutil.WINDOWS:
        def username(self):
            return super().username().split('\\')[-1]


class GpuProcess(object):
    INSTANCE_LOCK = threading.RLock()
    INSTANCES = {}
    SNAPSHOT_LOCK = threading.RLock()
    HOST_SNAPSHOTS = {}

    def __new__(cls, pid, device, gpu_memory=None, type=None):  # pylint: disable=redefined-builtin
        try:
            return cls.INSTANCES[(pid, device)]
        except KeyError:
            pass

        instance = super().__new__(cls)
        instance.__init__(pid, device, gpu_memory, type)
        with cls.INSTANCE_LOCK:
            cls.INSTANCES[(pid, device)] = instance
            with cls.SNAPSHOT_LOCK:
                try:
                    del cls.HOST_SNAPSHOTS[pid]
                except KeyError:
                    pass
        return instance

    def __init__(self, pid, device, gpu_memory=None, type=None):  # pylint: disable=redefined-builtin
        self.host = HostProcess(pid)
        self._ident = (self.pid, self.host._create_time, device.index)

        self.device = device
        if gpu_memory is None and not hasattr(self, '_gpu_memory'):
            gpu_memory = 'N/A'
        if gpu_memory is not None:
            self.set_gpu_memory(gpu_memory)
        if type is None and not hasattr(self, '_type'):
            type = ''
        if type is not None:
            self.type = type
        self._hash = None

    def __str__(self):
        return "{}.{}(device={}, gpu_memory={}, host_process={})".format(
            self.__class__.__module__, self.__class__.__name__,
            self.device, bytes2human(self.gpu_memory()), self.host
        )

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, (GpuProcess, psutil.Process)):
            return NotImplemented
        return self._ident == other._ident

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._ident)
        return self._hash

    @property
    def pid(self):
        return self.host.pid

    def gpu_memory(self):
        return self._gpu_memory

    def set_gpu_memory(self, value):
        self._gpu_memory = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = ''
        if 'C' in value:
            self._type += 'C'
        if 'G' in value:
            self._type += 'G'
        if 'X' in value or self._type == 'CG':
            self._type = 'X'

    @ttl_cache(ttl=1.0)
    @auto_garbage_clean(default=datetime.timedelta())
    def running_time(self):
        return datetime.datetime.now() - datetime.datetime.fromtimestamp(self.create_time())

    @auto_garbage_clean(default=time.time())
    def create_time(self):
        return self.host.create_time()

    @auto_garbage_clean(default='N/A')
    def username(self):
        return self.host.username()

    @auto_garbage_clean(default='N/A')
    def name(self):
        return self.host.name()

    @auto_garbage_clean(default=0.0)
    def cpu_percent(self):
        return self.host.cpu_percent()

    @auto_garbage_clean(default=0.0)
    def memory_percent(self):
        return self.host.memory_percent()

    @auto_garbage_clean(default=('No Such Process',))
    def cmdline(self):
        cmdline = self.host.cmdline()
        if len(cmdline) == 0:
            raise psutil.NoSuchProcess(pid=self.pid)
        return cmdline

    def is_running(self):
        return self.host.is_running()

    def send_signal(self, sig):
        self.host.send_signal(sig)

    def terminate(self):
        self.host.terminate()

    def kill(self):
        self.host.kill()

    @classmethod
    def clear_host_snapshots(cls):
        with cls.SNAPSHOT_LOCK:
            cls.HOST_SNAPSHOTS.clear()

    @auto_garbage_clean(default=None)
    def take_snapshot(self):
        with self.SNAPSHOT_LOCK:
            try:
                host = self.HOST_SNAPSHOTS[self.pid]
            except KeyError:
                with self.host.oneshot():
                    host = Snapshot(
                        real=self.host,
                        username=self.username(),
                        name=self.name(),
                        cmdline=self.cmdline(),
                        cpu_percent=self.cpu_percent(),
                        memory_percent=self.memory_percent(),
                        is_running=self.is_running(),
                        running_time=self.running_time()
                    )

                if host.cpu_percent < 1000.0:
                    host.cpu_percent_string = '{:.1f}'.format(host.cpu_percent)
                elif host.cpu_percent < 10000:
                    host.cpu_percent_string = '{}'.format(int(host.cpu_percent))
                else:
                    host.cpu_percent_string = '9999+'
                host.memory_percent_string = '{:.1f}'.format(host.memory_percent)

                if host.is_running:
                    host.running_time_human = timedelta2human(host.running_time)
                else:
                    host.running_time_human = 'N/A'
                    host.cmdline = ('No Such Process',)
                if len(host.cmdline) > 1:
                    host.cmdline = '\0'.join(host.cmdline).strip('\0').split('\0')
                if len(host.cmdline) == 1:
                    host.command = host.cmdline[0]
                else:
                    host.command = ' '.join(map(add_quotes, host.cmdline))

                host.info = '{:>5} {:>5}  {:>8}  {}'.format(host.cpu_percent_string,
                                                            host.memory_percent_string,
                                                            host.running_time_human,
                                                            host.command)

                self.HOST_SNAPSHOTS[self.pid] = host

        gpu_memory = self.gpu_memory()
        return Snapshot(
            real=self,
            identity=self._ident,
            pid=self.pid,
            device=self.device,
            gpu_memory=gpu_memory,
            gpu_memory_human=bytes2human(gpu_memory),
            type=self.type,
            username=host.username,
            name=host.name,
            cmdline=host.cmdline,
            command=host.command,
            cpu_percent=host.cpu_percent,
            cpu_percent_string=host.cpu_percent_string,
            memory_percent=host.memory_percent,
            memory_percent_string=host.memory_percent_string,
            is_running=host.is_running,
            running_time=host.running_time,
            running_time_human=host.running_time_human,
            host_info=host.info
        )
