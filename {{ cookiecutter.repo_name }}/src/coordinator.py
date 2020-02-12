import glob
import json
import os
import pickle

import pandas as pd
import yaml


class Path:
    """Incapsulates directory surfing.

        Usage example:
            p = Path('.')
            p
            > '/opt/shared/kishenya'
            p.join('data').join('raw')
            > '/opt/shared/kishenya/data/raw'
            p.join('data').join('raw').back()
            p.join('data').join('raw').up()  # same
            > '/opt/shared/kishenya/data'
            p.join('data').exists
            > True
            p.join('dataakjnfjknajkn').exists
            > False
            p.join('data').join('raw').contents()
            > ['/opt/shared/kishenya/data/raw/cards_ai.csv',
            '/opt/shared/kishenya/data/raw/retail_ai.csv',
            '/opt/shared/kishenya/data/raw/shop_ai.csv']
            p.save([1,2,3])
            > None
            p.load()
            > [1,2,3]
    """
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def __repr__(self):
        return self.path

    def join(self, other):
        return Path(os.path.join(self.path, other))

    def back(self):
        return Path(os.path.dirname(self.path))

    def up(self):
        return self.back()

    def load(self, *args, **kwargs):
        if self.path.endswith('yml') or self.path.endswith('yaml'):
            with open(self.path) as f:
                return yaml.load(f, *args, **kwargs)
        if self.path.endswith('csv'):
            return pd.read_csv(self.path, *args, **kwargs)
        if self.path.endswith('json'):
            with open(self.path) as f:
                return json.load(f, *args, **kwargs)
        # treat as pickle object
        with open(self.path, 'rb') as f:
            return pickle.load(f, *args, **kwargs)

    def save(self, obj):
        with open(self.path, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def contents(self, recursive=True):
        if recursive:
            p = glob.glob(os.path.join(self.path, '**'), recursive=True)
        else:
            p = glob.glob(os.path.join(self.path, '*'), recursive=False)
        return sorted([x for x in p
                       if not os.path.isdir(x)], key=lambda s: s.lower())

    @property
    def exists(self):
        return os.path.isdir(self.path) or os.path.isfile(self.path)


class Coordinator:
    """Provides paths to main folders.

    Initializes paths to `root`, `src`, etc.
    Every field is a member of Path, not str.

        Usage example::
            # From a notebook
            c = Coordinator()
            c.root
            > '/opt/shared/kishenya'
            c.data_interim
            > '/opt/shared/kishenya/data/interim'
    """
    def __init__(self, path='..'):
        path = os.path.abspath(path)

        self.root = Path(path)
        self.configs = self.root.join('configs')
        self.data = self.root.join('data')
        self.data_raw = self.data.join('raw')
        self.data_interim = self.data.join('interim')
        self.data_external = self.data.join('external')
        self.data_processed = self.data.join('processed')
        self.notebooks = self.root.join('notebooks')
        self.models = self.root.join('models')
        self.reports = self.root.join('reports')
        self.dotenv = self.root.join('.env')
