#!/usr/bin/python

import socket
import ConfigParser
import logging
import sys
import shutil
from os.path import realpath, dirname, exists
from os import makedirs
import jinja2


class clusterMaker(object):
    '''
    Make a Vagrantfile based on a base template
    catching a config file parameters
    '''
    def __init__(self):
        self.get_config()

    def get_config(self, config_file='vm_maker.ini'):
        ## Catch config from config file
        self.file_path = dirname(realpath(__file__))
        config = ConfigParser.RawConfigParser()
        config.read(self.file_path + '/conf/' + config_file)
        for section in config.sections():
            ## IF there is more than one node, repeat
            self.vm_box_name = config.get(section, 'vm_box_name')
            self.vm_box_url = config.get(section,'vm_box_url')
            self.vm_box_ip = config.get(section,'vm_box_ip')
            self.vm_box_hostname = config.get(section, 'vm_box_hostname')
            self.vm_ssh_port = config.get(section, 'vm_ssh_port')
            self.make_tree()
            self.make_vf()
            self.make_cf()

    def write_file(self, file_path, _vars ,temp_hand):
        ## Create File
        file_h = open(file_path, 'w')
        file_h.write(temp_hand.render(_vars))
        file_h.close()


    def make_tree(self):
        ## Make a folders tree for the VM
        if not exists(self.file_path + '/tmp/' + self.vm_box_hostname):
            makedirs(self.file_path + '/tmp')
            makedirs(self.file_path + '/tmp/' + self.vm_box_hostname)
            makedirs(self.file_path + '/tmp/' + self.vm_box_hostname + '/mdb_config')

    def jinja_base(self):
        ## Templates load and
        templateLoader = jinja2.FileSystemLoader(searchpath="%s/templates/" % self.file_path)
        templateEnv = jinja2.Environment(loader=templateLoader)
        return templateEnv

    def make_vf(self):
        ## Make VF inside of a node folder
        templateEnv = self.jinja_base()
        template = templateEnv.get_template("Vagrantfile")
        templateVars = {
            "VM_BOX_NAME" : self.vm_box_name,
            "VM_BOX_URL" : self.vm_box_url,
            "VM_BOX_IP" : self.vm_box_ip,
            "VM_BOX_HOSTNAME" : self.vm_box_hostname,
            "VM_SSH_PORT" : self.vm_ssh_port,
        }
        self.write_file(self.file_path + '/tmp/' + self.vm_box_hostname + '/Vagrantfile', templateVars, template)
        shutil.copytree(self.file_path + '/puppet', self.file_path + '/tmp/' + self.vm_box_hostname + '/puppet' )

    def make_cf(self):
        ## Prepare MongoDB files
        # Shard1
        templateEnv = self.jinja_base()
        template = templateEnv.get_template("shard_server.conf")
        templateVars = {
            "VM_BOX_IP" : self.vm_box_ip,
            "SHARD_PORT" : '10001',
            "SHARD_INSTANCE" : '1',
        }
        self.write_file(self.file_path + '/tmp/' + self.vm_box_hostname + '/mdb_config/' + 'shard_server_1.conf', templateVars, template)

        # Shard2
        templateVars = {
            "VM_BOX_IP" : self.vm_box_ip,
            "SHARD_PORT" : '10002',
            "SHARD_INSTANCE" : '2',
        }
        self.write_file(self.file_path + '/tmp/' + self.vm_box_hostname + '/mdb_config/' + 'shard_server_2.conf', templateVars, template)

        # Arbiter
        arbiter = templateEnv.get_template("arbiter_server.conf")
        self.write_file(self.file_path + '/tmp/' + self.vm_box_hostname + '/mdb_config/' + 'arbiter_server.conf', templateVars, arbiter)

        # MongoC
        configuration = templateEnv.get_template("config_server.conf")
        self.write_file(self.file_path + '/tmp/' + self.vm_box_hostname + '/mdb_config/' + 'config_server.conf', templateVars, configuration)

        # MongoS
        mongos = templateEnv.get_template("mongos_server.conf")
        templateVars = {
            "VM_BOX_IP" : self.vm_box_ip,
        }
        self.write_file(self.file_path + '/tmp/' + self.vm_box_hostname + '/mdb_config/' + 'mongos_server.conf', templateVars, mongos)


clusterMaker()
