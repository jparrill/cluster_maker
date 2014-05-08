class puppet::params {
    $MongoDB_rpms         = [ 'mongodb-org', 'mongodb-org-server', 'mongodb-org-mongos', 'mongodb-org-shell', 'mongodb-org-tools' ]
    $MongoDB_repo         = "http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/"
}
