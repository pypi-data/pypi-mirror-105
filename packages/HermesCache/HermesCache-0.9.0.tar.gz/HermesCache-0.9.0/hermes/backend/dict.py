import heapq
import threading
import time
from typing import Any, Dict, Iterable, Optional, Union

from . import AbstractBackend, AbstractLock


__all__ = 'Lock', 'Backend'


class Lock(AbstractLock):
  '''Key-unaware reentrant thread lock.'''

  _lock: threading.RLock
  '''Threading lock instance.'''

  def __init__(self, key = None):
    self._lock = threading.RLock()

  def acquire(self, wait = True):
    '''Acquire the ``RLock``.'''

    return self._lock.acquire(wait)

  def release(self):
    '''Release the ``RLock``.'''

    self._lock.release()


class BaseBackend(AbstractBackend):
  '''Base dictionary backend without key expiration.'''

  cache: dict
  '''A ``dict`` used to store cache entries.'''

  _lock: Lock
  '''Lock instance.'''

  def __init__(self, mangler):
    super().__init__(mangler)

    self.cache = {}
    self._lock = Lock()

  def lock(self, key) -> Lock:
    return self._lock

  def save(self, key: str = None, value = None, *, mapping: dict = None, ttl: int = None):
    if not mapping:
      mapping = {key: value}

    self.cache.update({k: self.mangler.dumps(v) for k, v in mapping.items()})

  def load(self, keys: Union[str, Iterable[str]]) -> Optional[Union[Any, Dict[str, Any]]]:
    if isinstance(keys, str):
      value = self.cache.get(keys, None)
      if value is not None:
        value = self.mangler.loads(value)
      return value
    else:
      return {k: self.mangler.loads(self.cache[k]) for k in keys if k in self.cache}

  def remove(self, keys: Union[str, Iterable[str]]):
    if isinstance(keys, str):
      keys = (keys,)

    for key in keys:
      self.cache.pop(key, None)

  def clean(self):
    self.cache.clear()

  def dump(self) -> Dict[str, Any]:
    '''Dump the cache entries.'''

    return {k: self.mangler.loads(v) for k, v in self.cache.items()}


class Backend(BaseBackend):
  '''
  Dictionary test purpose backend implementation.

  Single process in-memory cache without memory limit, but with
  expiration. Besides testing, it may be suitable for limited number of
  real-world cases with a small cache size.
  '''

  _ttlHeap: list
  '''TTL heap used by the thread to remove the expired entries.'''

  _ttlWatchThread: threading.Thread
  '''An instance of TTL watcher thread.'''

  _ttlWatchSleep: float
  '''Seconds for the expiration watcher to sleep in the loop.'''

  _ttlWatchThreadRunning = False
  '''Run flag of the while-loop of the thread.'''

  def __init__(self, mangler, *, ttlWatchSleep: float = 1):
    super().__init__(mangler)

    self._ttlHeap = []

    self._ttlWatchSleep = ttlWatchSleep
    self._ttlWatchThread = threading.Thread(target = self._watchExpiry, daemon = True)
    self._ttlWatchThreadRunning = True
    self._ttlWatchThread.start()

  def save(self, key: str = None, value = None, *, mapping: dict = None, ttl: int = None):
    super().save(key, value, mapping = mapping, ttl = ttl)

    if ttl:
      for k in mapping or (key,):
        heapq.heappush(self._ttlHeap, (time.time() + ttl, k))

  def clean(self):
    # It touches the heap and needs to be synchronised
    with self._lock:
      super().clean()
      self._ttlHeap.clear()

  def stop(self):
    '''Ask TTL watch thread to stop and join it.'''

    self._ttlWatchThreadRunning = False
    self._ttlWatchThread.join(2 * self._ttlWatchSleep)

  def dump(self) -> Dict[str, Any]:
    # It iterates the cache and needs to be synchronised
    with self._lock:
      return super().dump()

  def _watchExpiry(self):
    while self._ttlWatchThreadRunning:
      with self._lock:
        # May contain manually invalidated keys
        expiredKeys = []
        while self._ttlHeap and self._ttlHeap[0][0] < time.time():
          _, key = heapq.heappop(self._ttlHeap)
          expiredKeys.append(key)
        self.remove(expiredKeys)

      time.sleep(self._ttlWatchSleep)
