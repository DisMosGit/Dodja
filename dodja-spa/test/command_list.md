### Containers

```JSON
{
"Id": "df0a47627794ff68da8a187aa64b9ee4c77e8cc83ec1bbeaf35d7eabad34c69d",
"Created": "2021-04-15T06:00:15.034332134Z",
"Path": "docker-entrypoint.sh",
"Args": [
    "mongod"
],
"State": {
    "Status": "paused",
    "Running": true,
    "Paused": true,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 48517,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2021-06-04T12:38:07.272856247Z",
    "FinishedAt": "2021-06-04T12:37:59.967957944Z"
},
"Image": "sha256:ca8e14b1fda68aedb435fec2a6eaa326cf5633fc57b7e28b5cc37d938ead9edd",
"ResolvConfPath": "/var/lib/docker/containers/df0a47627794ff68da8a187aa64b9ee4c77e8cc83ec1bbeaf35d7eabad34c69d/resolv.conf",
"HostnamePath": "/var/lib/docker/containers/df0a47627794ff68da8a187aa64b9ee4c77e8cc83ec1bbeaf35d7eabad34c69d/hostname",
"HostsPath": "/var/lib/docker/containers/df0a47627794ff68da8a187aa64b9ee4c77e8cc83ec1bbeaf35d7eabad34c69d/hosts",
"LogPath": "/var/lib/docker/containers/df0a47627794ff68da8a187aa64b9ee4c77e8cc83ec1bbeaf35d7eabad34c69d/df0a47627794ff68da8a187aa64b9ee4c77e8cc83ec1bbeaf35d7eabad34c69d-json.log",
"Name": "/django-mongodb",
"RestartCount": 0,
"Driver": "overlay2",
"Platform": "linux",
"MountLabel": "",
"ProcessLabel": "",
"AppArmorProfile": "docker-default",
"ExecIDs": null,
"HostConfig": {
    "Binds": null,
    "ContainerIDFile": "",
    "LogConfig": {
        "Type": "json-file",
        "Config": {}
    },
    "NetworkMode": "default",
    "PortBindings": {
        "27017/tcp": [
            {
                "HostIp": "",
                "HostPort": "27017"
            }
        ]
    },
    "RestartPolicy": {
        "Name": "no",
        "MaximumRetryCount": 0
    },
    "AutoRemove": false,
    "VolumeDriver": "",
    "VolumesFrom": null,
    "CapAdd": null,
    "CapDrop": null,
    "CgroupnsMode": "host",
    "Dns": [],
    "DnsOptions": [],
    "DnsSearch": [],
    "ExtraHosts": null,
    "GroupAdd": null,
    "IpcMode": "private",
    "Cgroup": "",
    "Links": null,
    "OomScoreAdj": 0,
    "PidMode": "",
    "Privileged": false,
    "PublishAllPorts": false,
    "ReadonlyRootfs": false,
    "SecurityOpt": null,
    "UTSMode": "",
    "UsernsMode": "",
    "ShmSize": 67108864,
    "Runtime": "runc",
    "ConsoleSize": [
        0,
        0
    ],
    "Isolation": "",
    "CpuShares": 0,
    "Memory": 0,
    "NanoCpus": 0,
    "CgroupParent": "",
    "BlkioWeight": 0,
    "BlkioWeightDevice": [],
    "BlkioDeviceReadBps": null,
    "BlkioDeviceWriteBps": null,
    "BlkioDeviceReadIOps": null,
    "BlkioDeviceWriteIOps": null,
    "CpuPeriod": 0,
    "CpuQuota": 0,
    "CpuRealtimePeriod": 0,
    "CpuRealtimeRuntime": 0,
    "CpusetCpus": "",
    "CpusetMems": "",
    "Devices": [],
    "DeviceCgroupRules": null,
    "DeviceRequests": null,
    "KernelMemory": 0,
    "KernelMemoryTCP": 0,
    "MemoryReservation": 0,
    "MemorySwap": 0,
    "MemorySwappiness": null,
    "OomKillDisable": false,
    "PidsLimit": null,
    "Ulimits": null,
    "CpuCount": 0,
    "CpuPercent": 0,
    "IOMaximumIOps": 0,
    "IOMaximumBandwidth": 0,
    "MaskedPaths": [
        "/proc/asound",
        "/proc/acpi",
        "/proc/kcore",
        "/proc/keys",
        "/proc/latency_stats",
        "/proc/timer_list",
        "/proc/timer_stats",
        "/proc/sched_debug",
        "/proc/scsi",
        "/sys/firmware"
    ],
    "ReadonlyPaths": [
        "/proc/bus",
        "/proc/fs",
        "/proc/irq",
        "/proc/sys",
        "/proc/sysrq-trigger"
    ]
},
"GraphDriver": {
    "Data": {
        "LowerDir": "/var/lib/docker/overlay2/71656dc6526d8aa567e257c1da8c670a00922529542ac04e21948d94affd8249-init/diff:/var/lib/docker/overlay2/2151bbe721c5122ea1c9e668ac68d4cbd7d7e53cdb2426428108d50826b93e22/diff:/var/lib/docker/overlay2/03c343449d31a77b3169adb040c01114e7b2cd38abd3b994c93e916c02b47b51/diff:/var/lib/docker/overlay2/87c75d050dccec08a874158c801fc43a1de800097d7092ba269037192f170b58/diff:/var/lib/docker/overlay2/00aa2f3568d1c0311a216291532c60bd81002fe8ef8ac97eb2156868740222e9/diff:/var/lib/docker/overlay2/0a29e48cd583b5e92611bc2e8e883326385588110fdc0b87d994840e81032bca/diff:/var/lib/docker/overlay2/f41d90c8192bcd6043788dcb1abcd0b26e04ee262d79143a1ac24195206a26cb/diff:/var/lib/docker/overlay2/9196ae32ba0431b93fe5c07f44181c6061dde1c7a9f7aeb909234cd04e3bf11f/diff:/var/lib/docker/overlay2/72e5ffc89a203deb1e6ebe7bdb1e0e8fb19fd804ad90f49bf29dca0415f512a0/diff:/var/lib/docker/overlay2/0eab88535019bbd3a00272f650169491d32aca57255cdca16a130edc8ec402c4/diff:/var/lib/docker/overlay2/f4e82d3896ed31cbff75466c0b0d5766c9a9f2e9f5dd532d61b35c11766bfbe6/diff:/var/lib/docker/overlay2/437ac08af2fa09a6ce23e61ee7b2fffe577431cd428740b9e06ae9635bc5b7ba/diff:/var/lib/docker/overlay2/559b6f84d4630ee03aa087dc2e54ffb21047d569c5fa658b9b063b01ed6f6ad8/diff",
        "MergedDir": "/var/lib/docker/overlay2/71656dc6526d8aa567e257c1da8c670a00922529542ac04e21948d94affd8249/merged",
        "UpperDir": "/var/lib/docker/overlay2/71656dc6526d8aa567e257c1da8c670a00922529542ac04e21948d94affd8249/diff",
        "WorkDir": "/var/lib/docker/overlay2/71656dc6526d8aa567e257c1da8c670a00922529542ac04e21948d94affd8249/work"
    },
    "Name": "overlay2"
},
"Mounts": [
    {
        "Type": "volume",
        "Name": "3d497f229432f4b5a34d85da76a3ac3a128be8d3557a29f211d81629f77df0bd",
        "Source": "/var/lib/docker/volumes/3d497f229432f4b5a34d85da76a3ac3a128be8d3557a29f211d81629f77df0bd/_data",
        "Destination": "/data/configdb",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
    },
    {
        "Type": "volume",
        "Name": "41835107fdc245a99e282cb7f2c459ecb264318f5b27dc1f82701653fcbe9522",
        "Source": "/var/lib/docker/volumes/41835107fdc245a99e282cb7f2c459ecb264318f5b27dc1f82701653fcbe9522/_data",
        "Destination": "/data/db",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
    }
],
"Config": {
    "Hostname": "df0a47627794",
    "Domainname": "",
    "User": "",
    "AttachStdin": false,
    "AttachStdout": false,
    "AttachStderr": false,
    "ExposedPorts": {
        "27017/tcp": {}
    },
    "Tty": false,
    "OpenStdin": false,
    "StdinOnce": false,
    "Env": [
        "MONGO_INITDB_ROOT_USERNAME=root",
        "MONGO_INITDB_ROOT_PASSWORD=pass",
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "GOSU_VERSION=1.12",
        "JSYAML_VERSION=3.13.1",
        "GPG_KEYS=20691EEC35216C63CAF66CE1656408E390CFB1F5",
        "MONGO_PACKAGE=mongodb-org",
        "MONGO_REPO=repo.mongodb.org",
        "MONGO_MAJOR=4.4",
        "MONGO_VERSION=4.4.3"
    ],
    "Cmd": [
        "mongod"
    ],
    "Image": "mongo:4.4.3-bionic",
    "Volumes": {
        "/data/configdb": {},
        "/data/db": {}
    },
    "WorkingDir": "",
    "Entrypoint": [
        "docker-entrypoint.sh"
    ],
    "OnBuild": null,
    "Labels": {}
},
"NetworkSettings": {
    "Bridge": "",
    "SandboxID": "442d16884f6109265a62da59b61ae7f032102676b014c3cfe257cacda7bc0b45",
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "Ports": {
        "27017/tcp": [
            {
                "HostIp": "0.0.0.0",
                "HostPort": "27017"
            }
        ]
    },
    "SandboxKey": "/var/run/docker/netns/442d16884f61",
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
    "EndpointID": "805c6b7f330eaeb0ad71be52e145eb94dcd873f53153dc977d60d95f2174718e",
    "Gateway": "172.17.0.1",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "172.17.0.2",
    "IPPrefixLen": 16,
    "IPv6Gateway": "",
    "MacAddress": "02:42:ac:11:00:02",
    "Networks": {
        "bridge": {
            "IPAMConfig": null,
            "Links": null,
            "Aliases": null,
            "NetworkID": "58ebef1a074efe7c6d9d50e0856fd09d194bdeba5350affb9f869c8df6875ae0",
            "EndpointID": "805c6b7f330eaeb0ad71be52e145eb94dcd873f53153dc977d60d95f2174718e",
            "Gateway": "172.17.0.1",
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "MacAddress": "02:42:ac:11:00:02",
            "DriverOpts": null
        }
    }
}
}
```

