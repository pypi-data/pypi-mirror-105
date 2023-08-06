import inspect
import socket
import threading
import unittest


def load_tests(loader, tests, pattern):
  from . import abstract, dict, facade, memcached, redis  # noqa: F401

  suite = unittest.TestSuite()
  for m in filter(inspect.ismodule, locals().values()):
    suite.addTests(loader.loadTestsFromModule(m))

  return suite


class TestCase(unittest.TestCase):

  testee = None
  '''HermesCache object.'''

  fixture = None
  '''Object under test.'''

  def _arghash(self, *args, **kwargs):
    '''
    Not very neat as it penetrates into an implementation detail,
    though otherwise it'll be harder to make assertion on keys.
    '''

    arguments = args, tuple(sorted(kwargs.items()))
    return self.testee.mangler.hash(self.testee.mangler.dumps(arguments))


def createFixture(cache):

  class Fixture:

    calls = 0

    @cache
    def simple(self, a, b):
      '''Here be dragons... seriously just a docstring test.'''

      self.calls += 1
      return '{0}+{1}'.format(a, b)[::-1]

    @cache
    def nested(self, a, b):
      self.calls += 1
      return self.simple(b, a)[::-1]

    @cache(tags = ('rock', 'tree'))
    def tagged(self, a, b):
      self.calls += 1
      return '{0}-{1}'.format(a, b)[::-2]

    @cache(tags = ('rock', 'ice'))
    def tagged2(self, a, b):
      self.calls += 1
      return '{0}%{1}'.format(a, b)[::-2]

    @cache(tags = ('ash', 'stone'), key = lambda fn, a, b: f'mykey:{a}:{b}')
    def key(self, a, b):
      self.calls += 1
      return '{0}*{1}'.format(a, b)[::2]

    @cache(
      tags = ('a', 'z'),
      key = lambda fn, *a: 'mk:{0}:{1}'.format(*a).replace(' ', ''),
      ttl = 1200,
    )
    def all(self, a, b):
      self.calls += 1
      return {'a': a['alpha'], 'b': {'b': b[0]}}

  return Fixture()


class FakeBackendServer:

  port = None
  '''Fake server port.'''

  log = None
  '''Activity log.'''

  thread = None
  '''Server connection-accepting thread.'''

  closing = None
  '''Whether connection is closing.'''

  def __init__(self):
    self.log = []

  def serve(self):
    self.closing = False

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', 0))
    serverSocket.listen(1)

    self.port = serverSocket.getsockname()[1]

    self.thread = threading.Thread(target = self.target, args = (serverSocket,))
    self.thread.start()

  def close(self):
    self.closing = True

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.connect(('localhost', self.port))

    clientSock.close()

    self.thread.join()

  def target(self, serverSocket):
    clientSocket, _ = serverSocket.accept()

    if not self.closing:
      self.log.append('connected')

    try:
      chunk = clientSocket.recv(1024)
      if not self.closing:
        if not chunk:
          self.log.append('closed')
        else:
          self.log.append('received {}'.format(chunk))
    finally:
      clientSocket.close()
      serverSocket.close()
