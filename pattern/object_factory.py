class ObjectFactory:
    def __init__(self):
        self.builders = {}

    def register_builder(self, key, builder):
        self._builder[key] = builder

    def create(self, key, **kwargs):
        builder = self._builder.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)