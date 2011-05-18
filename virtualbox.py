from time import sleep

import vboxapi

# from libcloud.compute.providers import Provider
from libcloud.compute.types import NodeState
from libcloud.compute.base import Node, NodeDriver
from libcloud.compute.base import NodeSize, NodeImage


class VirtualBoxNodeImage(NodeImage):
    def __init__(self, appliance, *args, **kwargs):
        self._appliance = appliance
        
        info = self._appliance.getVirtualSystemDescriptions()[0].getDescriptionByType(3)
        
        settings = {
            'id': info[2][0],
            'name': info[3][0],
        }
        settings.update(kwargs)
        
        super(VirtualBoxNodeImage, self).__init__(*args, **settings)
    

class VirtualBoxNode(Node):
    def __init__(self, machine, *args, **kwargs):
        self._machine = machine
        
        state = NodeState.RUNNING if self._machine.state is 5 else NodeState.PENDING
        ip = self._machine.enumerateGuestProperties('*/IP')
        
        settings = {
            'id': self._machine.id,
            'name':self._machine.name,
            'state': state,
            'public_ip': ip[1],
            'private_ip': [],
        }
        settings.update(kwargs)
        
        super(VirtualBoxNode, self).__init__(*args, **settings)
    

class VirtualBoxNodeDriver(NodeDriver):
    type = 32
    name = "VirtualBox"
    
    def __init__(self, key='', *args, **kwargs):
        super(VirtualBoxNodeDriver, self).__init__(key, *args, **kwargs)
        
        self._manager = vboxapi.VirtualBoxManager(None, None)
        self._session = self._manager.mgr.getSessionObject(self._manager.vbox)
    
    def _to_node(self, machine):
        return VirtualBoxNode(machine, driver=self.connection.driver)
    
    def _to_image(self, path):
        appliance = self._manager.vbox.createAppliance()
        
        appliance.read(path)
        appliance.interpret()
        
        return VirtualBoxNodeImage(appliance, driver=self.connection.driver)
    
    def create_node(self, name, image, size, **kwargs):
        appliance = self._manager.vbox.createAppliance()
        
        appliance.read(image._appliance.path)
        appliance.interpret()
        
        self._manager.getArray(appliance, 'virtualSystemDescriptions')
        
        for desc in self._manager.getArray(appliance, 'virtualSystemDescriptions'):
            values = desc.getDescription()
            
            values[3][1] = name
            
            desc.setFinalValues([True] * len(values[3]), values[3], values[4])
        
        progress = appliance.importMachines()
        
        p = -1
        while not progress.completed:
            if progress.percent > p:
                p = progress.percent
                print '%s%%%s' % (p,  ((' (ETA %s seconds)' % progress.timeRemaining) if p > 20 else ''))
            
            sleep(1)
        
        machine = self._manager.getArray(appliance, 'machines')[0]        
        machine = self._manager.vbox.findMachine(machine)
        
        node = self._to_node(machine)
        
        print self.startup_node(node)
        
        return node
    
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
        self.shutdown_node(node)
        
        return self.startup_node(node)
    
    def startup_node(self, node):
        if node._machine.state is 5:
            return node._machine.state
        
        session = self._manager.mgr.getSessionObject(self._manager.vbox)
        
        progress = node._machine.launchVMProcess(session, 'headless', '')
        progress.waitForCompletion(-1)
        
        session.unlockMachine()
        
        return True if progress.resultCode is 0 else False
    
    def shutdown_node(self, node):
        if node._machine.state is not 5:
            return False
        
        session = self._manager.mgr.getSessionObject(self._manager.vbox)
        node._machine.lockMachine(session, self._manager.constants.LockType_Shared)
        
        progress = session.console.powerDown()
        progress.waitForCompletion(-1)
        
        session.unlockMachine()
        
        return True if progress.resultCode is 0 else False
    
    def list_nodes(self):
        return [self._to_node(vm) for vm in self._manager.getArray(self._manager.vbox, 'machines')]
    
    def list_images(self, locations=[]):
        return [self._to_image(path) for path in locations]
    
    def list_sizes(self):
        return [NodeSize(id='', name='', ram='', disk='', bandwidth=0, price=0, driver=self.connection.driver)]
    