attach(container, stdout=True, stderr=True, stream=False, logs=False, demux=False)

attach_socket(container, params=None, ws=False)

commit(container, repository=None, tag=None, message=None, author=None, changes=None, conf=None)

containers(quiet=False, all=False, trunc=False, latest=False, since=None, before=None, limit=-1, size=False, filters=None)

create_container(image, command=None, hostname=None, user=None, detach=False, stdin_open=False, tty=False, ports=None, environment=None, volumes=None, network_disabled=False, name=None, entrypoint=None, working_dir=None, domainname=None, host_config=None, mac_address=None, labels=None, stop_signal=None, networking_config=None, healthcheck=None, stop_timeout=None, runtime=None, use_config_proxy=True)

create_container_config(\*args, \*\*kwargs)

create_container_from_config(config, name=None)

create_endpoint_config(\*args, \*\*kwargs)

create_host_config(\*args, \*\*kwargs)

create_networking_config(\*args, \*\*kwargs)

diff(container)

export(container, chunk_size=2097152)

get_archive(container, path, chunk_size=2097152, encode_stream=False)

inspect_container(container)

kill(container, signal=None)

logs(container, stdout=True, stderr=True, stream=False, timestamps=False, tail='all', since=None, follow=None, until=None)

pause(container)

port(container, private_port)

