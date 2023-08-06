from invenio_indexer.api import RecordIndexer

from oarepo_references.proxies import current_references
from .constants import TEST_INDEX
from .utils import TestRecord, create_record, TaxonomyRecord


# import logging
#
# es_trace_logger = logging.getLogger('elasticsearch.trace')
# es_trace_logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# es_trace_logger.addHandler(handler)


def test_update_nested(app, db, test_es):
    current_references.flush_caches()
    current_references._load_dependency({
        'type': 'inline',
        'referencing': {
            'type': 'record',
            'subtype': 'TestRecord',
            'record_class': 'tests.utils.TestRecord',
            'record_indexer': None,
            'index_name': TEST_INDEX,
            'paths': [
                'n[#url]'
            ],
        },
        'referenced': {
            'type': 'record',
            'subtype': 'TaxonomyRecord',
            'record_class': 'tests.utils.TaxonomyRecord',
            'reference_transformer': lambda x: {
                'title': x['object_json']['metadata']['title'],
                'url': x['object_json']['links']['self']
            }
        },
    }, current_references.dependencies)

    ta = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    tr = create_record(TestRecord, {
        'n': {
            'url': ta.canonical_url,
            'title': 'aaa'
        }
    })
    tr.commit()
    db.session.commit()
    db.session.expire_all()

    ta = TaxonomyRecord.get_record(ta.id)
    ta['title'] = 'bbb'
    ta.commit()

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert dict(tr) == {
        'n': {
            'title': 'bbb',
            'url': 'http://localhost/records/1'
        },
        'pid': tr['pid']
    }
