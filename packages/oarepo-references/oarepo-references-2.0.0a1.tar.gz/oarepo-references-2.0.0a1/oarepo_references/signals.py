# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Miroslav Bauer, CESNET.
#
# oarepo-references is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module for tracking and updating references in Invenio records."""

from __future__ import absolute_import, print_function

import traceback

from blinker import Namespace
from invenio_records.signals import after_record_delete, after_record_update

from .proxies import current_references

_signals = Namespace()

before_references_update = _signals.signal('before-references-object_updated')
"""Signal sent before references are updated.
"""

after_references_updated = _signals.signal('after-reference-object_updated')
"""Signal sent after references were updated.
"""


@after_record_update.connect
def update_references_record(sender, record, *args, **kwargs):
    """A signal receiver that updates references records on record object_updated."""
    try:
        if hasattr(record, 'canonical_url'):
            for mro in type(record).mro():
                current_references.updated(
                    type='inline',
                    referenced_type='record',
                    referenced_subtype=mro.__name__,
                    record=record,
                    object_url=record.canonical_url,
                    object_json={
                        'links': {
                            'self': record.canonical_url
                        },
                        'metadata': dict(record),
                    },
                    **kwargs
                )
    except:
        traceback.print_exc()
        raise


@after_record_delete.connect
def delete_references_record(sender, record, *args, **kwargs):
    """A signal receiver that updates references records on record object_updated."""
    try:
        if hasattr(record, 'canonical_url'):
            for mro in type(record).mro():
                current_references.removed(
                    type='inline',
                    referenced_type='record',
                    referenced_subtype=mro.__name__,
                    record=record,
                    object_url=record.canonical_url,
                    **kwargs
                )
    except:
        traceback.print_exc()
        raise
