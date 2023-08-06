from oarepo_references.api import HandlerKey
from oarepo_references.proxies import current_references
from .utils import TestRecord, create_record, TaxonomyRecord


def test_no_reference_config_not_modified_when_moved(app, db, test_es):
    ta = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    tr = create_record(TestRecord, {
        'tax': ta.canonical_url
    })
    tr.commit()
    db.session.commit()
    ta = TestRecord.get_record(ta.id)
    current_references.moved(
        'record',
        'TaxonomyRecord',
        object_url=ta.canonical_url,
        new_url=ta.canonical_url + '/new'
    )
    db.session.commit()
    tr = TestRecord.get_record(tr.id)
    assert tr['tax'] == ta.canonical_url


def test_no_reference_config_not_modified_when_moved_bulk(app, db, test_es):
    ta = create_record(TaxonomyRecord, {
        'title': 'aaa'
    })
    tr = create_record(TestRecord, {
        'tax': ta.canonical_url
    })
    tr.commit()
    db.session.commit()
    ta = TestRecord.get_record(ta.id)
    with current_references.bulk():
        current_references.moved(
            'record',
            'TaxonomyRecord',
            object_url=ta.canonical_url,
            new_url=ta.canonical_url + '/new'
        )
    db.session.commit()
    tr = TestRecord.get_record(tr.id)
    assert tr['tax'] == ta.canonical_url


def test_default_handler(app):
    assert current_references.handlers == {
        HandlerKey(
            type='inline',
            referencing_type='record',
            referencing_subtype=None,
            referenced_type=None,
            referenced_subtype=None
        ): {
            'handler': 'oarepo_references.record.RecordInlineReferenceHandler',
            'referencing': {'type': 'record'},
            'type': 'inline'
        },
        HandlerKey(
            type='reference',
            referencing_type='record',
            referencing_subtype=None,
            referenced_type=None,
            referenced_subtype=None
        ): {
            'handler': 'oarepo_references.record.RecordReferenceHandler',
            'referencing': {'type': 'record'},
            'type': 'reference'}
    }
