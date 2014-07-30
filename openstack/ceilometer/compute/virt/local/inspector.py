import abc
import psutil
import six

import netifaces as netif

from ceilometer.compute.virt import inspector as virt_inspector
from ceilometer.openstack.common import units
from oslo.config import cfg
from stevedore import driver

OPTS = [
    cfg.StrOpt('local_instance_type',
               default='softlayer',
               help='Local instance inspector to use for inspecting '
               'the hypervisor layer.'),
]

CONF = cfg.CONF
CONF.register_opts(OPTS)


@six.add_metaclass(abc.ABCMeta)
class LocalInstanceInspector(object):

    @abc.abstractmethod
    def instance_name(self):
        pass

    @abc.abstractmethod
    def instance_uuid(self):
        pass


class LocalInspector(virt_inspector.Inspector):

    NAMESPACE = 'ceilometer.compute.virt.instance.inspector'

    def __init__(self):
        super(LocalInspector, self).__init__()
        self.inst_inspector = driver.DriverManager(
            namespace=LocalInspector.NAMESPACE,
            name=CONF.local_instance_type,
            invoke_on_load=True,
            invoke_args=None)
        assert isinstance(self.inst_inspector,
                          LocalInstanceInspector), ('Invalid instance '
                          'inspector type superclass')

    def inspect_instances(self):
        return virt_inspector.Instance(
            name=self.inst_inspector.instance_name(),
            UUID=self.inst_inspector.instance_uuid())

    def inspect_cpus(self, instance_name):
        cpu_count = psutil.cpu_count()
        cpu_times = psutil.cpu_times()
        
        return virt_inspector.CPUStats(number=cpu_count,
                                       time=cpu_times.user + cpu_times.system)

    def inspect_cpu_util(self, instance, duration=None):
        return virt_inspector.CPUUtilStats(util=psutil.cpu_percent())

    def inspect_vnics(self, instance_name):
        nic_stat = psutil.net_io_counters(pernic=True)
        for iface, counter in nic_stat.iteritems():
            link = netif.ifaddresses(iface)[netif.AF_LINK]
            interface = virt_inspector.Interface(
                name=iface,
                mac=link[0].get('addr'),
                fref=None,
                parameters=None)

            stat = virt_inspector.InterfaceStats(
                rx_bytes=counter.bytes_recv,
                rx_packets=counter.packets_recv,
                tx_bytes=counter.bytes_sent,
                tx_packets=counter.packets_sent)

            yield (interface, stat)

    def inspect_disks(self, instance_name):
        disk_stat = psutil.disk_io_counters(perdisk=True)
        for disk, counter in disk_stat.iteritems():
            dev = virt_inspector.Disk(device=disk)

            stat = virt_inspector.DiskStats(
                read_requests=counter.read_count,
                read_bytes=counter.read_bytes,
                write_requests=counter.write_count,
                write_bytes=counter.write_bytes,
                errors=0)

            yield (dev, stat)

    def inspect_memory_usage(self, instance, duration=None):
        memory = psutil.virtual_memory().used
        memory = memory / units.Mi
        return virt_inspector.MemoryUsageStats(usage=memory)
