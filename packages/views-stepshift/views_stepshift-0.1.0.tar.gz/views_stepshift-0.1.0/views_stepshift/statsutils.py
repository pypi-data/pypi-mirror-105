""" Statistical utils

#@TODO: Figure out numpy / pandas types here
"""
from typing import Any, List
import warnings

import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def prob_to_odds(p: Any, clip=True) -> Any:
    """ Cast probability into odds """

    if isinstance(p, list):
        p = np.array(p)

    if clip:
        offset = 1e-10
        offset = 1e-10
        upper = 1 - offset
        lower = 0 + offset
        p = np.clip(p, lower, upper)

    # Check for probs greq 1 because odds of 1 is inf which might break things
    if np.any(p >= 1):
        msg = "probs >= 1 passed to get_odds, expect infs"
        warnings.warn(msg)

    odds = p / (1 - p)
    return odds


def prob_to_logodds(p: Any) -> Any:
    """ Cast probability to log-odds """
    return np.log(prob_to_odds(p))


def odds_to_prob(odds: Any) -> Any:
    """ Cast odds ratio to probability """
    return odds / (odds + 1)


def logodds_to_prob(logodds: Any) -> Any:
    """ Cast logodds to probability """
    return odds_to_prob(np.exp(logodds))


def combined_exclusive_prob(s_list: List[pd.Series]) -> pd.Series:
    """Cast multiple probability series into one combined probability.

    That is: assuming independence, get the probability of at least one of
    the events occurring.
    """
    # Calculate p of none of the events occurring.
    for i, s in enumerate(s_list):
        # Check if s are probabilities.
        if np.any(s > 1):
            raise RuntimeError(f"Series {s.name} is not a probability (0-1).")
        if i > 0:
            p: float = p * (1 - s)
        else:
            p = 1 - s

    # Return p of at least one event occurring.
    return 1 - p
