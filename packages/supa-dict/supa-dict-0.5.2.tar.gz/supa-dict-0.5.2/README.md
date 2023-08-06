# sDict (Supa Dict!)

#### Installation

Installation can be done via pypi:
`pip3 install supa-dict`

#### Usage

SDict is an enhanced dictionary object for Python. It has several features
and applications especially well suited to use in templating engines. The
biggest enhancement is the ability to use dot notation for 'pathing' your
data. For example:

```python
>>> from supa_dict import sDict
>>> obj = sDict({'foo': 'bar', 'baz': {'key': 'val'}})
>>> print(obj.baz.key)
'val'
>>>
```

You can also use the .json, .yaml, and .toml attributes to load and dump
data in different formats. For instance with the following json file as
`./test.json`:

```json
{
  "foo": "bar",
  "baz": {
    "key": "val"
  }
}
```

You can import the json data using the .json property:

```python
>>> from supa_dict import sDict
>>> obj = sDict()
>>> obj.json = './test.json'
>>> print(obj)
{'foo': 'bar', 'baz': {'key': 'val'}}
>>> print(obj.baz.key)
'val'
>>>
```
