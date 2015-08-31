#!/usr/bin/python
import base64, urlparse, sys
from optparse import OptionParser

class Container(object):
  def __init__(self):
    self.data = []

  def setAttribute(self,id,attribute,value):
    for i,d in enumerate(self.data):
      if d['id'] == int(id):
        d[attribute] = value
        return
    self.data.append(Dictate({'id':int(id)}))
    self.setAttribute(id,attribute,value)
    
  def getById(self,id):
    for i,d in enumerate(self.data):
      if d['id'] == int(id):
        return d
    return Dictate({})

  def getByAttribute(self,attribute,value):
    for i,d in enumerate(self.data):
      if d[attribute] == value:
        return d
    return Dictate({})

      
  def list(self):
    return self.data

class Dictate(object):
    """Object view of a dict, updating the passed in dict when values are set
    or deleted. "Dictate" the contents of a dict...: """

    def __init__(self, d):
        # since __setattr__ is overridden, self.__dict = d doesn't work
        object.__setattr__(self, '_Dictate__dict', d)

    # Dictionary-like access / updates
    def __getitem__(self, name):
      if name in self.__dict:
        value = self.__dict[name]
        if isinstance(value, dict):  # recursively view sub-dicts as objects
            value = Dictate(value)
        return value
      else:
        return ""

    def __setitem__(self, name, value):
        self.__dict[name] = value
    def __delitem__(self, name):
        del self.__dict[name]

    # Object-like access / updates
    def __getattr__(self, name):
      return self[name]

    def __setattr__(self, name, value):
        self[name] = value
    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.__dict)
        
    def __str__(self):
        return str(self.__dict)    

class Interfaces(Container):
    def __init__(self):
      super(Interfaces, self).__init__()
      self.map = {
        'iface_name_':'name','iface_type_':'type','iface_lan_ip_':'ipaddress','iface_static_ip_':'ipaddress','iface_comment_':'comment',
        'iface_vlan_tag_':'vlanid','iface_static_mask_':'netmask','iface_static_gateway_':'gateway',
        'iface_phys_type_':'ifacetype', 'iface_portshield_to_': 'portshieldwith','iface_ifnum_':'ifnumber'
      }
      self.ifacetype = {'0': 'Physical interface','2': 'Virtual interface' , '-1': 'Unknown'}
    
    def parse(self,_key,_value):
      number = _key.split("_")[len(_key.split("_"))-1]
      for key, value in self.map.iteritems():
        if _key.startswith(key):
          if value == 'ifacetype':
            _value = self.ifacetype[_value];
          if value == 'ipaddress' and _value == "0.0.0.0":
            continue
        
          self.setAttribute(number,value,_value)
          return True
      return False
          
    def getByIfNumber(self,number):
      return self.getByAttribute('ifnumber',number)
          
class DHCPs(Container):
    def __init__(self):
      super(DHCPs, self).__init__()
      self.map = {
        'prefs_dhdynstart_':'start','prefs_dhdynend_':'stop','prefs_dhdynrouter_':'gateway','prefs_dhdynsubnetmask_':'netmask',
        'prefs_dhdynlease_':'leasetime','prefs_dhdyndns0_':'dns1','prefs_dhdyndns1_':'dns2','prefs_dhdyndns2_':'dns3',
        'prefs_dhdynbootp_':'bootp','prefs_dhdynscopeactive_':'active',
      }
    
    def parse(self,_key,_value):
      number = _key.split("_")[len(_key.split("_"))-1]
      for key, value in self.map.iteritems():
        if _key.startswith(key):
          if value == 'active':
            _value = True if (_value == "on") else False 
          if value.startswith("dns") and _value == "0.0.0.0":
            continue
        
          self.setAttribute(number,value,_value)
          return True          
      return False

class DHCPStatic(Container):
    def __init__(self):
      super(DHCPStatic, self).__init__()
      self.map = {
        'prefs_dhstaticname_':'name','prefs_dhstaticip_':'ipaddress','prefs_dhstatichw_':'macaddress',
        'prefs_dhstaticrouter_':'gateway','prefs_dhstaticsubnetmask_':'netmask',
        'prefs_dhstaticlease_':'leasetime','prefs_dhstatictype_':'type',
        'prefs_dhstaticdns0_':'dns1','prefs_dhstaticdns1_':'dns2','prefs_dhstaticdns2_':'dns3',
      }
      self.dhstatictype = {'0': 'Physical interface','2': 'Virtual interface' , '-1': 'Unknown'}
    
    def parse(self,_key,_value):
      number = _key.split("_")[len(_key.split("_"))-1]
      for key, value in self.map.iteritems():
        if _key.startswith(key):
          if value.startswith("macaddress"):
            _value = '-'.join(a+b for a,b in zip(_value[::2], _value[1::2]))
          
          if value.startswith("dns") and _value == "0.0.0.0":
            continue
        
          self.setAttribute(number,value,_value)
          return True          
      return False



