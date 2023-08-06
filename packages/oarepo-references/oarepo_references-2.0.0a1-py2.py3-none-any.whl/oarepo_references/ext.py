# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Miroslav Bauer, CESNET.
#
# oarepo-references is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module for tracking and updating references in Invenio records."""

from __future__ import absolute_import, print_function

from .api import RecordReferenceAPI
from . import config
from . import signals  # noqa


class _RecordReferencesState(RecordReferenceAPI):
    def __init__(self, app):
        super().__init__(app)


class OARepoReferences(object):
    """oarepo-references extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.init_config(app)
        self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        state = _RecordReferencesState(app)
        app.extensions['oarepo-references'] = state
        return state

    def init_config(self, app):
        """Initialize configuration.
        :param app: The Flask application.
        """
        for k in dir(config):
            if k.startswith('OAREPO_REFERENCES_'):
                app.config.setdefault(k, getattr(config, k))
