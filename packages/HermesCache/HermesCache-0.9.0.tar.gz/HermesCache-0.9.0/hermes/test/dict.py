import threading
import time

import hermes.backend.dict

from .. import test


class TestDict(test.TestCase):

  def setUp(self):
    self.testee = hermes.Hermes(hermes.backend.dict.Backend, ttl = 360, ttlWatchSleep = 0.01)
    self.addCleanup(self.testee.backend.stop)

    self.fixture = test.createFixture(self.testee)

    self.testee.clean()

  def testSimple(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', b = 'beta'))
      self.assertEqual(1, self.fixture.calls)

      key = 'cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', b = 'beta')
      self.assertEqual({key: 'ateb+ahpla'}, self.testee.backend.dump())

    self.fixture.simple.invalidate('alpha', b = 'beta')
    self.assertEqual({}, self.testee.backend.dump())


    self.assertEqual(1,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    expected = "]}'ammag'{[+}]'ateb'[ :'ahpla'{"
    for _ in range(4):
      self.assertEqual(expected, self.fixture.simple({'alpha': ['beta']}, [{'gamma'}]))

      self.assertEqual(2, self.fixture.calls)
      key = 'cache:entry:hermes.test:Fixture:simple:{}'.format(
        self._arghash({'alpha': ['beta']}, [{'gamma'}]))
      self.assertEqual({key: expected}, self.testee.backend.dump())


    self.fixture.simple.invalidate({'alpha': ['beta']}, [{'gamma'}])
    self.assertEqual({}, self.testee.backend.dump())

  def testTagged(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', b = 'beta'))
      self.assertEqual(1,       self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(3, len(cache))
      self.assertEqual(22, len(cache.pop('cache:tag:rock')))
      self.assertEqual(22, len(cache.pop('cache:tag:tree')))

      expected = 'cache:entry:hermes.test:Fixture:tagged:' + self._arghash('alpha', b = 'beta')
      self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual('ae-hl', tuple(cache.values())[0])


    self.fixture.tagged.invalidate('alpha', b = 'beta')

    cache = self.testee.backend.dump()
    self.assertEqual(2, len(cache))
    rockTag = cache.get('cache:tag:rock')
    treeTag = cache.get('cache:tag:tree')
    self.assertNotEqual(rockTag, treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(3, self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(5, len(cache))
      self.assertEqual(rockTag, cache.get('cache:tag:rock'))
      self.assertEqual(treeTag, cache.get('cache:tag:tree'))
      self.assertEqual(22, len(cache.get('cache:tag:ice')))

    self.testee.clean(['rock'])

    cache = self.testee.backend.dump()
    self.assertEqual(4, len(cache))
    self.assertTrue('cache:tag:rock' not in cache)
    iceTag = cache.get('cache:tag:ice')

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(5, self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(7,  len(cache), 'has new and old entries for tagged and tagged 2 + 3 tags')
      self.assertEqual(treeTag, cache.get('cache:tag:tree'))
      self.assertEqual(iceTag,  cache.get('cache:tag:ice'))
      self.assertEqual(22, len(cache.get('cache:tag:rock')))
      self.assertNotEqual(rockTag, cache.get('cache:tag:rock'))

  def testFunction(self):
    counter = dict(foo = 0, bar = 0)

    @self.testee
    def foo(a, b):
      counter['foo'] += 1
      return '{0}+{1}'.format(a, b)[::-1]

    key = lambda _fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    def bar(a, b):
      counter['bar'] += 1
      return '{0}-{1}'.format(a, b)[::2]


    self.assertEqual(0,  counter['foo'])
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('ateb+ahpla', foo('alpha', 'beta'))
      self.assertEqual(1, counter['foo'])
      self.assertEqual(
        {'cache:entry:hermes.test.dict:foo:' + self._arghash('alpha', 'beta'): 'ateb+ahpla'},
        self.testee.backend.dump()
      )

    foo.invalidate('alpha', 'beta')
    self.assertEqual(1,  counter['foo'])
    self.assertEqual({}, self.testee.backend.dump())


    self.assertEqual(0,  counter['bar'])
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('apabt', bar('alpha', 'beta'))
      self.assertEqual(1,       counter['bar'])

      cache = self.testee.backend.dump()
      self.assertEqual(3,  len(cache))
      self.assertEqual(22, len(cache.pop('cache:tag:a')))
      self.assertEqual(22, len(cache.pop('cache:tag:z')))

      expected = 'mk:alpha:beta'
      self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual('apabt', tuple(cache.values())[0])

    bar.invalidate('alpha', 'beta')
    self.assertEqual(1, counter['foo'])

    cache = self.testee.backend.dump()
    self.assertEqual(2,  len(cache))
    self.assertEqual(22, len(cache.pop('cache:tag:a')))
    self.assertEqual(22, len(cache.pop('cache:tag:z')))

  def testKey(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('apabt', self.fixture.key('alpha', 'beta'))
      self.assertEqual(1,       self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(3,  len(cache))
      self.assertEqual(22, len(cache.pop('cache:tag:ash')))
      self.assertEqual(22, len(cache.pop('cache:tag:stone')))

      expected = 'mykey:alpha:beta'
      self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual('apabt', tuple(cache.values())[0])

    self.fixture.key.invalidate('alpha', 'beta')

    cache = self.testee.backend.dump()
    self.assertEqual(2,  len(cache))
    self.assertEqual(22, len(cache.pop('cache:tag:ash')))
    self.assertEqual(22, len(cache.pop('cache:tag:stone')))

  def testAll(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual({'a': 1, 'b': {'b': 'beta'}}, self.fixture.all({'alpha': 1}, ['beta']))
      self.assertEqual(1, self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(3, len(cache))
      self.assertEqual(22, len(cache.pop('cache:tag:a')))
      self.assertEqual(22, len(cache.pop('cache:tag:z')))

      expected = "mk:{'alpha':1}:['beta']"
      self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual({'a': 1, 'b': {'b': 'beta'}}, tuple(cache.values())[0])

    self.fixture.all.invalidate({'alpha': 1}, ['beta'])

    cache = self.testee.backend.dump()
    self.assertEqual(2,  len(cache))
    self.assertEqual(22, len(cache.pop('cache:tag:a')))
    self.assertEqual(22, len(cache.pop('cache:tag:z')))

  def testClean(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    self.testee.clean()

    self.assertEqual(2,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

  def testCleanTagged(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    cache = self.testee.backend.dump()
    self.assertEqual(4, len(cache))

    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', 'beta')
      ),
    )
    self.assertEqual(22, len(cache.pop('cache:tag:rock')))
    self.assertEqual(22, len(cache.pop('cache:tag:tree')))

    expectedKey = 'cache:entry:hermes.test:Fixture:tagged:' + self._arghash('gamma', 'delta')
    self.assertEqual(expectedKey, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.testee.clean(('rock',))

    cache = self.testee.backend.dump()
    self.assertEqual(3, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop('cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', 'beta')))
    self.assertEqual(22, len(cache.pop('cache:tag:tree')))
    self.assertFalse('cache:tag:rock' in cache)

    expectedKey = 'cache:entry:hermes.test:Fixture:tagged:' + self._arghash('gamma', 'delta')
    self.assertEqual(expectedKey, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(3,            self.fixture.calls)

    cache = self.testee.backend.dump()
    self.assertEqual(5, len(cache), '+1 old tagged entry')
    self.assertEqual(
      'ateb+ahpla',
      cache.pop('cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', 'beta')))
    self.assertEqual(22, len(cache.pop('cache:tag:rock')))
    self.assertEqual(22, len(cache.pop('cache:tag:tree')))

    expectedKey = 'cache:entry:hermes.test:Fixture:tagged:' + self._arghash('gamma', 'delta')
    self.assertEqual(expectedKey, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.testee.clean(('rock', 'tree'))

    cache = self.testee.backend.dump()
    self.assertEqual(3, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop('cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', 'beta')))
    self.assertFalse('cache:tag:tree' in cache)
    self.assertFalse('cache:tag:rock' in cache)

    expectedKey = 'cache:entry:hermes.test:Fixture:tagged:' + self._arghash('gamma', 'delta')
    self.assertEqual(expectedKey, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(4,            self.fixture.calls)

    cache = self.testee.backend.dump()
    self.assertEqual(6, len(cache), '+2 old tagged entries')
    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', 'beta')
      ),
    )
    expectedKey = 'cache:entry:hermes.test:Fixture:tagged:' + self._arghash('gamma', 'delta')
    self.assertTrue(expectedKey in (':'.join(k.split(':')[:-1]) for k in cache.keys()))
    self.assertTrue('aldamg' in cache.values())


    self.testee.clean()

    self.assertEqual(4,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

  def testNested(self):
    self.assertEqual('beta+alpha', self.fixture.nested('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)
    self.assertEqual({
      'cache:entry:hermes.test:Fixture:nested:' + self._arghash('alpha', 'beta'): 'beta+alpha',
      'cache:entry:hermes.test:Fixture:simple:' + self._arghash('beta', 'alpha'): 'ahpla+ateb'
    }, self.testee.backend.dump())

  def testConcurrent(self):
    log = []
    key = lambda _fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    def bar(a, b):
      log.append(1)
      time.sleep(0.04)
      return '{0}-{1}'.format(a, b)[::2]

    threads = [threading.Thread(target = bar, args = ('alpha', 'beta')) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertEqual(1, sum(log))

    cache = self.testee.backend.dump()
    self.assertEqual(22, len(cache.pop('cache:tag:a')))
    self.assertEqual(22, len(cache.pop('cache:tag:z')))

    self.assertEqual('mk:alpha:beta', ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('apabt', tuple(cache.values())[0])

    del log[:]
    self.testee.clean()
    self.testee.backend.lock = lambda k: hermes.backend.AbstractLock(k)  # now see a dogpile

    threads = [threading.Thread(target = bar, args = ('alpha', 'beta')) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertGreater(sum(log), 1, 'dogpile')

    cache = self.testee.backend.dump()
    self.assertEqual(22, len(cache.pop('cache:tag:a')))
    self.assertEqual(22, len(cache.pop('cache:tag:z')))

    self.assertEqual('mk:alpha:beta', ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('apabt', tuple(cache.values())[0])

  def testExpiration(self):
    self.assertEqual({}, self.testee.backend.dump())

    @self.testee(ttl = 0.05)
    def fn1(a, b):
      return '{0}-{1}'.format(a, b)[::2]

    @self.testee(ttl = 0.2)
    def fn2(a, b):
      return '{0}-{1}'.format(a, b)[::2]

    fn1('alpha', b = 'beta')
    fn2('alpha', b = 'beta')

    key1 = 'cache:entry:hermes.test.dict:fn1:' + self._arghash('alpha', b = 'beta')
    key2 = 'cache:entry:hermes.test.dict:fn2:' + self._arghash('alpha', b = 'beta')
    self.assertIn(key1, self.testee.backend.dump())
    self.assertIn(key2, self.testee.backend.dump())

    time.sleep(0.1)
    self.assertNotIn(key1, self.testee.backend.dump())
    self.assertIn(key2, self.testee.backend.dump())


class TestDictLock(test.TestCase):

  def setUp(self):
    self.testee = hermes.backend.dict.Lock('123')

  def testAcquire(self):
    for _ in range(2):
      try:
        self.assertTrue(self.testee.acquire(True))
        self.assertTrue(self.testee.acquire(False))  # reentrant within one thread
      finally:
        self.testee.release()

  def testRelease(self):
    for _ in range(2):
      try:
        self.assertTrue(self.testee.acquire(True))
        self.assertTrue(self.testee.acquire(False))  # reentrant within one thread
      finally:
        self.testee.release()

  def testWith(self):
    with self.testee:
      self.assertTrue(self.testee.acquire(False))  # reentrant within one thread

  def testConcurrent(self):
    log   = []
    check = threading.Lock()

    def target():
      with self.testee:
        log.append(check.acquire(False))
        time.sleep(0.05)
        check.release()
        time.sleep(0.05)

    threads = [threading.Thread(target = target) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertEqual([True] * 4, log)
