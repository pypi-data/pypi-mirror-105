# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Miroslav Bauer, CESNET.
#
# oarepo-references is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test utility functions."""
from uuid import uuid4

from flask import url_for
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.minters import recid_minter
from invenio_records import Record

from tests.constants import TEST_INDEX


class TestRecord(Record):

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.recid_item',
                       pid_value=self['pid'], _external=True)


class TaxonomyRecord(Record):

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.recid_item',
                       pid_value=self['pid'], _external=True)


def create_record(cls, data, refresh=True):
    u = uuid4()
    pid = recid_minter(u, data)
    data['pid'] = pid.pid_value
    rec = cls.create(data, _id=u)
    RecordIndexer().index(rec, refresh=refresh)
    # strange - it seems that refresh above does not work
    if refresh:
        RecordIndexer().client.indices.refresh()
    return rec


def test_record_to_index(*args, **kwargs):
    return TEST_INDEX, '_doc'
