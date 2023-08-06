from oarepo_references.path_utils import find_path


def test_simple_path():
    d = {'a': 1}
    found = list(find_path(d, 'a'))
    assert found == [
        (d, 'a', 1)
    ]


def test_nested():
    d = {
        'a': {
            'b': 1
        }
    }
    found = list(find_path(d, 'a.b'))
    assert found == [
        (d['a'], 'b', 1)
    ]


def test_leaf_array():
    d = {'a': [1, 2]}
    found = list(find_path(d, 'a'))
    assert found == [
        (d['a'], 1, 2),
        (d['a'], 0, 1)
    ]


def test_nested_array():
    d = {
        'a': [
            {
                'b': 1
            },
            {
                'b': 2
            }
        ]
    }
    found = list(find_path(d, 'a.b'))
    assert found == [
        (d['a'][1], 'b', 2),
        (d['a'][0], 'b', 1)
    ]


def test_colon_in_array():
    d = {
        'a': [
            {
                'b': 1
            },
            {
                'b': 2
            }
        ]
    }
    found = list(find_path(d, 'a#b'))
    assert found == [
        (d['a'], 1, 2),
        (d['a'], 0, 1)
    ]


def test_colon():
    d = {
        'a': {
            'b': {
                'c': 1
            }
        }
    }
    found = list(find_path(d, 'a.b#c'))
    assert found == [
        (d['a'], 'b', 1)
    ]


def test_colon_array():
    d = {
        'a': {
            'b': [
                {
                    'c': 1
                },
                {
                    'c': 2
                }
            ]
        }
    }
    found = list(find_path(d, 'a.b#c'))
    assert found == [
        (d['a']['b'], 1, 2),
        (d['a']['b'], 0, 1),
    ]
