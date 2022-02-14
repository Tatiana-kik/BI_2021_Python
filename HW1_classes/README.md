
# Homework #1

## 1. Class for representation of fish

This class is a simple representation of fish. The 'fish' has the next
attributes - _age_, _size_ and _weight_. And the 'fish' can be _dead_
or _alive_ and can _grow_ (method _grow()_) that increase _age_, _size_ and
_weight_.


## 2. Class for representation of RNA

This class is a simple representation of RNA. It has the next abilities:
* translate\_to\_protein() - translation RNA to protein,
* back\_translation\_to\_dna() - back translation to DNA.


## 3. Class PositiveSet for storage not negative values

This class can store not negative values. But the task requirements are not clear.
As we know, original _set_ can store any types of data. But task require:
* in constructor - store positive **numbers**, but
* in _add()_ function - store not negative **elements**.

I strictly followed these requirements. 
But still the class PositiveSet looks strange for me.


## 4. Class FastaStatistics to get information about FASTA file

This class allows to get the next information from FASTA file:
* get\_seq\_number() - get sequence number,
* get\_gc() - get GC in %,
* make\_histo\_of\_lengths() - draw distribution of sequence lengths,
* make\_histo\_of\_clusters() - draw distribution of clusters with length K,
* make\_histo\_of\_aminos() - draw distribution of aminoacids (extra task for +1 point),
* make\_plot\_of\_gc() - draw distribution of GC% (extra task for +1 point).

Also it is possible to get all metrics by calling the function do\_all().


## Python version

This HW was tested on Python 3.8.10 on Ubuntu 20.04 machine.
