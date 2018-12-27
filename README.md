# MpAnalysis.Y1
An approach to accurately genotype STR and SNP using the multiplex PCR data and implement automatic conversion of CODIS system to STR.

# Extra SNP or STR locus
Apart from the CODIS locus information that we provided yet, a custom set of SNP/STR loci is also supported by MpAnalysis.Y1. For those loci that users are interested in, the target sequences in the same direction (at least 30bp non-homologous regions before and after the locus) are required. Besides, a corresponding internal reference containing sequence of repeats and the number of repeats units on the hg38 genome are necessary for each locus. For details, see the reference files uploaded already.

## Installation
To install, first download and unpack the newest release from GitHub:

    $ git clone https://github.com/MpAnalysisY1/MpAnalysis.Y1.git
    $ cd MpAnalysis.Y1

To compile, run:

    $ make

## Usage

To get help, run:

    $ python MpAnalysis.Y1.py --help

    Usage: MpAnalysis.Y1.py [options]

    Options:
      -h, --help            show this help message and exit
      -I LIST, --input_list=LIST
                        Input your data information
      -O OUTDIR, --outdir=OUTDIR
                        Output Directory
      -P THREADS NUM, --threads=THREADS NUM
                            Input the thread number(default:5)
      --AdaptClean=Boolean  When set as True, built-in AdapterRemoval v2 (http://b
                            mcresnotes.biomedcentral.com/articles/10.1186/s13104-0
                            16-1900-2) is used to search for and remove remnant
                            adapter sequences(default:False)
      -F PrimerF, --PrimerForward=PrimerF
                            Forward primer for cleaning, and --AdaptClean must be
                            set as True.(default: Illumina TruSeq LT and TruSeq
                            HT-based kits Read 1:
                            AGATCGGAAGAGCACACGTCTGAACTCCAGTCA)
      -R PrimerR, --PrimerReverse=PrimerR
                            Reverse primer for cleaning, and --AdaptClean must be
                            set as True.(default: Illumina TruSeq LT and TruSeq
                            HT-based kits Read 2:
                            AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT)
                        
To genotype STR and SNP without adapter trimming, run:

    $ python MpAnalysis.Y1.py -I input.list -O outdir
