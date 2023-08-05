from __future__ import absolute_import
from collections import OrderedDict

ENCODERS = OrderedDict()

try:
  import msgpack

  ENCODERS['msgpack'] = msgpack
except ImportError:
  pass

try:
  import json

  ENCODERS['json'] = json
except ImportError:
  pass

try:
  import erlpack

  class _erlpack:
    dumps = erlpack.pack
    loads = erlpack.unpack
  
  ENCODERS['erlpack'] = _erlpack
except ImportError:
  pass
