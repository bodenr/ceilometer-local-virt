import novaclient

import openstack.ceilometer.compute.virt.local.inspector as local_inspector
import openstack.softlayer.utils as sl_utils

from ceilometer import plugin
from ceilometer import nova_client
from ceilometer.openstack.common import log
from novaclient.v1_1 import client as nova_client
from oslo.config import cfg


LOG = log.getLogger(__name__)

nova_opts = [
    cfg.BoolOpt('nova_http_log_debug',
                default=False,
                help='Allow novaclient\'s debug log output.'),
]
cfg.CONF.register_opts(nova_opts)
cfg.CONF.import_group('service_credentials', 'ceilometer.service')


def client():
    conf = cfg.CONF.service_credentials
    tenant = conf.os_tenant_id or conf.os_tenant_name
    return nova_client.Client(
        username=conf.os_username,
        api_key=conf.os_password,
        project_id=tenant,
        auth_url=conf.os_auth_url,
        region_name=conf.os_region_name,
        endpoint_type=conf.os_endpoint_type,
        cacert=conf.os_cacert,
        insecure=conf.insecure,
        http_log_debug=cfg.CONF.nova_http_log_debug,
        no_cache=True)


class SLInstanceInspector(local_inspector.LocalInstanceInspector):

    def __init__(self):
        super(SLInstanceInspector, self).__init__()
        self.server = InstanceDiscovery().server()
        LOG.debug("SoftLayer instance inspector found: %s" % (self.server))

    def instance_name(self):
        return self.server.get('hostname')

    def instance_uuid(self):
        return self.server.get('id')


class InstanceDiscovery(plugin.DiscoveryBase):

    _client = None

    def __init__(self):
        super(InstanceDiscovery, self).__init__()
        if InstanceDiscovery._client is None:
            InstanceDiscovery._client = client()

    def server(self):
        search_ops = {'private_ip': str(sl_utils.private_ip()),
                      'hostname': sl_utils.hostname()}
        LOG.debug("Query SoftLayer VMs with params: %s" % (search_ops))
        server = InstanceDiscovery._client.servers.list(detailed=True,
                                                        search_ops=search_ops)
        assert type(server) != list and len(server) != 1, ("Unable to find "
            "local instance: %s" % sl_utils.hostname())
        LOG.debug("SoftLayer instance discovery found: %s" % (server[0]))
        return server[0]

    def discover(self, param=None):
        return [self.server()]