class NATs(Container):
    def __init__(self):
      super(NATs, self).__init__()
      self.map = {
        'natPolicyOrigSrc_':'src_orig','natPolicyOrigSvc_':'src_nat',
        'natPolicyOrigDst_':'dst_orig','natPolicyTransDst_':'dst_nat',
        'natPolicyOrigSvc_':'svc_orig','natPolicyTransSvc_':'svc_nat',
        'natPolicySrcIface_':'in_iface','natPolicyDstIface_':'out_iface',
        'natPolicyComment_':'comment',
        'natPolicyProbePort_':'port','natPolicyProbeType_':'type',
        'natPolocyNonDeletable':'can_delete','natPolicyEnabled_':'enabled',
      }
      self.type = {'0': 'UDP','1': 'TCP' , '-1': 'Unknown'}
    
    def parse(self,_key,_value):
      number = _key.split("_")[len(_key.split("_"))-1]
      for key, value in self.map.iteritems():
        if _key.startswith(key):          
          if value == "enabled": _value = (True if _value == "1" else False)
        
          self.setAttribute(number,value,_value)
          return True          
      return False
          
ifs = Interfaces()
dhcps = DHCPs()
dhcpstatic = DHCPStatic()
nats = NATs()
          
parser = OptionParser()
parser.add_option("-i", "--infile", dest="file", help="Set the input file")
parser.add_option("-d", "--dump", dest="dumpapa", action="store_true", default=False, help="Dump variables as is")
parser.add_option("-v", "--dumpplus", dest="dumpapaplus", action="store_true", default=False, help="Dump decoded values")
(options, args) = parser.parse_args()

          
if not options.file:
  print "Please specify a valid configuration file"
  sys.exit(1)
          
with open(options.file, "rb") as infile:
  decoded = base64.b64decode(infile.read())
  c = urlparse.parse_qsl(decoded)
  
oldpercent = 0
for i,v in enumerate(c):
  key = v[0]
  value = v[1]

  if options.dumpapa:
    print "%s = %s" % (key,value)
    continue

  percent = int((float(i+1)/len(c))*100);
  if oldpercent != percent:
    print "parsing line %d/%d %3d%% [%-100s]\r" % (i+1,len(c),percent,"".rjust(percent,"=")),
  oldpercent = percent
  sys.stdout.flush()
  
  if ifs.parse(key,value): continue
  if dhcps.parse(key,value): continue
  if dhcpstatic.parse(key,value): continue
  if nats.parse(key,value): continue
  
print "\n"
for i,ob in enumerate(ifs.list()):
  #print "%-2s | %-15s | %-10s" % (ob.id,ob.name,ob.ipaddress)
  if options.dumpapaplus:
    print ob
  else:
    print "interface id '%s' name '%s' type '%s'" % (ob.id,ob.name,ob.ifacetype),
    if (int(ob.vlanid) > 0): print "vlan '%s'" % (ob.vlanid),
    
    if (int(ob.portshieldwith) > -1): print "portshield with '%s'" % (ifs.getById(ob.portshieldwith).name),
  
    print ""
    
for i,ob in enumerate(dhcps.list()):
  if options.dumpapaplus:
    print ob
  else:
    if ob.active == False:
      continue
    
    print "dhcp range '%s-%s' netmask '%s' gateway '%s' dns" % (ob.start,ob.stop,ob.netmask,ob.gateway),
    if (ob.dns1): print "'%s'" % (ob.dns1),
    if (ob.dns2): print ",'%s'" % (ob.dns2),
    if (ob.dns3): print ",'%s'" % (ob.dns3),
  
    print ""

for i,ob in enumerate(dhcpstatic.list()):
  if options.dumpapaplus:
    print ob
  else:
    
    print "dhcp static name '%s' mac-address '%s' ip '%s' netmask '%s' gateway '%s' dns" % (ob.name,ob.macaddress,ob.ipaddress,ob.netmask,ob.gateway),
    if (ob.dns1): print "'%s'" % (ob.dns1),
    if (ob.dns2): print ",'%s'" % (ob.dns2),
    if (ob.dns3): print ",'%s'" % (ob.dns3),
  
    print ""
    
    
for i,ob in enumerate(nats.list()):
  if options.dumpapaplus:
    print ob
  else:
    if ob.enabled == False: continue
  
    print "nat ifIn '%s' ifOut '%s'" % (ifs.getByIfNumber(ob.in_iface).name if (ob.in_iface != "-1") else "Any",ifs.getByIfNumber(ob.out_iface).name if (ob.out_iface != "-1") else "Any"),
    print "%s" % (ob.in_iface), 
    print "from '%s'" % (ob.src_orig if (ob.src_orig) else "Any"),
    print "to '%s'" % (ob.dst_orig if (ob.dst_orig) else "Any"),
    print "becomes from '%s'" % (ob.src_nat if (ob.src_nat) else "Original"),
    print "to '%s'" % (ob.dst_nat if (ob.dst_nat) else "Original"),
    print ""
