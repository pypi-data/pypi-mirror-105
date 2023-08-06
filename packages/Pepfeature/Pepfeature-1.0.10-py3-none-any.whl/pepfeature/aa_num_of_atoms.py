"""
    This module contains methods to Calculate for each given sequence the total number of
    atoms of each type in that sequence (which is essentially a weighted sum of the aminoacid numbers). Results
    returned as CSV(s) or DataFrame.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

import pandas as pd
import numpy as np
from pepfeature import _utils

def _algorithm(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates for each given sequence the total number of
    atoms of each type in that sequence (which is essentially a weighted sum of the aminoacid numbers)

    Results appended as a new columns named feat_C_atoms, feat_H_atoms, feat_N_atoms, feat_O_atoms, feat_S_atoms

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """

    # Dataframe holding the number of each type of atom (C, H, O, N, S) for each Amino Acid:
    atom_groups_df = pd.DataFrame(data={'nC': [3, 3, 4, 5, 9, 2, 6, 6, 6, 6, 5, 4, 5, 5, 6, 3, 4, 5, 11, 9],
                                        'nH': [7, 7, 7, 9, 11, 5, 9, 13, 14, 13, 11, 8, 9, 10, 14, 7, 9, 11, 12, 11],
                                        'nN': [1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 2, 4, 1, 1, 1, 2, 1],
                                        'nO': [2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 3, 2, 2, 3],
                                        'nS': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                                  index=['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S',
                                         'T', 'V', 'W', 'Y'])

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = list(getattr(row, aa_column))

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)

        #Variables for each atom, to keep count of weighted sum for each aa in the peptide
        count_nC = 0
        count_nH = 0
        count_nN = 0
        count_nO = 0
        count_nS = 0


        for i in range(len(every_unique_aa)):
            count_nC+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nC'])
            count_nH+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nH'])
            count_nN+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nN'])
            count_nO+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nO'])
            count_nS+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nS'])

        #Creating the features and setting them
        dataframe.loc[row.Index, 'feat_C_atoms'] = count_nC
        dataframe.loc[row.Index, 'feat_H_atoms'] = count_nH
        dataframe.loc[row.Index, 'feat_N_atoms'] = count_nN
        dataframe.loc[row.Index, 'feat_O_atoms'] = count_nO
        dataframe.loc[row.Index, 'feat_S_atoms'] = count_nS

    return dataframe




def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates for each given sequence the total number of
    atoms of each type in that sequence (which is essentially a weighted sum of the aminoacid numbers) chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new columns named feat_C_atoms, feat_H_atoms, feat_N_atoms, feat_O_atoms, feat_S_atoms

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """

    _utils.multiprocessing_export_csv(dataframe=dataframe, function=_algorithm, Ncores=Ncores, chunksize=chunksize,
                                      save_folder=save_folder, aa_column=aa_column)

def calc_df(dataframe: object, Ncores: int = 1, aa_column: str = 'Info_window_seq'):
    """
     Calculates for each given sequence the total number of
    atoms of each type in that sequence (which is essentially a weighted sum of the aminoacid numbers)

    Results appended as a new columns named feat_C_atoms, feat_H_atoms, feat_N_atoms, feat_O_atoms, feat_S_atoms

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """
    return _utils.multiprocessing_return_df(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                            aa_column=aa_column)