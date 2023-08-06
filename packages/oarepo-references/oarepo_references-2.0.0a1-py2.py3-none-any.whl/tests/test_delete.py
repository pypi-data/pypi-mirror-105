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


def test_delete(app, db, test_es):
    current_references.flush_caches()
    current_references._load_dependency({
        'type': 'reference',
        'referencing': {
            'type': 'record',
            'subtype': 'TestRecord',
            'record_class': 'tests.utils.TestRecord',
            'record_indexer': None,
            'index_name': TEST_INDEX,
            'paths': [
                'tax:keyword'
            ],
        },
        'referenced': {
            'type': 'record',
            'subtype': 'TaxonomyRecord',
            'record_class': 'tests.utils.TaxonomyRecord',
        },
    }, current_references.dependencies)

    ta = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    tr = create_record(TestRecord, {
        'tax': ta.canonical_url
    })
    tr.commit()
    db.session.commit()
    db.session.expire_all()

    ta = TaxonomyRecord.get_record(ta.id)

    current_references.removed(
        'record',
        'TaxonomyRecord',
        object_url=ta.canonical_url,
    )

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert 'tax' not in tr


def test_delete_inlined(app, db, test_es):
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
                'tax#links.self:keyword'
            ],
        },
        'referenced': {
            'type': 'record',
            'subtype': 'TaxonomyRecord',
            'record_class': 'tests.utils.TaxonomyRecord',
        },
    }, current_references.dependencies)

    ta = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    tr = create_record(TestRecord, {
        'tax': {
            'links': {
                'self': ta.canonical_url
            },
            'metadata': {
                'title': 'aaa'
            }
        }
    })
    tr.commit()
    db.session.commit()
    db.session.expire_all()

    ta = TaxonomyRecord.get_record(ta.id)
    ta.delete()

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert 'tax' not in tr
