from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time
import config
import re
import os
import json

log = core.getLogger()
_flood_delay = 0

def printState (tabla):

    taggedPorts = []
    in2VLANSPorts = []

    for i in tabla:
      for j in i.get('ports'):
        if (j.get('type') == "tagged"):
          taggedPorts.append( { 'port': j.get('port'), 'taggedVlan': i.get('vlan') } )

    for i in tabla:  
      for j in i.get('ports'):
        for k in range ( len ( taggedPorts ) ):
          if (j.get('port') == taggedPorts[k].get('port') and (i.get('vlan') != taggedPorts[k].get('taggedVlan') ) ):
            in2VLANSPorts.append( {'port': j.get('port'), 'untaggedVlan': i.get('vlan'), 'taggedVlan': taggedPorts[k].get('taggedVlan') } )
       
    for i in taggedPorts:
      for k in in2VLANSPorts:
        if ( ( i.get('taggedVlan') == k.get('taggedVlan') ) and ( i.get('port') == k.get('port') ) ):
          taggedPorts.remove(i)

    print( ("Puertos con 1 VLAN etiq.: {0}").format(taggedPorts)   )     
    print( ("Puertos con 1 VLAN etiq. y 1 no: {0}").format(in2VLANSPorts) )


def importData():
  script_dir = os.path.dirname(__file__)
  path = script_dir + '/config.txt' 
  file = open(path, 'r')
  content = file.read()
  values = content.split("\n")
  arrValues = []
  for v in values:
    v = re.sub('[ ]*\=[ ]*', ' = ' ,v)
    v = re.sub('[ ]*\:[ ]*', ' : ' ,v)

    if ( len(v.split(" = ")) >= 2 ):
      
      if ( len(v.split(" = ")[1].split(" : ")) >= 2 ):
        arrValues.append([ v.split(" = ")[0] , v.split(" = ")[1].split(" : ")[0], v.split(" = ")[1].split(" : ")[1]  ])
  
      else:
        arrValues.append([ v.split(" = ")[0] , v.split(" = ")[1]  ])
  
  tabla = []
  i = 0
 
  while i < ( len(arrValues) - 1 ):
    ports = []
    vlanId = None
    if len(arrValues[i]) == 2:
      vlanId = arrValues[i][1]
      
      i += 1
      
      while ( len(arrValues[i]) == 3):
        ports.append( { 'port': str(arrValues[i][1]), 'type': str(arrValues[i][2]) } )
        if ( i < (len(arrValues) -1) ):
          i +=1
        else:
          break

      tabla.append({'vlan': str(vlanId), 'ports': ports })
      

  return tabla
  

