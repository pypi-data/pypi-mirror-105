import threading
from collections import defaultdict

from invenio_base.utils import obj_or_import_string

from oarepo_references.signals import before_references_update, after_references_updated


class ReferenceThreadLocalContext(threading.local):
    bulk_operation = False
    updated_objects = defaultdict(list)
    removed_objects = defaultdict(list)
    moved_objects = defaultdict(list)

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.updated_objects.clear()
        self.removed_objects.clear()
        self.moved_objects.clear()

    def start_bulk(self):
        self.initialize()
        self.bulk_operation = True

    def finish_bulk(self):
        self.perform_changes()
        self.bulk_operation = False

    def object_updated(self, cfg, kwargs):
        self.updated_objects[cfg['handler']].append({**cfg, **kwargs})
        assert self.updated_objects
        if not self.bulk_operation:
            self.perform_changes()

    def object_removed(self, cfg, kwargs):
        self.removed_objects[cfg['handler']].append({**cfg, **kwargs})
        assert self.removed_objects
        if not self.bulk_operation:
            self.perform_changes()

    def object_moved(self, cfg, kwargs):
        self.moved_objects[cfg['handler']].append({**cfg, **kwargs})
        assert self.moved_objects
        if not self.bulk_operation:
            self.perform_changes()

    def perform_changes(self):
        before_references_update.send(
            self,
            updated_objects=self.updated_objects,
            removed_objects=self.removed_objects,
            moved_objects=self.moved_objects)
        modified = True
        all_updated = {}
        all_removed = {}
        all_moved = {}
        while modified:
            modified = False
            if self.updated_objects:
                objs = {k: list(v) for k, v in self.updated_objects.items()}
                all_updated.update(objs)
                self.updated_objects.clear()
                modified = True
                for handler, parameters in objs.items():
                    obj_or_import_string(handler)().updated(parameters)
            if self.moved_objects:
                objs = {k: list(v) for k, v in self.moved_objects.items()}
                all_moved.update(objs)
                self.moved_objects.clear()
                modified = True
                for handler, parameters in objs.items():
                    obj_or_import_string(handler)().moved(parameters)
            if self.removed_objects:
                objs = {k: list(v) for k, v in self.removed_objects.items()}
                all_removed.update(objs)
                self.removed_objects.clear()
                modified = True
                for handler, parameters in objs.items():
                    obj_or_import_string(handler)().removed(parameters)
        after_references_updated.send(
            self,
            updated_objects=all_updated,
            removed_objects=all_removed,
            moved_objects=all_moved)


reference_thread_local_context = ReferenceThreadLocalContext()
