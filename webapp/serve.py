import os

from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

import redis


class NupicNamespace(BaseNamespace, BroadcastMixin):
  def recv_connect(self):
    def sendNupic():
      r = redis.Redis()

      ps_obj=r.pubsub()
      ps_obj.subscribe("nupic")

      for item in ps_obj.listen():
        self.emit('nupic_data', item)

    self.spawn(sendNupic)


class Application(object):
  def __init__(self):
    self.buffer = []

  def __call__(self, environ, start_response):
    path = environ['PATH_INFO'].strip('/') or 'index.html'

    if path.startswith('static/') or path == 'index.html':
      try:
        data = (open(path)
                .read()
                .replace("https://maps.googleapis.com/maps/api/js?key=API_KEY",
                         "https://maps.googleapis.com/maps/api/js?key=%s" % (
                            os.environ["API_KEY"])))

      except Exception:
        return not_found(start_response)

      if path.endswith(".js"):
        content_type = "text/javascript"
      elif path.endswith(".css"):
        content_type = "text/css"
      elif path.endswith(".swf"):
        content_type = "application/x-shockwave-flash"
      else:
        content_type = "text/html"

      start_response('200 OK', [('Content-Type', content_type)])
      return [data]

    if path.startswith("socket.io"):
      socketio_manage(environ, {'/nupic': NupicNamespace})
    else:
      return not_found(start_response)


def not_found(start_response):
  start_response('404 Not Found', [])
  return ['<h1>Not Found</h1>']


if __name__ == '__main__':
  print 'Listening on port http://0.0.0.0:8080 and on port 10843 (flash policy server)'
  SocketIOServer(('0.0.0.0', 8080),
                 Application(),
                 resource="socket.io",
                 policy_server=True,
                 policy_listener=('0.0.0.0', 10843)).serve_forever()
