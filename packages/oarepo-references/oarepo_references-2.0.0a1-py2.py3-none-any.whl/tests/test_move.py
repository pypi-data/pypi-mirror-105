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


def test_move(app, db, test_es):
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

    current_references.moved(
        'record',
        'TaxonomyRecord',
        object_url=ta.canonical_url,
        new_url=ta.canonical_url + '/new'
    )

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert tr['tax'] == ta.canonical_url + '/new'


def test_move_two_values(app, db, test_es):
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
                'tax3:keyword',
                'tax1:keyword',
                'tax2:keyword'
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
    ta1 = create_record(TaxonomyRecord, {
        'title': 'bbb'
    })
    tr = create_record(TestRecord, {
        'tax3': ta.canonical_url,
        'tax1': ta1.canonical_url,
        'tax2': ta.canonical_url
    })
    tr.commit()
    db.session.commit()
    db.session.expire_all()

    with current_references.bulk():
        current_references.moved(
            'record',
            'TaxonomyRecord',
            object_url=ta.canonical_url,
            new_url=ta.canonical_url + '/new'
        )
        current_references.moved(
            'record',
            'TaxonomyRecord',
            object_url=ta1.canonical_url,
            new_url=ta1.canonical_url + '/new'
        )

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert tr['tax3'] == ta.canonical_url + '/new'
    assert tr['tax1'] == ta1.canonical_url + '/new'
    assert tr['tax2'] == ta.canonical_url + '/new'


def test_move_referenced_many_times(app, db, test_es):
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
                'tax3:keyword',
                'tax1:keyword',
                'tax2:keyword'
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
    ta1 = create_record(TaxonomyRecord, {
        'title': 'bbb'
    })
    trs = []
    for i in range(200):
        tr = create_record(TestRecord, {
            'tax3': ta.canonical_url,
            'tax1': ta1.canonical_url,
            'tax2': ta.canonical_url,
            'title': f'record_{i}'
        }, refresh=False)
        tr.commit()
        trs.append(tr)
    RecordIndexer().client.indices.refresh()

    db.session.commit()
    db.session.expire_all()

    with current_references.bulk():
        current_references.moved(
            'record',
            'TaxonomyRecord',
            object_url=ta.canonical_url,
            new_url=ta.canonical_url + '/new'
        )
        current_references.moved(
            'record',
            'TaxonomyRecord',
            object_url=ta1.canonical_url,
            new_url=ta1.canonical_url + '/new'
        )

    db.session.commit()
    db.session.expire_all()

    for tr in trs:
        tr = TestRecord.get_record(tr.id)
        assert tr['tax3'] == ta.canonical_url + '/new'
        assert tr['tax1'] == ta1.canonical_url + '/new'
        assert tr['tax2'] == ta.canonical_url + '/new'


