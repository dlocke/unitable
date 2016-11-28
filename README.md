# UniTable

This Python package provides a "Universal Table" data structure.

Most of the code in this package was written in 2005-2007 at Open Data Group and originally targeted Python 2.3-2.4.  It was originally released as part of Augustus via SourceForge.  I've decided to re-release the code as a stand-alone package in the hopes that someone else will find this as useful as I have.

# Description

The "UniTable" is an implementation of a conceptual "Universal Table".
The data structure is analogous to an R frame: a table where the
columns are vectors of equal length, but may be of different types.
It is based on the Python numpy package and the programming interface
attempts to maintain consistency with the style established therein.

The design goal was to create a very fast, efficient object for data
shaping, model building, and scoring, both in a batch and real-time
context.  The key features are:

- Fast vector operations using any number of data columns.

- Support for demand driven, rule based calculations.  Derived columns
  can be defined in terms of operations on other columns, including other
  derived columns, and will be made available when referenced.

- The ability to invoke calculations in scalar or vector mode transparently.
  Thus, one set of rule definitions can be applied to an entire
  data set in batch mode, or to individual rows incoming as real-time
  events.

# Usage Examples

The typical way to create a UniTable is:

```python
from unitable import UniTable
tbl = UniTable
tbl.fromfile(filename)
```

Key order is maintained and may be indexed by name or number:

```python
>>> data = {'a':(1,2,3),'ts':(34567,35678,34657),'values':(5.4,2.2,9.9)}
>>> keyorder = ('a','ts','values')
>>> t = UniTable(keys=keyorder,**data)
>>> print t
+-+-----+------+
|a|  ts |values|
+-+-----+------+
|1|34567|   5.4|
|2|35678|   2.2|
|3|34657|   9.9|
+-+-----+------+

>>> print t[0]
[1, 34567, 5.4000000000000004]
>>> print t['ts']
[34567 35678 34657]
>>> print t.field(2)
[ 5.4  2.2  9.9]
```

Row Records maintain link to original data:

```python
>>> rec = t[1]
>>> print rec
[2, 35678, 2.2000000000000002]
>>> rec[2] = 2.3
>>> rec[1] = 99999
>>> print rec
[2, 99999, 2.2999999999999998]
>>> print repr(rec)
row 1: {'a':2, 'ts':99999, 'values':2.2999999999999998}
>>> print t
+-+-----+------+
|a|  ts |values|
+-+-----+------+
|1|34567|   5.4|
|2|99999|   2.3|
|3|34657|   9.9|
+-+-----+------+
```

Additional examples:

```python
>>> junk = t.newfield('addon')
>>> t['alpha'] = ['some','text','values']
>>> print t
+-+-----+------+-----+------+
|a|  ts |values|addon|alpha |
+-+-----+------+-----+------+
|1|34567|   5.4|    0|  some|
|2|99999|   2.3|    0|  text|
|3|34657|   9.9|    0|values|
+-+-----+------+-----+------+

>>> t['added'] = t['a'] + t['ts']
>>> print t
+-+-----+------+-----+------+------+
|a|  ts |values|addon|alpha |added |
+-+-----+------+-----+------+------+
|1|34567|   5.4|    0|  some| 34568|
|2|99999|   2.3|    0|  text|100001|
|3|34657|   9.9|    0|values| 34660|
+-+-----+------+-----+------+------+

>>> t.append((4,77777,6.6,1,'here',88888))
>>> print t
+-+-----+------+-----+------+------+
|a|  ts |values|addon|alpha |added |
+-+-----+------+-----+------+------+
|1|34567|   5.4|    0|  some| 34568|
|2|99999|   2.3|    0|  text|100001|
|3|34657|   9.9|    0|values| 34660|
|4|77777|   6.6|    1|  here| 88888|
+-+-----+------+-----+------+------+

>>> print t[1:3]
+-+-----+------+-----+------+------+
|a|  ts |values|addon|alpha |added |
+-+-----+------+-----+------+------+
|2|99999|   2.3|    0|  text|100001|
|3|34657|   9.9|    0|values| 34660|
+-+-----+------+-----+------+------+

>>> print t.take([1,3])
+-+-----+------+-----+-----+------+
|a|  ts |values|addon|alpha|added |
+-+-----+------+-----+-----+------+
|2|99999|   2.3|    0| text|100001|
|4|77777|   6.6|    1| here| 88888|
+-+-----+------+-----+-----+------+

>>> print t.subtbl(t['a']-3 == t['addon'])
+-+-----+------+-----+------+-----+
|a|  ts |values|addon|alpha |added|
+-+-----+------+-----+------+-----+
|3|34657|   9.9|    0|values|34660|
|4|77777|   6.6|    1|  here|88888|
+-+-----+------+-----+------+-----+

>>> t2 = t.sorted_on('values')
>>> print t2
+-+-----+------+-----+------+------+
|a|  ts |values|addon|alpha |added |
+-+-----+------+-----+------+------+
|2|99999|   2.3|    0|  text|100001|
|1|34567|   5.4|    0|  some| 34568|
|4|77777|   6.6|    1|  here| 88888|
|3|34657|   9.9|    0|values| 34660|
+-+-----+------+-----+------+------+
>>> assert t2 != t
>>> t2.sort_on('a')
>>> assert t2 == t

>>> print t.to_csv_str(sep=',')
a,ts,values,addon,alpha,added
1,34567,5.4,0,some,34568
2,99999,2.3,0,text,100001
3,34657,9.9,0,values,34660
4,77777,6.6,1,here,88888

>>> for row in t.izip(): print row
(1, 34567, 5.4000000000000004, 0, 'some', 34568)
(2, 99999, 2.2999999999999998, 0, 'text', 100001)
(3, 34657, 9.9000000000000004, 0, 'values', 34660)
(4, 77777, 6.5999999999999996, 1, 'here', 88888)
```

# TODOs

- Highlight EvalTable in this README.
- Highlight the NAB ("NumArray Binary") file format in this README.
- Add unit and regression testing.