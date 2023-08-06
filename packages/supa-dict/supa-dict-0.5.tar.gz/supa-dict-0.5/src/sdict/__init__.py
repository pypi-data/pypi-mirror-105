""" sDict() is an "enhanced" dictionary object that allows you to address keys with dot notation. """

# Stdlib imports
import os
import json
from typing import Any

# 3rd party support
__HAVE_YAML__ = True
__HAVE_TOML__ = True

try:
    import yaml
except ImportError:
    __HAVE_YAML__ = False

try:
    import toml
except ImportError:
    __HAVE_TOML__ = False


class sDict(dict):
    """Example:
    obj = sDict({'foo': 'bar', 'baz': 'qux', 'bar': {'other': 'value'}})
    print(obj.foo) -> 'bar'
    obj.foo = 'foo'
    print(obj.foo) -> 'foo'
    print(obj.bar.other) -> 'value'
    """

    def __init__(self, data: dict = {}) -> None:
        dict.__init__(self)
        for k, v in data.items():
            if type(v) == dict:
                dict.__setitem__(self, k, sDict(v))
            else:
                dict.__setitem__(self, k, v)

    def __getattr__(self, attr: str) -> Any:
        if attr in dir(self):
            return dict.__getattribute__(self, attr)
        else:
            return dict.__getitem__(self, attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr in dir(self) and not attr in self.keys():
            return dict.__setattr__(self, attr, value)
        else:
            return dict.__setitem__(self, attr, value)

    # Underpin the markup language support
    def __markup__(self, fn: Any) -> str:
        if type(fn) == str and os.path.isfile(fn):
            return open(fn).read()
        elif type(fn) == str and not os.path.isfile(fn):
            return fn
        elif hasattr(fn, 'read'):
            return fn.read()
        return ''

    # Generic markup
    @property
    def markup(self) -> None:
        ''' This is a noop '''
        return

    @markup.setter
    def markup(self, arg: Any) -> None:
        # Start with JSON
        try:
            self.json = arg
        except json.decoder.JSONDecodeError:
            # Then YAML
            try:
                self.yaml = arg
            except yaml.scanner.ScannerError:
                # Finally TOML
                try:
                    self.toml = arg
                except toml.decoder.TomlDecodeError:
                    raise ValueError('Unsupported format.')

    # JSON support
    @property
    def json(self) -> str:
        return json.dumps(self)

    @json.setter
    def json(self, arg: Any) -> None:
        return self.update(sDict(json.loads(self.__markup__(arg))))

    # YAML support
    @property
    def yaml(self) -> str:
        if __HAVE_YAML__:
            return yaml.dump(self)
        raise ValueError('YAML support is not available. `pip3 install pyyaml`')

    @yaml.setter
    def yaml(self, arg: Any) -> None:
        if __HAVE_YAML__:
            return self.update(sDict(yaml.safe_load(self.__markup__(arg))))
        raise ValueError('YAML support is not available. `pip3 install pyyaml`')

    # TOML support
    @property
    def toml(self) -> str:
        if __HAVE_TOML__:
            return toml.dumps(self)
        raise ValueError('TOML support is not available. `pip3 install toml`')

    @toml.setter
    def toml(self, arg: Any) -> None:
        if __HAVE_TOML__:
            return self.update(sDict(toml.loads(self.__markup__(arg))))
        raise ValueError('TOML support is not available. `pip3 install toml`')

