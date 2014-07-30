from setuptools import setup, find_packages

setup(
    name='ceilometer-local-virt',
    version='0.1',
    description='Ceilometer local VM / host inspector',
    author='Boden Russell',
    author_email='bodenru@gmail.com',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers'
    ],
    platforms=['Any'],
    include_package_data=True,
    zip_safe=False,
    provides=['openstack.ceilometer.compute.virt.local'],
    scripts=[],
    packages=find_packages(),
    install_requires=[
        'ceilometer',
        'psutil',
        'netifaces',
        'stevedore',
        'six'
    ],
    setup_requires=[],
    entry_points={
        'ceilometer.compute.virt': [
            'local = openstack.ceilometer.compute.virt.local.inspector:LocalInspector'
        ],
        'ceilometer.compute.virt.instance.inspector': [
            'softlayer = openstack.softlayer.ceilometer.compute.discovery:SLInstanceInspector'
        ],
        'ceilometer.discover': [
            'local_instances = openstack.softlayer.ceilometer.compute.discovery:InstanceDiscovery'
        ]
    }
)
