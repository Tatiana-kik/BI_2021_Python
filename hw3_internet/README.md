# HW3:  TBLASTN

**Tblastn** is a python module to search proteins in NCBI databases.


## 1. Overview

**Tblastn** get search parameters from user, make request to NCBI database 
and give result to user.

It is possible to use this module in 2 modes:
1. Single application mode;
1. API mode.


## 2. Requirements

Code was tested on Ubuntu 20.04, Python 3.8.10.
Necessary modules are listed in requirements.txt file.
To intstall them need to run `pip install -r requirements.txt`.


## 3. Single application mode

It is possible to run the module as single application like:<br>
`python tblastn.py -s <protein_seq> -d <database> -t <taxon> -w <max_awaiting>`

### 3.1 Parameters

- **protein\_seq** - protein sequence;
- **database name** - current version supports only 2 options:
   - **nt** (Nucleotide Collection) and
   - **wgs** (Whole-Genome Shotgun  Contigs);
- **taxon** - taxon name in NCBI format;
- **max_awaiting** - maximum awaiting timeout in seconds, default is 60 seconds.

Please see the NCBI website to get Taxon valid names.

### 3.2 Example

`python tblastn.py -s 442632573 -d wgs -t "Drosophila irilis (taxid:7244)" -w 500`

This request makes search of the sequence "442632573" in database "wgs" for taxon 
with the name "Drosophila irilis (taxid:7244)".


## 4. API mode

It is possible to import **tblastn** in your python code and use API functions 
like:<br>
`alignments, errtext = tblastn_find(sequence, database, taxon, verbose, seconds)`<br>
and<br>
`tblastn_print_result(alignments)`


### 4.1 API:  tblast\_find()

This function makes search of protein sequence in NCBI databases.<br>
Calling of function has view:<br>
`alignments, errtext = tblastn_find(sequence, database, taxon, verbose, seconds)`<br>

**4.1.1 Parameters**<br>

- **sequence** - protein sequence;
- **database** - current version supports only 2 options:
   - **nt** (Nucleotide Collection) and
   - **wgs** (Whole-Genome Shotgun Contigs);
- **taxon** - taxon name in NCBI format;
- **verbose** - verbose parameter to see additional output: 0 (default) 1 or 2;
- **seconds** - maximum awaiting timeout in seconds, default is 60 seconds.

Please see the NCBI website to get Taxon valid names.

**4.1.2 Return value**<br>

- **alignments** - list of alignments, each list item has a lot of info (see below)
- **errtext** - error text, empty string if all is okay and error description in 
other case.

**4.1.3 Alignment structure**

**Alignment** is a python dictionary with the next keys:

- seq\_id
- seq\_accession
- seq\_title
- seq\_length:
- bit-score
- score
- evalue
- identity
- positive
- query-from
- query-to
- hit-from
- hit-to
- hit-frame
- align-len
- gaps
- qseq
- hseq
- midline

**4.1.4 Example**<br>

```python
#import tblastn

alignments, errtext = tblastn_find('442632573', 'nt', 'Drosophila irilis (taxid:7244)',
                                   verbose=1, seconds=120)
if errtext:
    print(f'Error:  {errtext}')
else:
    tblastn_print_result(alignments)
```

**4.1.5 Communication flow**

During the work this API function makes several HTTP requests. In general
it looks like this:

1. make initial POST request with all search parameters;
1. get reply with Request ID;
1. in cycle ask search status by doing GET requests;
1. when search status is READY - request the search result in XML format;
1. parce XML and fill Alignments structures (dictionaries);
1. return result.

### 4.2 API:  tblastn\_print\_result()

Calling of function has view:<br>
`tblastn_print_result(alignments)`

**4.2.1 Parameters**<br>

- **alignments** - list of dictionaries, that returns tblastn\_find().

**4.2.2 Return value**<br>

No return value.


## 5. Conclusion

### 5.1 What do we have?

As a result we have a python application and API to make search in NCBI databases.
This is a convenient option for automation of the alignment search.

### 5.2 Problems

Search in NCBI databases is complicated. There are about 90 parameters in a request
and it is possible to tune the request if need. But **tblastn** module supports only
3 parameters and it is possible tochoose only 2 databases. This limitation of current 
version of sorfware is due to a long time of testing and debugging complicated 
functionality.

Moreover NCBI servers can be busy and for the same request the search time may vary
from 10 seconds till 10 minutes. This makes debugging and testing more slow.

At the same time NCBI server can keep silens and do not reply. In this case python 
module `request` catch exception and you can see output in console.
