import traceback
from collections import defaultdict
import re

import sqlalchemy.orm
from elasticsearch.helpers import bulk
from elasticsearch_dsl.query import Bool, Nested, Terms
from invenio_base.utils import obj_or_import_string
from invenio_indexer.api import RecordIndexer
from invenio_search import RecordsSearch

from .api import ReferenceHandler
from .path_utils import find_path


class BaseRecordHandler(ReferenceHandler):

    def process(self, args, new_value_function):
        to_index = []
        indices = set()
        for record, matched_paths in self.filter_records(args):
            try:
                modified = False
                for path, record_args in matched_paths.items():
                    if self.patch_path(record, path, record_args, new_value_function):
                        modified = True
                if modified:
                    record.commit()

                    indexer = obj_or_import_string(
                        get_common_referencing_value(
                            matches_to_configs(matched_paths),
                            'record_indexer', RecordIndexer,
                            transformer=obj_or_import_string))()

                    index_name = get_common_referencing_value(
                        matches_to_configs(matched_paths), 'index_name')
                    data = indexer._prepare_record(record, index_name, '_doc')
                    index_name, _ = indexer._prepare_index(index_name, '_doc')
                    indices.add(index_name)
                    to_index.append({
                        '_index': index_name,
                        '_type': '_doc',
                        '_id': str(record.id),
                        '_source': data
                    })
                    if len(to_index) >= 100:
                        bulk(RecordIndexer().client, to_index)
                        to_index = []
            except:
                traceback.print_exc()
                raise

        if to_index:
            bulk(RecordIndexer().client, to_index)

        if indices:
            RecordIndexer().client.indices.refresh(index=','.join(indices))

    def filter_records(self, args):
        by_index = defaultdict(list)
        for arg in args:
            by_index[arg['referencing']['index_name']].append(arg)

        for idx, index_args in by_index.items():
            q = []
            values_by_paths = defaultdict(list)
            for argidx, arg in enumerate(index_args):
                url = arg['object_url']
                for pidx, path in enumerate(arg['referencing']['paths']):
                    values_by_paths[path].append(
                        (
                            url, argidx, pidx
                        )
                    )

            for path, vals in values_by_paths.items():
                q.append(make_terms_query(path, [v[0] for v in vals], path))

            indexer = obj_or_import_string(
                get_common_referencing_value(
                    index_args, 'record_indexer', RecordIndexer,
                    transformer=obj_or_import_string))()

            index_name, _ = indexer._prepare_index(idx, '_doc')

            RecordIndexer().client.indices.refresh(index=index_name)

            # TODO: replace scan with PIT (point-in-time)
            for rec in RecordsSearch(index=index_name).source('_id').query(
                Bool(should=q, minimum_should_match=1)
            ).scan():
                matches = {}
                for path in rec.meta.matched_queries:
                    by_path = {}
                    for val in values_by_paths[path]:
                        by_path[val[0]] = index_args[val[1]]
                    matches[path] = by_path
                record_class = get_common_referencing_value(
                    matches_to_configs(matches), 'record_class',
                    transformer=obj_or_import_string)
                try:
                    record = record_class.get_record(rec.meta.id, with_deleted=False)
                except sqlalchemy.orm.exc.NoResultFound:
                    continue

                yield record, matches

    def patch_path(self, d, path, record_args, new_value_function):
        modified = False
        for parent, prop, extracted_url in find_path(d, path):

            if extracted_url in record_args:
                value = new_value_function(record_args[extracted_url])
                if value is not None:
                    if value != parent[prop]:
                        parent[prop] = value
                        modified = True
                else:
                    del parent[prop]
                    modified = True
        return modified


class RecordReferenceHandler(BaseRecordHandler):

    def moved(self, args):
        self.process(args, new_value_function=lambda x: x['new_url'])

    def removed(self, args):
        self.process(args, new_value_function=lambda x: None)

    def updated(self, args):
        # reference not changed when record is updated, so do nothing
        pass


class RecordInlineReferenceHandler(BaseRecordHandler):

    def record_transformer(self, record_args):
        transformer = record_args.get('referenced', '').get('reference_transformer')
        if transformer:
            return obj_or_import_string(transformer)(record_args)
        else:
            return record_args['object_json']

    def moved(self, args):
        self.process(args, new_value_function=lambda x: self.record_transformer(x))

    def removed(self, args):
        self.process(args, new_value_function=lambda x: None)

    def updated(self, args):
        self.process(args, new_value_function=lambda x: self.record_transformer(x))


def matches_to_configs(matches):
    return [
        y for x in matches.values() for y in x.values()
    ]


def get_common_referencing_value(matches, field_name, default=None, transformer=lambda x: x):
    values = set(
        transformer(
            m['referencing'].get(field_name)
        ) for m in matches
    )
    if None in values:
        values.remove(None)

    if len(values) > 1:
        raise ValueError(f'Configuration error: multiple values of {field_name} in {matches}')
    if not values:
        if not default:
            raise ValueError(f'Configuration error: no values of {field_name} in {matches}')
        else:
            return default
    return next(iter(values))


def make_terms_query(path, values, name, prefix='', set_name=True):
    path = path.replace(']', '').replace(':', '.').replace('#', '.')
    path = path.split('[', maxsplit=1)
    path = [x.strip('.') for x in path]  # sequence n[#x]
    if len(path) > 1:
        # generate nested
        if set_name:
            return Nested(path=prefix + path[0], _name=name, query=Bool(
                must=[make_terms_query(path[1], values, name, path[0] + '.', set_name=False)]
            ))
        else:
            return Nested(path=prefix + path[0], query=Bool(
                must=[make_terms_query(path[1], values, name, path[0] + '.', set_name=False)]
            ))
    else:
        # generate terms
        if set_name:
            return Terms(**{prefix + path[0]: values, '_name': name})
        else:
            return Terms(**{prefix + path[0]: values})
