def find_path(d, path):
    path = path.split(':')[0]  # discard path after ':' - that is for ES only
    path = path.replace('[', '.').replace(']', '').strip().strip('.')
    path = path.split('#')  # split on '#'
    path = [x.strip('.') for x in path]
    for parent, prop in iterate_path({'a': d}, 'a', path[0].split('.')):
        if len(path) == 1:
            yield parent, prop, parent[prop]
        else:
            for c, cprop in iterate_path({'a': parent[prop]}, 'a', path[1].split('.')):
                yield parent, prop, c[cprop]


def iterate_path(parent, propName, path):
    processed = False
    if isinstance(parent, dict) or isinstance(parent, (list, tuple)):
        record = parent[propName]
        if isinstance(record, (list, tuple)):
            # iterate in reversed order because of possible deletes in the code using the iterator
            for idx in list(reversed(range(len(record)))):
                yield from iterate_path(record, idx, path)
            processed = True
        elif path and path[0] in record:
            yield from iterate_path(record, path[0], path[1:])
            processed = True

    if not processed and not path:
        yield parent, propName
