import enum
from functools import lru_cache


class Scope(enum.Enum):
    Singleton = "Singleton"
    NoScope = "NoScope"


def inject(scope: Scope = Scope.Singleton):

    def _inject(cls):
        def get_instance() -> cls:
            arguments = {}
            for d_name, d_type in cls.__init__.__annotations__.items():
                if d_name == "return":
                    continue
                arguments[d_name] = d_type.get_instance()
            return cls(**arguments)

        if scope == Scope.Singleton:
            get_instance = lru_cache(1)(get_instance)

        cls.get_instance = get_instance
        return cls

    return _inject
