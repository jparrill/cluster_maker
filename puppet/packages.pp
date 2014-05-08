class puppet::packages inherits puppet::params {
    yumrepo { '10gen':
        descr    => '10Gen MongoDB Repository',
        baseurl  => $puppet::params::MongoDB_repo,
        enabled  => 1,
        gpgcheck => 0,
        metadata_expire => 30,
    }

    package { $puppet::params::MongoDB_rpms:
        ensure  => latest,
        require => Yumrepo['10gen'],
    }
}
