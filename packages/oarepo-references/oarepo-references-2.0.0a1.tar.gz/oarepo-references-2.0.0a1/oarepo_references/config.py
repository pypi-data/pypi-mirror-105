OAREPO_REFERENCES_DEFAULT_DEPENDENCY_HANDLERS = [
    {
        "type": "reference",
        "referencing": {
            "type": "record"
        },
        "handler": "oarepo_references.record.RecordReferenceHandler"
    },
    {
        "type": "inline",
        "referencing": {
            "type": "record"
        },
        "handler": "oarepo_references.record.RecordInlineReferenceHandler"
    },
]


OAREPO_REFERENCES_DEPENDENCY_HANDLERS = [
    # add your own dependency handlers in your config code
]

OAREPO_REFERENCES_DEPENDENCIES = [
    # add your application dependencies in your config code
]
