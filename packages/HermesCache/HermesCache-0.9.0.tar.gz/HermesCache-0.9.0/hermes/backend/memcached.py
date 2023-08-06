import threading
import time
from typing import Any, Dict, Iterable, Optional, Union

from . import AbstractBackend, AbstractLock


try:
  import pylibmc as memcache
except ImportError:
  import memcache


__all__ = 'Lock', 'Backend'


class Lock(AbstractLock):
  '''Key-aware distributed lock.'''

  client: memcache.Client
  '''Memcached client.'''

  timeout: int
  '''
  Maximum TTL of lock, can be up to 30 days, otherwise memcached will
  treated it as a UNIX timestamp of an exact date.
  '''

  sleep: float
  '''Amount of time to sleep per ``while True`` iteration when waiting.'''

  def __init__(self, key: str, client: memcache.Client, *, sleep: float = 0.1, timeout: int = 900):
    super().__init__(key)

    self.client  = client
    self.sleep   = sleep
    self.timeout = timeout

  def acquire(self, wait = True):
    while True:
      if self.client.add(self.key, 'locked', self.timeout):
        return True
      elif not wait:
        return False
      else:
        time.sleep(self.sleep)

  def release(self):
    self.client.delete(self.key)


class Backend(AbstractBackend):
  '''Memcached backend implementation.'''

  _local: threading.local
  '''Thread-local data.'''

  _options: dict
  '''Client options for deferred connection.'''

  _lockconf: dict
  '''Lock config.'''

  def __init__(
    self,
    mangler,
    *,
    servers: Iterable[str] = ('localhost:11211',),
    lockconf: dict = None,
    **kwargs
  ):
    self.mangler  = mangler
    self._options = dict(kwargs, servers = servers)
    self._local   = threading.local()

    self._lockconf = lockconf or {}

  @property
  def client(self) -> memcache.Client:
    '''Thread-mapped memcached client accessor'''

    if not hasattr(self._local, 'client'):
      self._local.client = memcache.Client(**self._options)

    return self._local.client

  def lock(self, key) -> Lock:
    return Lock(self.mangler.nameLock(key), self.client, **self._lockconf)

  def save(self, key: str = None, value = None, *, mapping: dict = None, ttl: int = None):
    if not mapping:
      mapping = {key: value}
    mapping = {k: self.mangler.dumps(v) for k, v in mapping.items()}

    self.client.set_multi(mapping, ttl if ttl is not None else 0)

  def load(self, keys: Union[str, Iterable[str]]) -> Optional[Union[Any, Dict[str, Any]]]:
    if isinstance(keys, str):
      value = self.client.get(keys)
      if value is not None:
        value = self.mangler.loads(value)
      return value
    else:
      # python3 pylibmc returns byte keys
      return {
        k.decode() if isinstance(k, bytes) else k: self.mangler.loads(v)
        for k, v in self.client.get_multi(tuple(keys)).items()
      }

  def remove(self, keys: Union[str, Iterable[str]]):
    if isinstance(keys, str):
      keys = (keys,)

    self.client.delete_multi(keys)

  def clean(self):
    self.client.flush_all()
