"""
    This module contains 2 functions to calculate Frequency of Amino Acid types for given amino acid sequences. Results
    returned as CSV(s) or DataFrame.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

from pepfeature import _utils

def _algorithm(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates Frequency of Amino Acid types for given amino acid sequences

    For each sequence calculates nine features corresponding to the proportion (out of 1) of each Amino Acid type in the sequences

    Results appended as a new columns named feat_Prop_{group-value} e.g.  feat_Prop_Tiny, feat_Prop_Small etc.

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """
    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_groups_dict = {'Tiny': ["A", "C", "G", "S", "T"], 'Small': ["A", "B", "C", "D", "G", "N", "P", "S", "T", "V"],
                      'Aliphatic': ["A", "I", "L", "V"], 'Aromatic': ["F", "H", "W", "Y"],
                      'NonPolar': ["A", "C", "F", "G", "I", "L", "M", "P", "V", "W", "Y"],
                      'Polar': ["D", "E", "H", "K", "N", "Q", "R", "S", "T", "Z"],
                      'Charged': ["B", "D", "E", "H", "K", "R", "Z"], 'Basic': ["H", "K", "R"],
                      'Acidic': ["B", "D", "E", "Z"]}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = getattr(row, aa_column)
        peptide_length = len(peptide)

        for group_name, group_aa_values in AA_groups_dict.items():
            count = 0
            for aa in peptide:
                # accumlate number of times the aas appears in the particular group
                count += group_aa_values.count(aa)

            # set the frequency to corresponding columns for each row of the dataframe, column is automatically created if it doesn't exist
            dataframe.loc[row.Index, 'feat_Prop_{}'.format(group_name)] = (count / peptide_length) #* 100

    return dataframe




def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates Frequency of Amino Acid types for given amino acid sequences chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new columns named feat_Prop_{group-value} e.g.  feat_Prop_Tiny, feat_Prop_Small etc.

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
    Calculates Frequency of Amino Acid types for given amino acid sequences

    For each sequence calculates nine features corresponding to the proportion (out of 1) of each Amino Acid type in the sequences

    Results appended as a new columns named feat_Prop_{group-value} e.g.  feat_Prop_Tiny, feat_Prop_Small etc.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """

    return _utils.multiprocessing_return_df(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                            aa_column=aa_column)