class LearningSwitch (object):
  
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent

    # En caso de querer comprobar que el objeto es el mismo
    checkimportedData = True

    if (checkimportedData):
    
      print ("1 - Objeto creado parseando el txt (lento)")
      tabla = importData()
      print(json.dumps(tabla,sort_keys=True, indent=2))

      print("2 - Objeto tomado como variable de otro fichero .py (mejor)")
      print(json.dumps(config.tabla,sort_keys=True, indent=2))
      
          
    printState(config.tabla)


    # Our table
    self.macToPort = []

    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    # We just use this to know when to log a helpful message
    self.hold_down_expired = _flood_delay == 0

    #log.debug("Initializing LearningSwitch, transparent=%s",
    #          str(self.transparent))


  def _handle_PacketIn (self, event):
    
    packet = event.parsed
    
    def getVlan(port, id_):

      res = None
      if (id_ != None):
        res =  id_
      else:

        tabla = importData()
    	
      	for i in tabla:		
    		    for j in i.get('ports'):
    			if (j.get('port') == port):
    				res = i.get('vlan') 	
	
    	return res


    def tagType (portname, vlanname):
      tabla = importData()
      for i in tabla:
        if i.get('vlan') == str(vlanname):
    			for j in i.get('ports'):
    				if(j.get('port') == str(portname)):					
    					ttype = j.get('type')
    					return ttype


    def flood (message = None):

      srcPort = str(event.port)
      if ( packet.find('vlan') is not None ):
    		  vlanId = getVlan( srcPort, packet.find('vlan').id  )
      else:
    		  vlanId = getVlan( srcPort, None )
     
      put = True  
      for i in self.macToPort:
        if ( ( i.get('mac')== packet.src ) and ( i.get('port')== int(srcPort) ) and ( i.get('vlan')== vlanId ) ):
          put = False

      if (put):
        self.macToPort.append ({ 'mac': packet.src, 'port': int(srcPort), 'vlan': vlanId })     

      taggedPorts = []
      untaggedPorts = []	
      tabla = importData()

      for i in tabla:		
    	     if i.get('vlan') == str(vlanId):
    		    for j in i.get('ports'):	
         			if (j.get('port') != srcPort and j.get('type') == "tagged"):
        				taggedPorts.append(j.get('port'))
        			if (j.get('port') != srcPort and j.get('type') == "untagged"):
        				untaggedPorts.append(j.get('port'))
      
      tag = tagType(srcPort, vlanId)

      msg = of.ofp_flow_mod()
      msg.match.in_port = int ( srcPort ) 

    	# Tagged	
      if tag == "tagged":
        # print ("FLOOD from T-port {0}").format(srcPort)
    		# T a T
        for i in taggedPorts:
    			msg.actions.append( of.ofp_action_output( port = int(i)  ) )			  
    		# T a U	
        if untaggedPorts != []:
            msg.actions.append(of.ofp_action_strip_vlan())
        for i in untaggedPorts:
    			msg.actions.append( of.ofp_action_output( port = int(i)  ) )	
    	# Untagged
      if tag == "untagged":	
        # print ("FLOOD from U-port {0}").format(srcPort)
    		# U a U
        for i in untaggedPorts:
          msg.actions.append( of.ofp_action_output( port = int(i)  ) )
    		# U a T
        if taggedPorts != []:
            msg.actions.append(of.ofp_action_vlan_vid(vlan_vid=int(vlanId)) )				
        for i in taggedPorts:
          msg.actions.append( of.ofp_action_output( port = int(i)  ) )	
    	
      self.connection.send(msg)
      return
      


    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    if not self.transparent: # 2
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop() # 2a
        return

    if packet.dst.is_multicast:
      flood() # 3a
    
    else:

      vlan = None

      if ( packet.find('vlan') is not None ):
        vlan =  packet.find('vlan').id
      else:
        vlan = None

      found = False
      
      if vlan != None:
      
        for i in self.macToPort:
          if (i.get('mac') == packet.dst and i.get('vlan') == vlan):
            port = int ( i.get('port') )
            found = True
    
      if vlan == None:
            tabla = importData()

            for j in tabla:
                for k in j.get('ports'):
                  if (str(event.port) == str(k.get('port'))  and k.get('type') == "untagged"):
                    # port = k.get('port')
                    vlan = j.get('vlan')
                    
            if (vlan != None):
              for i in self.macToPort:
                if (str( i.get('mac') ) == str( packet.dst ) and str( i.get('vlan') ) == str( vlan ) ):
                  port = i.get('port')
                  found = True


      if not found: # 4
        flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a

      else:
   
        vlanId = vlan
        
        put = True  
        for i in self.macToPort:
          if ( ( i.get('mac')== packet.src ) and ( i.get('port')== int(event.port) ) and ( i.get('vlan')== vlanId ) ):
            put = False

        if (put):
          self.macToPort.append ({ 'mac': packet.src, 'port': int(event.port), 'vlan': vlanId })  

        if port == event.port: # 5
          log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        
      	tag1 = tagType(str(event.port), str(vlanId) )
        tag2 = tagType(str(port), str(vlanId) )

        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.data = event.ofp # 6a

        # Tagged  
        if tag1 == "tagged":
            if tag2 == "tagged":
              msg.actions.append( of.ofp_action_output( port = int(port)  ) )          
            if tag2 == "untagged":
              msg.actions.append(of.ofp_action_strip_vlan())
              msg.actions.append( of.ofp_action_output( port = int(port)  ) )  
        
        # Untagged  
        if tag1 == "untagged":
            if tag2 == "untagged":
              msg.actions.append( of.ofp_action_output( port = int(port)  ) )          
            if tag2 == "tagged":
              msg.actions.append(of.ofp_action_vlan_vid(vlan_vid=int(vlanId)) )       
              msg.actions.append( of.ofp_action_output( port = int(port)  ) )          
            
        self.connection.send(msg)
        return

    



class l2_learning (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, transparent):
    core.openflow.addListeners(self)
    self.transparent = transparent

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay):
  """
  Starts an L2 learning switch.
  """
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")

  core.registerNew(l2_learning, str_to_bool(transparent))
