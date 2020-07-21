import yaml
import jinja2
import os

TRANSFORMERS = dict()


def parseable(cls):

    name = cls.__name__

    if name in TRANSFORMERS:
        raise ValueError(f"Transformer '{name}' is already registered.")

    TRANSFORMERS[name] = cls

    return cls


def parse(structure):

    if isinstance(structure, list):
        return TRANSFORMERS["Compose"].parse(transformers=structure)
    elif isinstance(structure, dict):
        if len(structure) == 0:
            raise ValueError("Received empty dictionary")
        elif len(structure) > 1:
            raise ValueError(f"Received multiple items: {list(structure)}")

        [(name, kwargs)] = structure.items()

        if kwargs is None:
            kwargs = {}

        return TRANSFORMERS[name].parse(**kwargs)


def loads(content, key="transformers", values=None):

    if values is None:
        values = {}

    env_vars = os.environ.copy()
    env_vars.update(values)

    template = jinja2.Template(content)
    content = template.render(**env_vars)

    structure = yaml.safe_load(content)[key]

    return parse(structure)


def load(buffer, key="transformers", values=None):

    content = buffer.read()

    return loads(content, key=key, values=values)

