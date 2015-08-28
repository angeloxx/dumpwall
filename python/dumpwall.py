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
        'iface_phys_type_':'ifacetype', 'iface_portshield_to_': 'portshieldwith'
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

        
ifs = Interfaces()

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
  
  if ifs.parse(key,value):
    continue
  
for i,ifn in enumerate(ifs.list()):
  #print "%-2s | %-15s | %-10s" % (ifn.id,ifn.name,ifn.ipaddress)
  if options.dumpapaplus:
    print ifn
  else:
    print "interface id '%s' name '%s' type '%s'" % (ifn.id,ifn.name,ifn.ifacetype),
    if (int(ifn.vlanid) > 0):
      print "vlan '%s'" % (ifn.vlanid),
    
    if (int(ifn.portshieldwith) > -1):
      print "portshield with '%s'" % (ifs.getById(ifn.portshieldwith).name),
  
    print ""