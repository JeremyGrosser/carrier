##################################
  API Documentation
##################################

:Release: |version|
:Date: |today|

Endpoints
~~~~~~~~~

/api/1/
=======
Methods: GET

Returns a list of VMs on this host

Example::

	curl -X GET http://carrier:3000/api/1/
	["t0000", "t0001", "t0002"]

/api/1/:server
==============
Methods: GET, POST, PUT, DELETE, CONNECT

Query, create, update, and delete this server resource. POST creates a new
server object with this name, using the JSON configuration specified in the
JSON body. If an empty configuration is sent, sane defaults are used. PUT
updates the configuration for a VM in the STOPPED state only. DELETE destroys
a VM and all data associated with it. GET returns the current status and config
for the given resource.

Examples::

	curl -X POST --data-binary '{
		"memory": 1024,
		"disk": 50
	}' http://carrier:3000/api/1/t0000
	{
	  "state": "STOPPED", 
	  "config": {
	    "vnc": 1, 
	    "name": "t0000", 
	    "nic": "e1000", 
	    "boot": "n", 
	    "mac": "02:52:0a:00:00:01", 
	    "memory": 1024, 
	    "console": 3001, 
	    "disk": 10
	  }
	}

::

	curl -X PUT --data-binary '{
		"mac": "00:11:22:33:44:55"
	}' http://carrier:3000/api/1/t0000
	{
	  "state": "STOPPED", 
	  "config": {
	    "vnc": 1, 
	    "name": "t0000", 
	    "nic": "e1000", 
	    "boot": "n", 
	    "mac": "00:11:22:33:44:55", 
	    "memory": 1024, 
	    "console": 3001, 
	    "disk": 10
	  }
	}

::

	curl -X GET http://carrier:3000/api/1/t0000
	{
	  "state": "STOPPED", 
	  "config": {
	    "vnc": 1, 
	    "name": "t0000", 
	    "nic": "e1000", 
	    "boot": "n", 
	    "mac": "00:11:22:33:44:55", 
	    "memory": 1024, 
	    "console": 3001, 
	    "disk": 10
	  }
	}

::

	curl -X DELETE http://carrier:3000/api/1/t0000
	# Returns nothing.

::

	curl -X CONNECT http://carrier:3000/api/1/t0000
	# Connects to serial console, this is a two-way connection

/api/1/:server/:action
======================
Methods: POST

Perform an action on the given server. Valid actions are: start, stop

Examples::

	curl -X POST http://carrier:3000/api/1/t0000/start
	{
	  "state": "RUNNING", 
	  "config": {
	    "vnc": 2, 
	    "name": "t0000", 
	    "nic": "e1000", 
	    "boot": "n", 
	    "mac": "02:52:0a:00:00:02", 
	    "memory": 1024, 
	    "console": 3002, 
	    "disk": 10
	  }
	}

::

	curl -X POST http://carrier:3000/api/1/t0000/stop
	{
	  "state": "STOPPED", 
	  "config": {
	    "vnc": 2, 
	    "name": "t0000", 
	    "nic": "e1000", 
	    "boot": "n", 
	    "mac": "02:52:0a:00:00:02", 
	    "memory": 1024, 
	    "console": 3002, 
	    "disk": 10
	  }
	}
