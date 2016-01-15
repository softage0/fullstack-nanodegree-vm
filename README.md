# Tournament Planner

Tournament Planner is a planner to arrange Swiss Tournament style games.


## Quick start

Several quick start options are available:

* Download [the latest Vagrant](https://www.vagrantup.com/downloads.html) and install.
* Clone the repo: `git clone https://github.com/softage0/udacity-fsnd-p2.git`.
* Run the following code on the cloned repo:
```
$ cd vagrant
$ vagrant up (It would take several minutes to install and setup the relevant environment.)
```
* Run the following code to setup the initial database:
```
$ vagrant ssh
vagrant$ cd /vagrant/tournament
vagrant$ psql
psql$ create database tournament
psql$ /c tournament
psql$ /i tournament.sql
psql$ /q
```
* Run tournament_test.py for unit test
```
vagrant$ python tournament_test.py
```
