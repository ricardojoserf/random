from sys import argv

from mininet.topo import Topo
from mininet.net import Mininet


class Tarea( Topo ):
    
    def __init__( self ):
        
        # Initialize topology
        Topo.__init__( self )

 	switchList = []
	swCount = 0
	hostCount = 0

	rings_sizes = ['13','5','6']	
	
	hosts_r1 = ['0','0','1','1','0','2','1','0','1','0','0','0','2']		
	sw_r1 = [ ['0','0'], ['0','0'] , ['0','0'] , ['1','2'] , ['1','2'] , ['0','0'] , ['1','3'] , ['0','0'] , ['0','0'] , ['0','0'] , ['1','2'] , ['1','3'] ,['0','0'] ]

	hosts_r2 = ['0','1','0','1','0']
	sw_r2 = [ ['1','2'] , ['0','0'] , ['1','2'] , ['0','0'] , ['0','0'] ]

	hosts_r3 = ['1','1','1','0','0','0']
	sw_r3 = [ ['0','0'] , ['1','1'] , ['1','1'] , ['1','2'] , ['2','1'], ['0','0'] ]

	

	for i in range(int(rings_sizes[0])):

		switchList.append(self.addSwitch('sw%s' % (swCount)))
		swCount += 1
				
		for i in range(int(hosts_r1[i])):
			host = self.addHost('h%s' % (hostCount))
			hostCount += 1
			self.addLink(host, switchList[swCount-1], bw=100, delay='2ms')

		if swCount > 1:
			self.addLink(switchList[swCount-1], switchList[swCount-2], bw=1000, delay='3ms')
		

	for i in range(int(rings_sizes[0])):

		for j in range(int(sw_r1[i][0])):

			switchList.append(self.addSwitch('sw%s' % (swCount)))
			swCount += 1
			self.addLink(switchList[swCount-1], switchList[i], bw=1000, delay='3ms')
			
			for k in range(int(sw_r1[i][1])):
	
				host = self.addHost('h%s' % (hostCount))
				hostCount += 1
				self.addLink(host, switchList[swCount-1], bw=100, delay='2ms')
		
	self.addLink(switchList[0],switchList[12], bw=1000, delay='3ms')

	flag1 = swCount + 1

	for i in range(int(rings_sizes[1])):

		switchList.append(self.addSwitch('sw%s' % (swCount)))
		swCount += 1

		for j in range(int(hosts_r2[i])):
			host = self.addHost('h%s' % (hostCount))
			hostCount += 1
			self.addLink(host, switchList[swCount-1], bw=100, delay='2ms')

		if swCount > flag1:
			self.addLink(switchList[swCount-1], switchList[swCount-2], bw=1000, delay='3ms')


	self.addLink(switchList[flag1-1],switchList[8], bw=1000, delay='3ms')
	self.addLink(switchList[swCount-1],switchList[10], bw=1000, delay='3ms')

	for i in range(int(rings_sizes[1])):
		for j in range(int(sw_r2[i][0])):
			switchList.append(self.addSwitch('sw%s' % (swCount)))
			swCount += 1
			self.addLink(switchList[swCount-1], switchList[flag1 + i - 1], bw=1000, delay='3ms')

			for k in range(int(sw_r2[i][1])):
				host = self.addHost('h%s' % (hostCount))
				hostCount += 1
				self.addLink(host, switchList[swCount-1], bw=100, delay='2ms')

	flag2 = swCount + 1

	for i in range(int(rings_sizes[2])):

		switchList.append(self.addSwitch('sw%s' % (swCount)))
		swCount += 1

		for j in range(int(hosts_r3[i])):
			host = self.addHost('h%s' % (hostCount))
			hostCount += 1
			self.addLink(host, switchList[swCount-1], bw=100, delay='2ms')

		if swCount > flag2:
			self.addLink(switchList[swCount-1], switchList[swCount-2], bw=1000, delay='3ms')

	for i in range(int(rings_sizes[2])):

		for j in range(int(sw_r3[i][0])):

			switchList.append(self.addSwitch('sw%s' % (swCount)))
			swCount += 1
			self.addLink(switchList[swCount-1], switchList[i + flag2 -1], bw=1000, delay='3ms')
			
			for k in range(int(sw_r3[i][1])):
	
				host = self.addHost('h%s' % (hostCount))
				hostCount += 1
				self.addLink(host, switchList[swCount-1], bw=100, delay='2ms')

	self.addLink(switchList[0],switchList[30], bw=1000, delay='3ms')
	self.addLink(switchList[1],switchList[25], bw=1000, delay='3ms')

	host = self.addHost('h%s' % (hostCount))
	hostCount += 1
	self.addLink(host, switchList[34], bw=100, delay='2ms')


topos = { 'tarea': ( lambda: Tarea() ) }
