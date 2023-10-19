#!/bin/env python3
# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    A copy of the GNU General Public License is available at
#    http://www.gnu.org/licenses/gpl-3.0.html

"""OTU clustering"""

import argparse
import sys
import os
import gzip
import statistics
import textwrap
import numpy as np
from pathlib import Path
from collections import Counter
from typing import Iterator, Dict, List
# https://github.com/briney/nwalign3
# ftp://ftp.ncbi.nih.gov/blast/matrices/
import nwalign3 as nw
np.int = int

__author__ = "Marwa Ghraizi"
__copyright__ = "Universite Paris Diderot"
__credits__ = ["Marwa Ghraizi"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Marwa Ghraizi"
__email__ = "marwaghraizi@gmail.com"
__status__ = "Developpement"



def isfile(path: str) -> Path:  # pragma: no cover
    """Check if path is an existing file.

    :param path: (str) Path to the file

    :raises ArgumentTypeError: If file does not exist

    :return: (Path) Path object of the input file
    """
    myfile = Path(path)
    if not myfile.is_file():
        if myfile.is_dir():
            msg = f"{myfile.name} is a directory."
        else:
            msg = f"{myfile.name} does not exist."
        raise argparse.ArgumentTypeError(msg)
    return myfile


def get_arguments(): # pragma: no cover
    """Retrieves the arguments of the program.

    :return: An object that contains the arguments
    """
    # Parsing arguments
    parser = argparse.ArgumentParser(description=__doc__, usage=
                                     "{0} -h"
                                     .format(sys.argv[0]))
    parser.add_argument('-i', '-amplicon_file', dest='amplicon_file', type=isfile, required=True, 
                        help="Amplicon is a compressed fasta file (.fasta.gz)")
    parser.add_argument('-s', '-minseqlen', dest='minseqlen', type=int, default = 400,
                        help="Minimum sequence length for dereplication (default 400)")
    parser.add_argument('-m', '-mincount', dest='mincount', type=int, default = 10,
                        help="Minimum count for dereplication  (default 10)")
    parser.add_argument('-o', '-output_file', dest='output_file', type=Path,
                        default=Path("OTU.fasta"), help="Output file")
    return parser.parse_args()


def read_fasta(amplicon_file: Path, minseqlen: int) -> Iterator[str]:
    """Read a compressed fasta and extract all fasta sequences.

    :param amplicon_file: (Path) Path to the amplicon file in FASTA.gz format.
    :param minseqlen: (int) Minimum amplicon sequence length
    :return: A generator object that provides the Fasta sequences (str).
    """
    with gzip.open(amplicon_file, "rt") as monfich:
        seq = ""
        for line in monfich:
            if line.startswith(">"):
                # if we exceeded min len we yield
                if len(seq) >= minseqlen:
                    yield seq
                seq = ""
            else:
                seq += line.strip()
        yield seq
            


def dereplication_fulllength(amplicon_file: Path, minseqlen: int, mincount: int) -> Iterator[List]:
    """Dereplicate the set of sequence

    :param amplicon_file: (Path) Path to the amplicon file in FASTA.gz format.
    :param minseqlen: (int) Minimum amplicon sequence length
    :param mincount: (int) Minimum amplicon count
    :return: A generator object that provides a (list)[sequences, count] of sequence with a count >= mincount and a length >= minseqlen.
    """
    seq_count = {}
    # another way with counter

    #all_sequences = list(read_fasta(amplicon_file, minseqlen))
   # unique_sequences = set(all_sequences)
    #for seq in unique_sequences:
        #seq_count = seq.count(all_sequences)
        #if seq._count >= mincount:
            #yield [seq, seq_count]
    
    
    for sequence in list(read_fasta(amplicon_file, minseqlen)):
        if sequence in seq_count:
            seq_count[sequence] += 1
        else:
            seq_count[sequence] = 1

    seq_count = sorted(seq_count.items(), key=lambda x:x[1], reverse=True) 
    for (seq, count) in seq_count:
        if count >= mincount:
            yield [seq, count]

def get_identity(alignment_list: List[str]) -> float:
    """Compute the identity rate between two sequences

    :param alignment_list:  (list) A list of aligned sequences in the format ["SE-QUENCE1", "SE-QUENCE2"]
    :return: (float) The rate of identity between the two sequences.
    """
    #alignment = nw.global_align(alignment_list[0], alignment_list[1], gap_open=-1, gap_extend=-1, matrix=os.path.abspath(os.path.join(os.path.dirname(__file__),"MATCH")))
    print(alignment_list)
    alignment_length = len(alignment_list[0])
    
    common_nucleotides = sum(1 for i in range(alignment_length) if alignment_list[0][i] == alignment_list[1][i])
    id = common_nucleotides/alignment_length*100
    print(id)
    return id

def abundance_greedy_clustering(amplicon_file: Path, minseqlen: int, mincount: int, chunk_size: int, kmer_size: int) -> List:
    """Compute an abundance greedy clustering regarding sequence count and identity.
    Identify OTU sequences.

    :param amplicon_file: (Path) Path to the amplicon file in FASTA.gz format.
    :param minseqlen: (int) Minimum amplicon sequence length.
    :param mincount: (int) Minimum amplicon count.
    :param chunk_size: (int) A fournir mais non utilise cette annee
    :param kmer_size: (int) A fournir mais non utilise cette annee
    :return: (list) A list of all the [OTU (str), count (int)] .
    """
    # align the first with all the sequences and add it to OTU bank if it exceeds 97% with any of them
    # align the second to the OTU bank
    # align the third to the OTU bank



def write_OTU(OTU_list: List, output_file: Path) -> None:
    """Write the OTU sequence in fasta format.

    :param OTU_list: (list) A list of OTU sequences
    :param output_file: (Path) Path to the output file
    """
    pass


#==============================================================
# Main program
#==============================================================
def main(): # pragma: no cover
    """
    Main program function
    """
    # Get arguments
    args = get_arguments()
    #fasta_zipped = args.amplicon_file
    #minseqlen = args.minseqlen
    #mincount = args.mincount
    get_identity(["TGGGGAATATTGCACAATGGGCGCAAGCCTG-ATGCAG", "TGGGGAATA--GCACAATGGGCGCAAGCCTCTAGCAG"])
    # Votre programme ici



if __name__ == '__main__':
    main()
