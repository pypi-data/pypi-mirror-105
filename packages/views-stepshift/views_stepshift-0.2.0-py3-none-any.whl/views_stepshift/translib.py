import pandas as pd

def tlag(s: pd.Series, time: int) -> pd.Series:
    """ Time lag """
    if time < 0:
        msg = f"Time below 0 passed to tlag: {time} \n"
        msg += "Call tlead() instead \n"
        raise RuntimeError(msg)

    return s.groupby(level=1).shift(time)

def rollmax(s: pd.Series, window: int) -> pd.Series:
    """ Rolling max """
    # See https://github.com/pandas-dev/pandas/issues/14013
    y = s.groupby(level=1).apply(
        lambda x: x.rolling(window=window, min_periods=0).max()
    )

    return y

def delta(s: pd.Series, time: int = 1) -> pd.Series:
    """ Return the time-delta of s """
    return s - tlag(s, time=time)

def onset_possible(s: pd.Series, window: int) -> pd.Series:
    """Onset possible if no event occured in the preceeding window times """
    # fillna() is so that the first t in a group is always a possible onset
    return (~rollmax(tlag(s, 1).fillna(0), window).astype(bool)).astype(int)

def onset(s: pd.Series, window: int) -> pd.Series:
    """Compute onset

    A row is defined as an onset if
    * onset is possible
    * s is greater than 0
    """
    s_onset_possible = (
        onset_possible(s, window).astype(bool) & s.astype(bool)
    ).astype(int)
    return s_onset_possible
