Abbreviation Resolver
=====================
Abbreviation resolver is a Python library, which task is to identify and 
disambiguate acronyms and abbreviation in text.
For example, given a sentence "Web site underwent a severe DOS attack.", 
the program should suggest the right interpretation of "DOS" among the set 
of candidates "Denial-of-service", "Disk operating system" and "Data over signalling".


Abbreviation resolver supports Python versions 2.7 and 3.4 


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
>> from abresolver import Text
>> t = Text(u'kolmas p palavik')
>> t.tokenize_abs()
[{
  'text': 'p',
  'start': 7,
  'end': 8,
  'expansions': ['päev',
                 'parem',
                 'parietaalne',
                 'pupill',
                 'pool'],
  'scores': [0.99974249284129602,
             0.00013896032431022265,
             0.00010385371199489893,
             9.3145225880433136e-06,
             5.3785998108879645e-06],
  }]

>> t = Text(u'püsib p pahhüpleuraalne ladestus')
>> t.tokenize_abs()
[{'text': 'p',
  'start': 6,
  'end': 7,
  'expansions': ['parietaalne',
                 'päev',
                 'parem',
                 'pupill',
                 'pool'],
  'scores': [0.83779262694858747,
             0.072167145074973585,
             0.06692486376766027,
             0.023099431317849875,
             1.5932890928882162e-05],
  }]
```

A call to `tokenize_abs()` creates a new layer 'abr' in a Text object,
which contains analysis information for each abbreviation or acronym identified in text.
Analysis entry includes abbreviation text itself, its start and end position in the document,
a list of candidate full forms with the corresponding scores.
The candidate terms are sorted by score, such that the most likely candidate 
with a higher score comes first.

These attributes can be accessed individually using the corresponding properties:
```python
>> t = Text(u'püsib p pahhüpleuraalne ladestus. kolmas p palavik')
>> t.abr_texts
['p', 'p']
>> t.abr_spans
[(6, 7), (41, 42)]
>> t.abr_expansions
[['parietaalne', 'päev', 'parem', 'pupill', 'pool'],
 ['päev', 'parem', 'parietaalne', 'pupill', 'pool']]
>> t.abr_scores
[[0.6196715074809509,
  0.36973995956261818,
  0.0097006165941946505,
  0.00087920614701522952,
  8.7102152210321713e-06],
 [0.99974249284129602,
  0.00013896032431022265,
  0.00010385371199489893,
  9.3145225880433136e-06,
  5.3785998108879645e-06]]
```


Data
----
Abbreviation resolver requires two datafiles - *abbreviation model* and *word2vec model* - which are not included into the package due to data protection issues. 


### Abbreviation Model
Abbreviation model provides probabilities P(term|abbreviation) which were estimated based on a training corpus.
The model is stored in a .csv file with columns term, abbreviation, and P(term|abbreviation), e.g.

| t             | a             | P(t&#124;a)|
| ------------- |:-------------:| --------:|
| temperatuur   | t             | 0.383632 |
| tund          | t             | 0.242967 |
| tänav         | t             | 0.005115 |
| tumor         | t             | 0.056266 |
| diameeter     | d             | 0.669767 |
| diagnoos      | d             | 0.304651 |
| distants      | d             | 0.016279 |
| distants      | d             | 0.016279 |
| disc          | d             | 0.009302 |


### Word2vec Model
Word2vec model enable to estimate how well individual words, such as abbreviation full forms, fit the sentence context.
Word2vec models can be trained using [gensim](https://radimrehurek.com/gensim/) or [word2vec](https://code.google.com/p/word2vec/) software. 
To load the model, abbreviation resolver uses *gensim* API:
```
gensim.models.Word2Vec.load(model_file_name)
```
Pre-trained general purpose word2vec models for Estonian can be obtained from https://github.com/estnltk/word2vec-models.


