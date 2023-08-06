What is ProteinBERT?
=============

ProteinBERT is a universal protein language model pretrained on ~106M proteins from the UniRef90 dataset. Through its Python API, the pretrained model can be fine-tuned on any protein-related task in a matter of minutes. Based on our experiments with a wide range of benchmarks, ProteinBERT usually achieves state-of-the-art performance. ProteinBERT is built on TenforFlow/Keras.

ProteinBERT's deep-learning architecture is inspired by BERT, but it contains several innovations such as its global-attention layers that grow only lineraly with sequence length (compared to self-attention's quadratic growth). As a result, the model can process protein sequences of almost any length, includng extremely long protein sequences (of over tens of thousands of amino acids).

The model takes protein sequences as inputs, and can also take protein GO annotations as additional inputs (to help the model infer about the function of the input protein and update its internal representations and outputs accordingly).
This package provides seamless access to a pretrained state that has been produced by training the model for 28 days over ~670M records (i.e. ~6.4 iterations over the entire training dataset of ~106M records). For users interested in pretraining the model from scratch, the package also includes scripts for that.


Installation
=============

Dependencies
------------

ProteinBERT requires Python 3.

Below are the Python packages required by ProteinBERT, which are automatically installed with it (and the versions of these packages that were tested with ProteinBERT 1.0.0):

* tensorflow (2.4.0)
* numpy (1.20.1)
* pandas (1.2.3)
* h5py (3.2.1)
* lxml (4.3.2)
* pyfaidx (0.5.8)


Install ProteinBERT
------------

Just run:

.. code-block:: sh

    pip install protein-bert
    
Alternatively, clone this repository and run:

.. code-block:: sh

    python setup.py install
    
    
Using ProteinBERT
=============

Fine-tuning ProteinBERT is very easy. You can see some working examples `in this notebook <https://github.com/nadavbra/protein_bert/blob/master/ProteinBERT%20demo.ipynb>`_.
    
    
Pretraining ProteinBERT from scratch
=============

If, instead of using the existing pretrained model weights, you would like to train it from scratch, then follow the steps below. We warn you however that this is a long process (we pretrained the current model for a whole month), and it also requires a lot of storage (>1TB).

Step 1: Create the UniRef dataset
------------

ProteinBERT is pretrained on a dataset derived from UniRef90. Follow these steps to produce this dataset:

1. First, choose a working directory with sufficient (>1TB) free storage.

.. code-block:: sh
    
    cd /some/workdir

2. Download the metadata of GO from CAFA and extract it.

.. code-block:: sh

    wget https://www.biofunctionprediction.org/cafa-targets/cafa4ontologies.zip
    mkdir cafa4ontologies
    unzip cafa4ontologies.zip -d cafa4ontologies/
    
3. Download UniRef90, as both XML and FASTA.

.. code-block:: sh

    wget ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.xml.gz
    wget ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz
    gunzip uniref90.fasta.gz
    
4. Use the *create_uniref_db* script provided by ProteinBERT to extract the GO annotations associated with UniRef's records into an SQLite database (and a CSV file with the metadata of these GO annotations). Since this is a long process (which can take up to a few days), it is recommended to run this in the background (e.g. using *nohup*).
    
.. code-block:: sh

    nohup create_uniref_db --uniref-xml-gz-file=./uniref90.xml.gz --go-annotations-meta-file=./cafa4ontologies/go.txt --output-sqlite-file=./uniref_proteins_and_annotations.db --output-go-annotations-meta-csv-file=./go_annotations.csv >&! ./log_create_uniref_db.txt &
    
5. Create the final dataset (in the H5 format) by merging the database of GO annotations with the protein sequences using the *create_uniref_h5_dataset* script provided by ProteinBERT. This is also a long process that should be let to run in the background.

.. code-block:: sh
    
    nohup create_uniref_h5_dataset --protein-annotations-sqlite-db-file=./uniref_proteins_and_annotations.db --protein-fasta-file=./uniref90.fasta --go-annotations-meta-csv-file=./go_annotations.csv --output-h5-dataset-file=./dataset.h5 --min-records-to-keep-annotation=100 >&! ./log_create_uniref_h5_dataset.txt &
    
6. Finally, use ProteinBERT's *set_h5_testset* script to designate which of the dataset records will be considered part of the test set (so that their GO annotations are not used during pretraining). If you are planning to evaluate your model on certain downstream benchmarks, it is recommended that any UniRef record similar to a test-set protein in these benchmark will be considered part of the pretraining's test set. You can use BLAST to find all of these UniRef records and provide them to *set_h5_testset* through the flag ``--uniprot-ids-file=./uniref_90_seqs_matching_test_set_seqs.txt``, where the provided text file contains the UniProt IDs of the relevant records, one per line (e.g. *A0A009EXK6_ACIBA*).

.. code-block:: sh

    set_h5_testset --h5-dataset-file=./dataset.h5
    
    
Step 2: Pretrain ProteinBERT on the UniRef dataset
------------

Once you have the dataset ready, the *pretrain_proteinbert* script will train a ProteinBERT model on that dataset.

Basic use of the pretraining script looks as follows:

.. code-block:: sh

    mkdir -p ~/proteinbert_models/new
    nohup pretrain_proteinbert --dataset-file=./dataset.h5 --autosave-dir=~/proteinbert_models/new >&! ~/proteinbert_models/log_new_pretraining.txt &
    
By running that, ProteinBERT will continue to train indefinitely. Therefore, make sure to run it in the background using *nohup* or other options. Every given number of epochs (determined as 100 batches) the model state will be automatically saved into the specified autosave directory. If this process is interrupted and you wish to resume pretraining
from a given snapshot (e.g. the most up-to-date state file within the autosave dir) use the ``--resume-from`` flag (provide it the state file that you wish to resume from).

*pretrain_proteinbert* has MANY options and hyper-parameters that are worth checking out:

.. code-block:: sh

    pretrain_proteinbert --help
    
    
Step 3: Use your pretrained model state when fine-tuning ProteinBERT
------------

Normally the function *load_pretrained_model* is used to load the existing pretrained model state. If you wish to load your own pretrained model state instead, then use the *load_pretrained_model_from_dump* function instead.

    
License
=======
ProteinBERT is a free open-source project available under the `MIT License <https://en.wikipedia.org/wiki/MIT_License>`_.
 
   
Cite us
=======

TODO
