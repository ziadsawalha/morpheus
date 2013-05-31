import collections
import time

from morpheus import MorpheusDict
from morpheus.operations import as_of, is_required, is_type


class Foo(MorpheusDict):
    '''A MorpheusDict with complex rules and a migraiton entry'''
    __schema__ = dict(
        simple=int,

        status=basestring,
        state=as_of(0.7).is_replaced_by('status'),

        boolean=is_type(bool),
        chain=is_type(int),

        must=is_required()
    )


class Bar(dict):
    '''Simple subclass'''
    pass


class Woo(MorpheusDict):
    '''Just a list of allowed fields'''
    __schema__ = ['id', 'name', 'simple', 'state']


class MappingImpl(collections.MutableMapping):
    """An implementation of MutableMapping"""

    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        return self._data[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._data[self.__keytransform__(key)] = value

    def __delitem__(self, k):
        del self._data[k]

    def __keytransform__(self, key):
        return key

    def __repr__(self):
        return self._data.__repr__()

    def __dict__(self):
        return self._data


def test_simple_instantiation():
    '''Compare to dict for simple instantiation'''
    sample = {
        'simple': 1,
        'state': 'active',
        'boolean': True,
        'chain': 12,
        'must': 1,
    }
    count = range(1000)

    start = time.time()
    for _ in count:
        dict(sample)
    end = time.time()
    delta_dict = end - start

    start = time.time()
    for _ in count:
        MorpheusDict(sample)
    end = time.time()
    delta_morpheus = end - start

    hit = 100 * (delta_morpheus - delta_dict) / delta_dict
    print ("- Simple:   %s%% (from %s to %s)" % (hit,
           format(delta_dict, '0.000'), format(delta_morpheus, '0.000')))


def test_subclass_instantiation():
    '''Compare to a subclassed dict'''
    sample = {
        'simple': 1,
        'state': 'active',
        'boolean': True,
        'chain': 12,
        'must': 1,
    }
    count = range(1000)

    start = time.time()
    for _ in count:
        Bar(sample)
    end = time.time()
    delta_dict = end - start

    start = time.time()
    for _ in count:
        MorpheusDict(sample)
    end = time.time()
    delta_morpheus = end - start

    hit = 100 * (delta_morpheus - delta_dict) / delta_dict
    print ("- Subclass: %s%% (from %s to %s)" % (hit,
           format(delta_dict, '0.000'), format(delta_morpheus, '0.000')))


def test_complex_instantiation():
    '''Compare to dict and manual migration'''
    sample = {
        'simple': 1,
        'state': 'active',
        'boolean': True,
        'chain': 12,
        'must': 1,
    }
    count = range(1000)

    start = time.time()
    for _ in count:
        data = dict(sample)
        data['status'] = data.pop('state')
    end = time.time()
    delta_dict = end-start

    start = time.time()
    for _ in count:
        data = Foo(sample)
    end = time.time()
    delta_morpheus = end-start

    assert data['status'] == 'active'
    hit = 100 * (delta_morpheus - delta_dict) / delta_dict
    print ("- Complex:  %s%% (from %s to %s)" % (hit,
           format(delta_dict, '0.000'), format(delta_morpheus, '0.000')))


def test_list_instantiation():
    '''Compare to dict using simple list validation of fields'''
    sample = {
        'id': 1,
        'name': 'active',
        'simple': True,
        'state': 12,
    }
    count = range(1000)

    start = time.time()
    for _ in count:
        dict(sample)
    end = time.time()
    delta_dict = end-start

    start = time.time()
    for _ in count:
        Woo(sample)
    end = time.time()
    delta_morpheus = end-start

    hit = 100 * (delta_morpheus - delta_dict) / delta_dict
    print ("- List:     %s%% (from %s to %s)" % (hit,
           format(delta_dict, '0.000'), format(delta_morpheus, '0.000')))


def test_mapping_instantiation():
    '''Compare to mutable mapping for instantiation'''
    sample = {
        'simple': 1,
        'state': 'active',
        'boolean': True,
        'chain': 12,
        'must': 1,
    }
    count = range(1000)

    start = time.time()
    for _ in count:
        MappingImpl(sample)
    end = time.time()
    delta_dict = end - start

    start = time.time()
    for _ in count:
        MorpheusDict(sample)
    end = time.time()
    delta_morpheus = end - start

    hit = 100 * (delta_morpheus - delta_dict) / delta_dict
    print ("- Mapping:   %s%% (from %s to %s)" % (hit,
           format(delta_dict, '0.000'), format(delta_morpheus, '0.000')))


if __name__ == "__main__":
    print "Performance Hit:"
    test_simple_instantiation()
    test_subclass_instantiation()
    test_mapping_instantiation()
    test_list_instantiation()
    test_complex_instantiation()
