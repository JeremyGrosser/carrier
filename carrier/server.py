import simplejson as json
import struct
import bottle

from control import VirtualMachine

bottle.debug(True)

def load_servers():
    try:
        servers = json.load(file('/mnt/vm/servers.json'))
        for name in servers:
            servers[name] = VirtualMachine(servers[name])
    except:
        servers = {}
    return servers

def save_servers(servers):
    res = {}
    for name in servers:
        res[name] = servers[name].get_config()
    json.dump(file('/mnt/vm/servers.json', 'w'), res)

def genconfig(console_base=3000, mac_prefix='02:52:0a'):
    nextid = 1
    while True:
        yield {
            'console': console_base + nextid,
            'vnc': nextid,
            'mac': '%s:%s' % (mac_prefix, ':'.join(['%02X' % ord(x) for x in struct.pack('>I', nextid)[1:]])),
            'nic': 'e1000',
            'memory': 1024,
            'disk': 10,
            'boot': 'n',
        }
        nextid += 1
    return

newconfig = genconfig()
servers = load_servers()

@bottle.post('/api/1/:server/:action')
def server_action(server, action):
    vm = servers[server]
    if action == 'stop':
        vm.stop()
    if action == 'start':
        vm.start()

    bottle.response.content_type = 'text/javascript'
    return json.dumps({
        'state': vm.get_state(),
        'config': vm.get_config(),
    }, indent=2)

@bottle.post('/api/1/:server')
def server_create(server):
    if server in servers:
        bottle.abort(409, 'Server %s already exists.' % server)

    config = newconfig.next()   
    config.update(json.load(bottle.request.body))
    config['name'] = server

    vm = VirtualMachine(config)
    servers[server] = vm
    save_servers(servers)

    bottle.response.content_type = 'text/javascript'
    return json.dumps({
        'state': vm.get_state(),
        'config': config,
    }, indent=2)

@bottle.put('/api/1/:server')
def server_update(server):
    config = json.load(bottle.request.body)
    vm = servers[server]

    if vm.get_state() != 'STOPPED': 
        bottle.abort(400, 'Cannot modify a running VM, stop it first.')
    vm.update(config)
    save_servers(servers)

    bottle.response.content_type = 'text/javascript'
    return json.dumps({
        'state': vm.get_state(),
        'config': vm.get_config(),
    }, indent=2)

@bottle.delete('/api/1/:server')
def server_delete(server):
    vm = servers[server]

    if vm.get_state() != 'STOPPED':
        bottle.abort(400, 'Cannot delete a running VM, stop it first.')
    vm.delete()
    del servers[server]
    save_servers(servers)
    return

@bottle.get('/api/1/:server')
def server_status(server):
    vm = servers[server]
    result = {
        'config': vm.get_config(),
        'state': vm.get_state(),
    }

    bottle.response.content_type = 'text/javascript'
    return json.dumps(result, indent=2)

@bottle.get('/api/1/')
def server_list():
    bottle.response.content_type = 'text/javascript'
    return json.dumps(servers.keys(), indent=2)

application = bottle.app()

if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=3000, server=bottle.PasteServer)
