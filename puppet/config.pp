class puppet::config inherits puppet::params {
    file { '/etc/mongo':
        ensure => "directory",
        mode   => 775,
	}

    file { '/var/log/mongo':
        ensure => "directory",
        mode   => 775,
    }

    file { '/var/lib/mongo/shard_1':
        ensure => "directory",
        mode   => 775,
    }

    file { '/var/lib/mongo/shard_2':
        ensure => "directory",
        mode   => 775,
    }

    file { '/var/lib/mongo/arbiter':
        ensure => "directory",
        mode   => 775,
    }

    file { '/var/lib/mongo/config':
        ensure => "directory",
        mode   => 775,
    }

    file { '/var/run/mongo/':
        ensure => "directory",
        mode   => 775,
    }

    exec { 'move_config_files':
        command => "mv -f /vagrant/mdb_config/*.conf /etc/mongo/",
        path    => "/bin:/usr/bin",
        require => File['/etc/mongo'],
    }

}
