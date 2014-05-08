cluster_maker
=============

Tool to use for testing operations in MongoDB clusters

Requirements:
	- Vagrant
	- Virtualbox & Guest Additions
	- python2.7
	- pip
	- Virtualenv

How it works:
- Clone the Repository and execute this
```sh
cd cluster_maker
virtualenv -p python2.7 .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
python clusterMaker.py
```
Now we must to go to tmp folder and...:
```
cd tmp/node1.local
vagrant up
```
TADAAAAA!! we have all daemons of a MongoDB cluster running in a CentOS 6.4, but dont have js files to configure replicaSet and Sharding...yet

Too much work to do...
