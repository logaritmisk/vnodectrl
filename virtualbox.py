from time import sleep

import vboxapi

from libcloud.compute.types import NodeState
from libcloud.compute.base import Node, NodeDriver
from libcloud.compute.base import NodeSize, NodeImage


def machine_loader(fn):
	def decorate(*largs):
		return lambda *args: fn(*(largs + args))
	
	return decorate


@machine_loader
def machine_from_imachine(imachine, node=None, *args, **kwargs):
    node._machine = imachine
    
    node.name = node._machine.name
    node.state = NodeState.RUNNING if node._machine.state is 5 else NodeState.PENDING
    node.public_ip = node._machine.enumerateGuestProperties('*/IP')[1]
    
    return True

@machine_loader
def machine_from_iappliance(iappliance, iprogress, node=None, *args, **kwargs):
    if not iprogress.completed:
        return False
    
    machines = node.driver._manager.getArray(iappliance, 'machines')
    machine = machines[0]
    
    machine = node.driver._manager.vbox.findMachine(machine)
    
    return machine_from_imachine(machine)(node)


class VirtualBoxNodeImage(NodeImage):
    def __init__(self, appliance, *args, **kwargs):
        self._appliance = appliance
        
        info = self._appliance.getVirtualSystemDescriptions()[0].getDescriptionByType(3)
        
        settings = {
            'id': info[2][0],
            'name': info[3][0],
        }
        settings.update(kwargs)
        
        NodeImage.__init__(self, *args, **settings)
    

class VirtualBoxNode(Node):
    def __init__(self, loader, *args, **kwargs):    
        self._loader = loader
        
        settings = {
            'id': '',
            'name': '',
            'state': NodeState.UNKNOWN,
            'public_ip': [],
            'private_ip': [],
        }
        settings.update(kwargs)
        
        Node.__init__(self, *args, **settings)
    
    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        
        if name is '_loader':
            return value
        
        if self._loader:
            loader, self._loader = self._loader, None
            
            if not loader(self):
                self._loader = loader
        
        return value
    

class VirtualBoxNodeDriver(NodeDriver):
    type = 32
    name = "VirtualBox"
    
    def __init__(self, *args, **kwargs):
        NodeDriver.__init__(self, *args, **kwargs)
        
        self._manager = vboxapi.VirtualBoxManager(None, None)
        self._session = self._manager.mgr.getSessionObject(self._manager.vbox)
    
    def _to_node(self, loader):
        return VirtualBoxNode(loader, driver=self.connection.driver)
    
    def _to_image(self, path):
        appliance = self._manager.vbox.createAppliance()
        
        appliance.read(path)
        appliance.interpret()
        
        return VirtualBoxNodeImage(appliance, driver=self.connection.driver)
    
    def create_node(self, name, image, size, **kwargs):
        appliance = self._manager.vbox.createAppliance()
        
        appliance.read(image._appliance.path)
        appliance.interpret()
        
        constants = self._manager.constants.all_values('VirtualSystemDescriptionType')
        
        for desc in self._manager.getArray(appliance, 'virtualSystemDescriptions'):
            values = desc.getDescription()
            
            values[constants['Name']][1] = name
            
            desc.setFinalValues([True] * len(values[3]), values[3], values[4])
        
        progress = appliance.importMachines()
        
        if kwargs.get('wait', False):
            progress.waitForCompletion(kwargs.get('timeout', -1))
        
        return self._to_node(machine_from_iappliance(appliance, progress))
    
    def destroy_node(self, node):
        constants = self._manager.constants.all_values('SessionState')
        
        if node._machine.sessionState is not constants['Unlocked']:
            return False
        
        constants = self._manager.constants.all_values('CleanupMode')
        
        mediums = node._machine.unregister(constants['Full'])
        progress = node._machine.delete(mediums)
        
        progress.waitForCompletion(-1)
        
        return True if progress.resultCode is 0 else False
    
    def reboot_node(self, node):
        self.ex_shutdown_node(node)
        
        return self.ex_startup_node(node)
    
    def list_nodes(self):
        return [self._to_node(machine_from_imachine(machine)) for machine in self._manager.getArray(self._manager.vbox, 'machines')]
    
    def list_images(self, locations=[]):
        return [self._to_image(path) for path in locations]
    
    def list_sizes(self):
        return [NodeSize(id='', name='', ram='', disk='', bandwidth=0, price=0, driver=self.connection.driver)]
    
    def ex_startup_node(self, node):
        if node._machine.state is 5:
            return node._machine.state
        
        session = self._manager.mgr.getSessionObject(self._manager.vbox)
        
        progress = node._machine.launchVMProcess(session, 'headless', '')
        progress.waitForCompletion(-1)
        
        session.unlockMachine()
        
        return True if progress.resultCode is 0 else False
    
    def ex_shutdown_node(self, node):
        if node._machine.state is not 5:
            return False
        
        session = self._manager.mgr.getSessionObject(self._manager.vbox)
        node._machine.lockMachine(session, self._manager.constants.LockType_Shared)
        
        progress = session.console.powerDown()
        progress.waitForCompletion(-1)
        
        session.unlockMachine()
        
        return True if progress.resultCode is 0 else False
    