prune_containers(filters=None)

put_archive(container, path, data)

remove_container(container, v=False, link=False, force=False)

rename(container, name)

resize(container, height, width)

restart(container, timeout=10)

start(container, \*args, \*\*kwargs)

stats(container, decode=None, stream=True)

stop(container, timeout=None)

top(container, ps_args=None)

unpause(container)

update_container(container, blkio_weight=None, cpu_period=None, cpu_quota=None, cpu_shares=None, cpuset_cpus=None, cpuset_mems=None, mem_limit=None, mem_reservation=None, memswap_limit=None, kernel_memory=None, restart_policy=None)

wait(container, timeout=None, condition=None)

### Images

get_image(image, chunk_size=2097152)

history(image)

images(name=None, quiet=False, all=False, filters=None)

import_image(src=None, repository=None, tag=None, image=None, changes=None, stream_src=False)

import_image_from_data(data, repository=None, tag=None, changes=None)

import_image_from_file(filename, repository=None, tag=None, changes=None)

import_image_from_image(image, repository=None, tag=None, changes=None)

import_image_from_stream(stream, repository=None, tag=None, changes=None)

import_image_from_url(url, repository=None, tag=None, changes=None)

inspect_distribution(image, auth_config=None)

inspect_image(image)

load_image(data, quiet=None)

prune_images(filters=None)

pull(repository, tag=None, stream=False, auth_config=None, decode=False, platform=None, all_tags=False)

push(repository, tag=None, stream=False, auth_config=None, decode=False)

remove_image(image, force=False, noprune=False)

search(term, limit=None)

tag(image, repository, tag=None, force=False)

### Building images

build(path=None, tag=None, quiet=False, fileobj=None, nocache=False, rm=False, timeout=None, custom_context=False, encoding=None, pull=False, forcerm=False, dockerfile=None, container_limits=None, decode=False, buildargs=None, gzip=False, shmsize=None, labels=None, cache_from=None, target=None, network_mode=None, squash=None, extra_hosts=None, platform=None, isolation=None, use_config_proxy=True)

### Networks

connect_container_to_network(container, net_id, ipv4_address=None, ipv6_address=None, aliases=None, links=None, link_local_ips=None, driver_opt=None)

create_network(name, driver=None, options=None, ipam=None, check_duplicate=None, internal=False, labels=None, enable_ipv6=False, attachable=None, scope=None, ingress=None)

disconnect_container_from_network(container, net_id, force=False)

inspect_network(net_id, verbose=None, scope=None)

networks(names=None, ids=None, filters=None)

prune_networks(filters=None)

### Volumes

create_volume(name=None, driver=None, driver_opts=None, labels=None)

inspect_volume(name)

prune_volumes(filters=None)

remove_volume(name, force=False)

volumes(filters=None)

### Executing commands in containers

exec_create(container, cmd, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', environment=None, workdir=None, detach_keys=None)

exec_inspect(exec_id)

exec_resize(exec_id, height=None, width=None)

exec_start(exec_id, detach=False, tty=False, stream=False, socket=False, demux=False)
