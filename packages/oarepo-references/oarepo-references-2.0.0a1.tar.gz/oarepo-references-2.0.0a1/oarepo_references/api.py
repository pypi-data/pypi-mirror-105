import contextlib
from collections import namedtuple, defaultdict
from functools import cached_property

from .bulk import reference_thread_local_context


class ReferenceHandler:
    def moved(self, args):
        # args: array of moved objects
        raise NotImplemented()

    def removed(self, args):
        # args: array of removed objects
        raise NotImplemented()

    def updated(self, args):
        # args: array of updated objects
        raise NotImplemented()


HandlerKey = namedtuple('HandlerKey',
                        'type,'
                        'referencing_type, referencing_subtype, '
                        'referenced_type, referenced_subtype')


class RecordReferenceAPI:
    def __init__(self, app):
        self.app = app

    @cached_property
    def handlers(self):
        h = {}
        for cfg in self.app.config['OAREPO_REFERENCES_DEFAULT_DEPENDENCY_HANDLERS']:
            self._load_config(cfg, h)
        for cfg in self.app.config.get('OAREPO_REFERENCES_DEPENDENCY_HANDLERS', []):
            self._load_config(cfg, h)
        return h

    @cached_property
    def dependencies(self):
        h = {}
        for cfg in self.app.config.get('OAREPO_REFERENCES_DEPENDENCIES', []):
            self._load_dependency(cfg, h)
        return h

    def _load_dependency(self, cfg, h):
        """If using from your code, do not forget to flush_caches afterwards"""
        try:
            handler = next(
                self._get_handlers(
                    self.handlers,
                    type=cfg['type'],
                    referencing_type=cfg.get('referencing', {}).get('type', None),
                    referencing_subtype=cfg.get('referencing', {}).get('subtype', None),
                    referenced_type=cfg.get('referenced', {}).get('type', None),
                    referenced_subtype=cfg.get('referenced', {}).get('subtype', None),
                    raise_exception=False)
            )
            self._load_config({**handler, **cfg}, h)
        except StopIteration:
            self._load_config({**cfg}, h)

    @cached_property
    def dependencies_by_referenced(self):
        ret = defaultdict(list)
        for k, v in self.dependencies.items():
            ret[HandlerKey(
                type=k.type,
                referencing_type=None,
                referencing_subtype=None,
                referenced_type=k.referenced_type,
                referenced_subtype=k.referenced_subtype,
            )].append(v)
        return ret

    @staticmethod
    def _load_config(cfg, handlers):
        handler = cfg
        key = HandlerKey(
            type=cfg['type'],
            referencing_type=cfg.get('referencing', {}).get('type', None),
            referencing_subtype=cfg.get('referencing', {}).get('subtype', None),
            referenced_type=cfg.get('referenced', {}).get('type', None),
            referenced_subtype=cfg.get('referenced', {}).get('subtype', None),
        )
        handlers[key] = handler

    def set_handler(self, type, referencing_type, referencing_subtype,
                    referenced_type, referenced_subtype, **kwargs):
        self._load_config({
            'type': type,
            'referencing': {
                'type': referencing_type,
                'subtype': referencing_subtype,
            },
            'referenced': {
                'type': referenced_type,
                'subtype': referenced_subtype,
            },
            **kwargs
        }, self.handlers)

    @staticmethod
    def _get_handlers(handlers, type,
                      referencing_type, referencing_subtype,
                      referenced_type, referenced_subtype,
                      raise_exception=True):
        found = False
        for rt in (referencing_type, None):
            for tt in (referenced_type, None):
                for rs in (referencing_subtype, None):
                    for ts in (referenced_subtype, None):
                        h = handlers.get(
                            HandlerKey(
                                type=type,
                                referencing_type=rt,
                                referencing_subtype=rs,
                                referenced_type=tt,
                                referenced_subtype=ts,
                            )
                        )
                        if h:
                            found = True
                            yield h
        if not found:
            if raise_exception:
                raise AttributeError(
                    f'oarepo-references: Handler not found for '
                    f'referencing_type "{referencing_type}", '
                    f'referencing_subtype "{referencing_subtype}", '
                    f'referenced_type "{referenced_type}", '
                    f'referenced_subtype "{referenced_subtype}". '
                    f'Registered handlers: {handlers.keys()}'
                )

    def get_handlers(self, type,
                     referencing_type, referencing_subtype,
                     referenced_type, referenced_subtype,
                     raise_exception=False):
        yield from self._get_handlers(
            self.dependencies, type,
            referencing_type, referencing_subtype,
            referenced_type, referenced_subtype,
            raise_exception=raise_exception)

    def get_referencing_handlers(self, type, referenced_type, referenced_subtype):
        for tt in (referenced_type, None):
            for ts in (referenced_subtype, None):
                key = HandlerKey(
                    type=type,
                    referencing_type=None,
                    referencing_subtype=None,
                    referenced_type=tt,
                    referenced_subtype=ts,
                )
                yield from self.dependencies_by_referenced.get(key, [])

    @contextlib.contextmanager
    def bulk(self):
        try:
            reference_thread_local_context.start_bulk()
            yield self
        finally:
            reference_thread_local_context.finish_bulk()
            pass

    def updated(self,
                referenced_type,
                referenced_subtype,
                **kwargs):
        for handler in self.get_referencing_handlers(
            'inline', referenced_type, referenced_subtype
        ):
            reference_thread_local_context.object_updated(
                handler, kwargs
            )

    def removed(self,
                referenced_type,
                referenced_subtype,
                **kwargs):
        for handler in self.get_referencing_handlers(
            'inline', referenced_type, referenced_subtype
        ):
            reference_thread_local_context.object_removed(
                handler, kwargs
            )
        for handler in self.get_referencing_handlers(
            'reference', referenced_type, referenced_subtype
        ):
            reference_thread_local_context.object_removed(
                handler, kwargs
            )

    def moved(self,
              referenced_type,
              referenced_subtype,
              **kwargs):
        for handler in self.get_referencing_handlers(
            'inline', referenced_type, referenced_subtype
        ):
            reference_thread_local_context.object_moved(
                handler, kwargs
            )
        for handler in self.get_referencing_handlers(
            'reference', referenced_type, referenced_subtype
        ):
            reference_thread_local_context.object_moved(
                handler, kwargs
            )

    def flush_caches(self):
        """Used only in tests"""
        if 'dependencies' in self.__dict__:
            del self.__dict__['dependencies']
        if 'handlers' in self.__dict__:
            del self.__dict__['handlers']
        if 'dependencies_by_referenced' in self.__dict__:
            del self.__dict__['dependencies_by_referenced']


__all__ = ['ReferenceHandler', 'RecordReferenceAPI']
