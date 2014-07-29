import netifaces as netif
import os
import socket
import SoftLayer

import openstack.ceilometer.compute.virt.local.inspector as local_inspector


class SLInstanceInspector(local_inspector.LocalInstanceInspector):

    def __init__(self):
        super(SLInstanceInspector, self).__init__()
        self.client = SoftLayer.Client(
            username=os.getenv('SL_USERNAME', None),
            api_key=os.getenv('SL_KEY', None),
            endpoint_url=os.getenv('SL_URL', None))
        self.vms = SoftLayer.managers.vs.VSManager(self.client)
        self.hostname = str(socket.gethostname())
        self.private_ip = netif.ifaddresses('eth0')[netif.AF_INET][0]['addr']
        instances = self.vms.list_instances(hostname=self.hostname,
                                            private_ip=self.private_ip)
        assert len(instances) == 1, ("Unable to find local instance: %s"
                                     % self.hostname)
        self.instance = instances[0]

    def instance_name(self):
        return self.instance.get('hostname')

    def instance_uuid(self):
        return self.instance.get('id')

