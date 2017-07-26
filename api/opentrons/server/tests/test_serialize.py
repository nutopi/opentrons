import json
import pytest

from collections import OrderedDict
from opentrons.server import serialize
from opentrons import robot, instruments, containers


@pytest.fixture
def instance():
    class A:
        def __init__(self, args):
            self.update(args)

        def update(self, args):
            for k, v in args.items():
                setattr(self, k, v)

        def __iter__(self):
            return iter([0])

    a1 = A({'b': 1, 'c': 'c', 'd': True, 'e': None})
    a2 = A({'a': 1})
    a3 = A({})

    root = A({
                'a': a1,
                'b': [a2, 'b', 1],
                'c': {'a': 1, 'b': [1, 2, a3]},
            })
    root.update({'circular': root})

    return (root, a1, a2, a3)


def test_robot():
    trough = containers.load('trough-12row', 'C1', 'trough')
    plate = containers.load('96-PCR-flat', 'D1', 'plate')

    # a tip rack for our pipette
    p200rack = containers.load('tiprack-200ul', 'B1', 'tiprack')

    # create a p200 pipette on robot axis B
    p200 = instruments.Pipette(
        name="p200",
        axis="b",
        min_volume=20,
        max_volume=200,
        tip_racks=[p200rack]
    )

    # Robot tree is pretty big and hard to verify
    # Making sure we can serialize it into json
    tree, refs = serialize.get_object_tree(robot)


def test_get_object_tree(instance):
    root, a1, a2, a3 = instance
    tree, refs = serialize.get_object_tree(root)

    assert refs == {id(o): o for o in [root, a1, a2, a3]}
    assert tree == {
        'i': id(root),
        'v': {
            '0': 0,
            'a': {
                'i': id(a1),
                'v': {
                    '0': 0,
                    'b': 1,
                    'c': 'c',
                    'd': True,
                    'e': None}},
            'b': [{'i': id(a2), 'v': {'0': 0, 'a': 1}}, 'b', 1],
            'c': {
                'i': tree['v']['c']['i'],
                'v': {
                    'a': 1,
                    'b': [1, 2, {'i': id(a3), 'v': {'0': 0}}]}},
            'circular': {'i': id(root), 'v': None}}}

    assert json.dumps(tree)


def test_get_object_tree_shallow(instance):
    root, *_ = instance
    tree, refs = serialize.get_object_tree(root, shallow=True)
    assert tree == {
        'i': id(root),
        'v': {
            '0': 0, 'a': {}, 'b': {}, 'c': {},
            'circular': {'i': id(root), 'v': None}}}
    assert refs == {id(root): root}


def test_ordered_dict():
    b = OrderedDict()
    b['b'] = 1
    a = {'a': b}
    tree, refs = serialize.get_object_tree(a)
    assert tree == {
        'i': id(a),
        'v': {'a': {
                'i': id(b),
                'v': {'b': 1}}}}
