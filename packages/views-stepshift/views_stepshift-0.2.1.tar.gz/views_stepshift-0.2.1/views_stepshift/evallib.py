""" Evaluation library. """
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

from sklearn import metrics  # type: ignore

# real
def mean_squared_error(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes MSE given array of actuals and probs."""
    return metrics.mean_squared_error(y_true=actuals, y_pred=preds)


def log_loss(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes the log loss score given array of actuals and probs."""
    return metrics.log_loss(y_true=actuals, y_pred=preds)


def tadda_score(
    y_deltas: pd.Series,
    f_deltas: pd.Series,
    epsilon=0.048,
    smooth_penalty=False,
    element_by_element=False,
) -> float:
    """Computes TADDA given array of y deltas and f deltas.

    Args:
        y_deltas: 1d np.ndarray of length N holding the actual changes.
        f_deltas: 1d np.ndarray of length N holding the forecasted values.
        epsilon: a positive scalar that defines the target around actual values
            where values are "close enough".
        smooth_penalty: when y[i] =/- epsilon(E) crosses 0, there is a jump in
            TADDA. This can be smoothed away by only penalizing directional
            chance by |f-E| (False by default).
        element_by_element: return the mean of the individual contributions if
            False or the vector of individual TADDA values if True (False by
            default).
    Returns:
        scalar if element_by_element is False, and np.array if
            element_by_element is True.
    """

    def sign_not_equal(y_deltas, f_deltas):
        # 0 is treated as both pos and neg: returns 0 (not not equal) when y=0
        y_sign = np.where(y_deltas > 0.0, 1, 0)
        f_sign = np.where(f_deltas > 0.0, 1, 0)
        return np.where((y_sign == f_sign) | (np.equal(y_deltas, 0.0)), 0, 1)

    term1 = np.abs(y_deltas - f_deltas)

    if not smooth_penalty:
        sign_equality = sign_not_equal(y_deltas, f_deltas)
        over_epsilon = np.where(np.abs(y_deltas - f_deltas) > epsilon, 1, 0)
        term2 = np.abs(f_deltas) * sign_equality * over_epsilon
    else:
        cutoff = np.where(
            np.abs(y_deltas) < epsilon, np.abs(np.abs(y_deltas) - epsilon), 0
        )
        sign_equality = sign_not_equal(y_deltas, f_deltas)
        over_epsilon = np.where(np.abs(y_deltas - f_deltas) > epsilon, 1, 0)
        term2 = (
            np.abs(np.abs(f_deltas) - cutoff) * sign_equality * over_epsilon
        )

    return term1 + term2 if element_by_element else (term1 + term2).mean()

# real
def concordance_correlation_coefficient(
    y_true, y_pred, sample_weight=None, multioutput="uniform_average"
):
    """Concordance correlation coefficient.
    The concordance correlation coefficient is a measure of inter-rater agreement.
    It measures the deviation of the relationship between predicted and true values
    from the 45 degree angle.
    Read more: https://en.wikipedia.org/wiki/Concordance_correlation_coefficient
    Original paper: Lawrence, I., and Kuei Lin. "A concordance correlation
    coefficient to evaluate reproducibility." Biometrics (1989): 255-268.
    Parameters
    ----------
    y_true : array-like of shape = (n_samples) or (n_samples, n_outputs)
        Ground truth (correct) target values.
    y_pred : array-like of shape = (n_samples) or (n_samples, n_outputs)
        Estimated target values.
    Returns
    -------
    loss : A float in the range [-1,1]. A value of 1 indicates perfect agreement
    between the true and the predicted values.
    Examples
    --------
    >>> y_true = [3, -0.5, 2, 7]
    >>> y_pred = [2.5, 0.0, 2, 8]
    >>> concordance_correlation_coefficient(y_true, y_pred)
    0.97678916827853024
    """
    cor = np.corrcoef(y_true, y_pred)[0][1]

    mean_true = np.mean(y_true)
    mean_pred = np.mean(y_pred)

    var_true = np.var(y_true)
    var_pred = np.var(y_pred)

    sd_true = np.std(y_true)
    sd_pred = np.std(y_pred)

    numerator = 2 * cor * sd_true * sd_pred

    denominator = var_true + var_pred + (mean_true - mean_pred) ** 2

    return numerator / denominator


# real
def mean_absolute_error(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes MAE given array of actuals and preds."""
    return metrics.mean_absolute_error(y_true=actuals, y_pred=preds)


# real
def r2_score(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes r2 given array of actuals and preds."""
    return metrics.r2_score(y_true=actuals, y_pred=preds)


# prob
def average_precision(actuals: pd.Series, probs: pd.Series) -> float:
    """Computes average precision given array of actuals and probs."""
    return metrics.average_precision_score(y_true=actuals, y_score=probs)


# prob
def area_under_pr(actuals: pd.Series, probs: pd.Series) -> float:
    """Computes AUPR given array of actuals and preds."""
    precision, recall, _ = metrics.precision_recall_curve(actuals, probs)
    return metrics.auc(recall, precision)


# prob
def area_under_roc(actuals: pd.Series, probs: pd.Series) -> float:
    """Computes AUROC given array of actuals and probs."""
    return metrics.roc_auc_score(y_true=actuals, y_score=probs)


# prob
def brier(actuals: pd.Series, probs: pd.Series) -> float:
    """Computes brier score given array of actuals and probs."""
    return metrics.brier_score_loss(y_true=actuals, y_prob=probs)


# bool
def accuracy(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes accuracy from series of actuals and predictions with
    single threshold applied."""
    return metrics.accuracy_score(y_true=actuals, y_pred=preds)


# bool
def precision(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes precision from confusion matrix."""
    return metrics.precision_score(y_true=actuals, y_pred=preds)


# bool
def recall(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes recall from confusion matrix."""
    return metrics.recall_score(y_true=actuals, y_pred=preds)


# bool
def f1_score(actuals: pd.Series, preds: pd.Series) -> float:
    """Computes F1-score given precision and recall."""
    return metrics.f1_score(y_true=actuals, y_pred=preds)


# bool
def class_report(actuals: pd.Series, preds: pd.Series) -> float:
    """Classification report."""
    return metrics.classification_report(y_true=actuals, y_pred=preds)


def confusion_matrix(actuals: pd.Series, preds: pd.Series) -> np.ndarray:
    """Compute a confusion metrix according to a specified threshold."""
    return metrics.confusion_matrix(y_true=actuals, y_pred=preds)


def threshold_cost(
    threshold: float,
    actuals: pd.Series,
    preds: pd.Series,
    cost_matrix: np.ndarray,
) -> float:
    """Compute cost by threshold given a cost matrix."""
    cost_tn, cost_fp, cost_fn, cost_tp = cost_matrix.ravel()
    bin_preds = np.where(preds >= threshold, 1, 0)
    matrix = metrics.confusion_matrix(actuals, bin_preds)
    tn, fp, fn, tp = matrix.ravel()

    # Punish the scores.
    cost = (tp * cost_tp) + (tn * cost_tn) + (fn * cost_fn) + (fp * cost_fp)

    return cost

def optimal_threshold(
    actuals: pd.Series,
    probs: pd.Series,
    cost_matrix: np.ndarray,
    n_steps: int = 1001,
) -> float:
    """Compute the optimal classification threshold given a cost matrix."""
    threshold_space = list((np.linspace(0, 1, n_steps)))
    threshold_costs = {}

    for threshold in threshold_space:
        threshold_costs.update(
            {threshold: threshold_cost(threshold, actuals, probs, cost_matrix)}
        )

    return min(threshold_costs, key=threshold_costs.get)
