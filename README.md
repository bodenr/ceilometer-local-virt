Ceilometer local host / vm inspector
====================================

Implements an OpenStack [ceilometer](https://wiki.openstack.org/wiki/Ceilometer) virt
inspector which can be installed to collect measurements from a local operating system.

This code is a PoC and not intended for production usage at this point in time.


Use cases for this inspector include:

* Using push based measurements with ceilometer on VMs which host access
is restricted and thus a per physical host integration cannot be used. This
is often the case when running VMs in an off-prem cloud.

* Collecting local measurements from a bare metal host which does not have
a hypervisor with VMs.

As a local inspector, the measurement reporting requires the instance ```UUID``` and ```name```
within the measurement data. Given the means to obtain these values vary from
env to env, this functionality is pluggable by means of a ```LocalInstanceInspector```.

The plugin defaults to the ```conf``` instance inspector which expects to find the
instance UUID and name in the conf.

For more details have a look at the entry points in this projects ```setup.py```.
In particular the ```ceilometer.compute.virt.instance.inspector``` plug-point.


Installation
====================================

The local VM inspector installs as a proper plugin to the [ceilometer compute agent](http://docs.openstack.org/icehouse/install-guide/install/apt/content/ceilometer-install-nova.html).
For this topology both the ceilometer compute agent and local inspector are installed on
the local VM or bare metal host.

* Follow the OpenStack docs for [installing the ceilometer compute agent](http://docs.openstack.org/icehouse/install-guide/install/apt/content/ceilometer-install-nova.html).

* Clone this repo: ```git clone https://github.com/bodenr/ceilometer-local-virt.git```

* Install the project: ```cd ceilometer-local-virt && python setup.py install```

* Edit the ```ceilometer.conf``` to specify the local inspector.

```ini
[DEFAULT]
hypervisor_inspector = local
```

* If you've implemented your own ```LocalInstanceInspector``` then specify it in the 
```ceilometer.conf``` as follows:

```ini
local_instance_type = your_inspector_id
```

* If you're using the default ```conf``` instance inspector, define your
instance UUID and name in the ```ceilometer.conf``` as follows:

```ini
local_instance_name = The instance name
local_instance_uuid = THE_INSTANCE_UUID
```

* Restart the ceilometer compute agent to pickup the changes.

