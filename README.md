Abbreviation Resolver
=====================
Abbreviation resolver is a Python library, which task is to identify and disambiguate acronyms and abbreviation in text.

Abbreviation resolver supports Python 2.7.


Installation
------------
```bash
    $ git clone https://github.com/estnltk/abbreviation-resolver
    $ cd abbreviation-resolver
    $ python setup.py install
```


Development installation with zc.buildout
-----------------------------------------
```bash    
    $ git clone https://github.com/estnltk/abbreviation-resolver
    $ cd abbreviation-resolver
    $ python bootstrap.py
    $ ./bin/buildout
```


Usage
-----
To run abbreviation resolver, first it's necessary to create a configuration file which specifies file locations of the abbreviation and word2vec models, e.g.
```
[MODEL]
ABBREVIATION_MODEL=/opt/home/sass/projects/lyhendid/tasks/model/results/model.csv
WORD2VEC_MODEL=/opt/home/sass/projects/lyhendid/tasks/etl/results/word2vec/all.snts.word.wvm
```
and export an environment variable `CONFIG` pointing to the configuration file
```
$ export CONFIG=<configuration file path>
```

Now abbreviation resolver is ready for use:
```python
> from abresolver import Text
> t = Text('')
>t.tokenize_abs()
```


Data
----
Abbreviation resolver requires two datafiles - `abbreviation model` and `word2vec model` - which are not included into the package due to licensing issues. 

