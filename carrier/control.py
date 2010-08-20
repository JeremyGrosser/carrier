from subprocess import Popen
from threading import Thread
import os

class VirtualMachine(object):
    STORAGE_PATH = '/mnt/vm'

    def __init__(self, config):
        self.config = config
        self.process = None

    def create_disk(self):
        p = Popen('/usr/bin/qemu-img create -f qcow2 %s/%s.root %iG' % (
            self.STORAGE_PATH, self.config['name'], self.config['disk']), shell=True)
        p.wait()
        p = Popen('/usr/bin/qemu-img create -f raw %s/%s.swap 1G' % (
            self.STORAGE_PATH, self.config['name']), shell=True)
        p.wait()

    def delete_disk(self):
        os.unlink('%s/%s.root' % (self.STORAGE_PATH, self.config['name']))
        os.unlink('%s/%s.swap' % (self.STORAGE_PATH, self.config['name']))

    def update(self, newconfig):
        for key in newconfig:
            if not key in ('boot', 'memory', 'mac', 'console', 'nic', 'vnc'):
                raise Exception('Cannot modify config option %s, it is read-only' % key)
            else:
                self.config[key] = newconfig[key]
        return self.config

    def delete(self):
        self.delete_disk()

    def start(self):
        self.process = Popen(('/usr/bin/kvm -hda %s/%s.root -hdb %s/%s.swap -m %i -vnc :%i -serial mon:telnet:127.0.0.1:%i,server,nowait -net nic,macaddr=%s,model=%s -net tap -boot %s -monitor /dev/null' % (
            self.STORAGE_PATH, self.config['name'],
            self.STORAGE_PATH, self.config['name'],
            self.config['memory'],
            self.config['vnc'],
            self.config['console'],
            self.config['mac'],
            self.config['nic'],
            self.config['boot'],
        )).split(' '))

    def stop(self):
        #self.process.terminate()
        os.kill(self.process.pid, 15)
        self.process.wait()

    def get_state(self):
        if not self.process:
            return 'STOPPED'
        self.process.poll()
        if self.process.returncode == None:
            return 'RUNNING'
        else:
            return 'STOPPED'

    def get_config(self):
        return self.config
