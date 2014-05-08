class puppet::services {
    define start_processes($mongo, $path_conf) {
        exec { "start process ${mongo} -f ${path_conf}":
            command => "/usr/bin/${mongo} -f ${path_conf}",
            onlyif  => "test -f ${path_conf}",
            path    => "/bin:/usr/bin",
            require => Exec['delete.lock'],
        }
    }

    exec { "delete.lock":
        command => "find /var/lib/mongo/ -name *.lock | xargs rm -rf",
        path    => "/bin:/usr/bin",
    }

    notify {"Cluster Maker - Starting Cluster Processes":}
    ->
    start_processes
        {
            "shard_server_1": mongo  => 'mongod', path_conf =>'/etc/mongo/shard_server_1.conf';
            "shard_server_2": mongo  => 'mongod', path_conf =>'/etc/mongo/shard_server_2.conf', require => Exec['start process mongod -f /etc/mongo/shard_server_1.conf'];
            "arbiter_server": mongo => 'mongod', path_conf =>'/etc/mongo/arbiter_server.conf', require => Exec['start process mongod -f /etc/mongo/shard_server_2.conf'];
            "config_server": mongo => 'mongod', path_conf =>'/etc/mongo/config_server.conf', require => Exec['start process mongod -f /etc/mongo/arbiter_server.conf'];
            "config_server_1": mongo => 'mongod', path_conf =>'/etc/mongo/config_server_1.conf', require => Exec['start process mongod -f /etc/mongo/config_server.conf'];
            "config_server_2": mongo => 'mongod', path_conf =>'/etc/mongo/config_server_2.conf', require => Exec['start process mongod -f /etc/mongo/config_server_1.conf'];
            "config_server_3": mongo => 'mongod', path_conf =>'/etc/mongo/config_server_3.conf', require => Exec['start process mongod -f /etc/mongo/config_server_2.conf'];
            "mongos": mongo => 'mongos', path_conf =>'/etc/mongo/mongos_server.conf', require => Exec['start process mongod -f /etc/mongo/config_server_3.conf'];
        }
}
