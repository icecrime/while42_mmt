import os
import yaml


def load(filepath):
    # Inject the YAML configuration file describing database connection and stuff.
    with open(os.path.join(filepath)) as f:
        globals().update(yaml.load(f))
