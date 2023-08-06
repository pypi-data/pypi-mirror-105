import logging
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

log = logging.getLogger(__name__)


@dataclass
class DataSelector:
    """ Data subsetting for Model

    Because we do time shifting there are 4 ways of subsetting data.

    Data can be subset by the temporal alignment of the outcome or the
    features and for training or prediction. All 4 can be used.

    For an onset model, as that is theoretically related to the outcome,
    the parameters col_mask_train_outcome and col_mask_predict_outcome
    should be set to an "onset_possible" column to subset training
    and predictions respectively.

    I can't think of a theoretical case for subsetting on features
    but perhaps a drought or an economic crisis should do the
    subsetting aligned to the features?


    Args:
        col_mask_train_outcome:
        col_mask_train_features:
        col_mask_predict_outcome:
        col_mask_predict_features:

    """

    col_mask_train_outcome: Optional[str] = None
    col_mask_train_features: Optional[str] = None
    col_mask_predict_outcome: Optional[str] = None
    col_mask_predict_features: Optional[str] = None

    @property
    def cols_needed(self) -> List[str]:
        cols_needed = []
        for col in [
            self.col_mask_train_outcome,
            self.col_mask_train_features,
            self.col_mask_predict_outcome,
            self.col_mask_predict_features,
        ]:
            if col:
                cols_needed.append(col)
        return sorted(list(set(cols_needed)))

    def subset_df_train(
        self, df_step: pd.DataFrame, df: pd.DataFrame, step: int
    ) -> pd.DataFrame:

        if self.col_mask_train_outcome:
            log.debug(
                f"Dataselector subsetting by {self.col_mask_train_outcome}"
            )
            s_binary = df[self.col_mask_train_outcome].dropna()
            s_mask = s_binary.astype(bool)
            df_step = df_step.reindex(s_mask.loc[s_mask].index)

        if self.col_mask_train_features:
            log.debug(
                f"Dataselector subsetting by {self.col_mask_train_features}"
            )
            s_binary = (
                df[self.col_mask_train_features]
                .groupby(level=1)
                .shift(step)
                .dropna()
            )
            s_mask = s_binary.astype(bool)
            df_step = df_step.reindex(s_mask.loc[s_mask].index)

        return df_step 

    def subset_s_pred(self, s_pred, df, step) -> pd.Series:

        if self.col_mask_predict_outcome:
            log.debug(
                f"Dataselector subsetting by {self.col_mask_predict_outcome}"
            )
            s_binary = df[self.col_mask_predict_outcome].dropna()
            s_mask = s_binary.astype(bool)

            s_pred = s_pred.loc[s_mask]


        if self.col_mask_predict_features:
            log.debug(
                f"Dataselector subsetting by {self.col_mask_predict_features}"
            )
            s_binary = (
                df.loc[:, self.col_mask_predict_features]
                .groupby(level=1)
                .shift(step)
                .dropna()
            )
            s_mask = s_binary.astype(bool)
            s_pred = s_pred.reindex(s_mask.loc[s_mask].index)

        return s_pred
