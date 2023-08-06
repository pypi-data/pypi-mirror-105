""" Common data utilities """
from typing import List, Union
import functools
import logging

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

log = logging.getLogger(__name__)


def resample(
    df: pd.DataFrame,
    cols: List[str],
    share_positives: float,
    share_negatives: float,
    threshold=0,
):
    """ Resample a dataframe with respect to cols

    Resampling is a technique for changing the positive/negative balance
    of a dataframe. Positives are rows where any of the specified cols
    are greater than the threshold. Useful for highly unbalanced
    datasets where positive outcomes are rare.

    """
    # If both shares are 1 just return the unaltered df
    if share_positives == 1 and share_negatives == 1:
        return df

    # Negatives are rows where all cols are close to zero
    mask_negatives = np.isclose(df[cols], threshold).max(axis=1)
    # Positives are all the others
    mask_positives = ~mask_negatives

    df_positives = df.loc[mask_positives]
    df_negatives = df.loc[mask_negatives]

    len_positives = len(df_positives)
    len_negatives = len(df_negatives)

    n_positives_wanted = int(share_positives * len_positives)
    n_negatives_wanted = int(share_negatives * len_negatives)

    replacement_pos = share_positives > 1
    replacement_neg = share_negatives > 1
    df = pd.concat(
        [
            df_positives.sample(n=n_positives_wanted, replace=replacement_pos),
            df_negatives.sample(n=n_negatives_wanted, replace=replacement_neg),
        ]
    )
    return df


def check_has_multiindex(data: Union[pd.Series, pd.DataFrame]) -> None:
    """ Raise RuntimeError if Series s doesn't have MultiIndex """
    if not isinstance(data.index, pd.MultiIndex):
        msg = (
            "Data is lacking a multiindex that was expected."
            "Set the index with df.set_index([timevar, groupvar])."
        )
        raise RuntimeError(msg)


def balance_panel_last_t(df: pd.DataFrame) -> pd.DataFrame:
    """ Balance a multiindexed dataframe panel.

    The balanced index has observations for all groups present at the
    last t.
    Assumens df is indexed with timevar as index level 0, and groupvar
    at index level 1.

    Args:
        df: Dataframe with multiindex to balance
    Returns:
        df: A reindexed dataframe
    """
    log.debug(f"Balancing index of panel with shape {df.shape}")
    check_has_multiindex(df)

    # Reset the index to actual values,
    # Needed in case data has been subseted with .loc before
    # If this isn't done, df.index.levels[0].max() gets the
    # pre-subsetting max
    df = df.reset_index().set_index(df.index.names).sort_index()

    return df.reindex(
        pd.MultiIndex.from_product(
            [
                df.index.levels[0].unique(),
                df.loc[df.index.levels[0].max()].index.unique(),
            ],
            names=df.index.names,
        )
    ).sort_index()


def assign_into_df(df_to: pd.DataFrame, df_from: pd.DataFrame) -> pd.DataFrame:
    """ Assign all columns from df_from into df_to

    Only assigns non-missing values from df_from, meaning the
    same column can be inserted multiple times and values be
    retained if the row coverage is different between calls.
    So a df_a with col_a covering months 100-110 and df_b with col_a covering
    months 111-120 could be assigned into a single df which would get
    values of col_a for months 100 - 120.
    """

    for col in df_from:
        log.debug(f"Inserting col {col}")
        # Get a Series of the col for all rows
        s = df_from.loc[:, col]
        
        # Get the "is not null" boolean series to use as mask, ~ is NOT
        mask = ~s.isnull()

        # Get the index from that mask,
        # ix is now index labels of rows with (not missing) data
        ix = s.loc[mask].index
        try:
            df_to.loc[ix, col] = s.loc[ix]
        # Handle KeyError when assigning into a df without all times or locations
        except KeyError:
            try:
                # Only assign ix positions that exist in df_to
                ix = pd.MultiIndex.from_tuples(
                    [tup for tup in ix if tup in df_to.index]
                )
                df_to.loc[ix, col] = s.loc[ix]
            # If it still doesn't work we've got no ix in common.
            except TypeError as exc:
                raise TypeError("No index positions in common.")

    return df_to


def rebuild_index(data: pd.DataFrame) -> pd.DataFrame:
    """ Rebuild the index of the dataframe

    Sometimes we construct new dataframes from old ones or subset
    dataframes by time. The contents of the df.index of the new
    dataframes then still contain the full set of values from the old
    df. This function rebuilds the index to only have the actual
    values with rows.
    """
    check_has_multiindex(data)
    return data.reset_index().set_index(data.index.names).sort_index()


def check_s_binary(s: pd.Series) -> None:
    """ Check that s only contains valueus 0 and 1 """
    log.debug(f"Checking that s named {s.name} is binary")
    unique_values = s.unique()
    error = RuntimeError(
        f"Series {s.name} expected to be binary [0, 1] only, has values {unique_values}"
    )
    if not len(unique_values) == 2:
        raise error
    elif not all([val in [0, 1] for val in unique_values]):
        raise error


def merge_dfs(dfs: List[pd.DataFrame], how="inner"):
    """ Merge a list of dataframes in a reduce pattern """

    return functools.reduce(
        lambda left, right: pd.merge(
            left, right, left_index=True, right_index=True, how=how
        ),
        dfs,
    )


def check_mixed_dtypes(data: pd.DataFrame) -> None:
    """ Check if there are any mixed datatypes overlooked """
    log.debug(f"Checking for mixed dtypes in df")
    mixed_cols = []
    for col in data.columns:
        mixed = (
            data[[col]].applymap(type) != data[[col]].iloc[0].apply(type)
        ).any(axis=1)
        if len(data[mixed]) > 0:
            mixed_cols.append(col)

    if len(mixed_cols) > 0:
        raise RuntimeError(f"Dataframe contains mixed dtypes in {mixed_cols}")
