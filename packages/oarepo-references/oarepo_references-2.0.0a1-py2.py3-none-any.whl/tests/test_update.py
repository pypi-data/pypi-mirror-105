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


def test_update(app, db, test_es):
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
    ta['title'] = 'bbb'
    ta.commit()

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert tr['tax']['metadata']['title'] == 'bbb'


def test_update_transformer(app, db, test_es):
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
                'tax#url:keyword'
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
        'tax': {
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
    assert tr['tax'] == {
        'title': 'bbb',
        'url': ta.canonical_url
    }


def test_update_multiple(app, db, test_es):
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
                'tax1#url:keyword',
                'tax2#url:keyword',
                'tax3#url:keyword',
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

    ta1 = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    ta2 = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    tr = create_record(TestRecord, {
        'tax1': {
            'url': ta1.canonical_url,
            'title': 'aaa'
        },
        'tax2': {
            'url': ta2.canonical_url,
            'title': 'aaa'
        },
        'tax3': {
            'url': ta2.canonical_url,
            'title': 'aaa'
        }
    })
    tr.commit()
    db.session.commit()
    db.session.expire_all()

    with current_references.bulk():
        ta1 = TaxonomyRecord.get_record(ta1.id)
        ta1['title'] = 'bbb'
        ta1.commit()

        ta2 = TaxonomyRecord.get_record(ta2.id)
        ta2['title'] = 'ccc'
        ta2.commit()

    db.session.commit()
    db.session.expire_all()

    tr = TestRecord.get_record(tr.id)
    assert tr['tax1'] == {
        'title': 'bbb',
        'url': ta1.canonical_url
    }
    assert tr['tax2'] == {
        'title': 'ccc',
        'url': ta2.canonical_url
    }
    assert tr['tax3'] == {
        'title': 'ccc',
        'url': ta2.canonical_url
    }


def test_update_many(app, db, test_es):
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
                'tax#url:keyword'
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
    trs = []
    for i in range(200):
        tr = create_record(TestRecord, {
            'tax': {
                'url': ta.canonical_url,
                'title': 'aaa'
            }
        }, refresh=False)
        tr.commit()
        trs.append(tr)
    RecordIndexer().client.indices.refresh()

    db.session.commit()
    db.session.expire_all()

    ta = TaxonomyRecord.get_record(ta.id)
    ta['title'] = 'bbb'
    ta.commit()

    db.session.commit()
    db.session.expire_all()

    for tr in trs:
        tr = TestRecord.get_record(tr.id)
        assert tr['tax'] == {
            'title': 'bbb',
            'url': ta.canonical_url
        }
