# src/core/id_generator.py
"""
ID GENERATOR
Clean alternative to global mutable counters. Each entity type gets its own
sequential counter, eliminating the need for the global keyword inside entity
modules and keeping ID logic self-contained.
"""
from itertools import count


class IDGenerator:
    def __init__(self):
        self._counters = {}

    def next_id(self, prefix: str) -> str:
        if prefix not in self._counters:
            self._counters[prefix] = count(1)
        return f"{prefix}_{next(self._counters[prefix])}"


# Singleton واحد يتشارك فيه كل الـ entities
id_generator = IDGenerator()
