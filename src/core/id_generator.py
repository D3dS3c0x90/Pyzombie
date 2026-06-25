# src/core/id_generator.py
"""
🆔 ID GENERATOR
بديل نظيف للـ global mutable variables (ZOMBIE_ID, BULLET_ID) اللي كانت
في settings.py القديم. كل entity نوع بياخد counter منفصل بدون استخدام
global keyword جوه entities.py.
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
