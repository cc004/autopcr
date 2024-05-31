import math

def inverse_normal_cdf(p, tolerance=1e-5):
    if p <= 0 or p >= 1:
        raise ValueError("p must be between 0 and 1")

    if p < 0.5:
        return -inverse_normal_cdf(1 - p, tolerance)

    low = 0.0
    high = 10.0
    mid = (low + high) / 2
    while high - low > tolerance:
        mid = (low + high) / 2
        if norm_cdf(mid) < p:
            low = mid
        else:
            high = mid
    
    return mid

def norm_cdf(x):
    return (1 + math.erf(x / math.sqrt(2))) / 2

def wilson_score_interval(successes, total, confidence_level=0.95):
    """
    Calculate the Wilson score interval for a proportion.
    
    Parameters
    ----------
    count : int
        Number of successes.
    nobs : int
        Total number of trials or observations.
    alpha : float, optional
        Significance level (default is 0.05). The default alpha = 0.05 returns a 95% confidence interval.
        
    Returns
    -------
    ci_low : float
        Lower bound of the confidence interval.
    ci_upp : float
        Upper bound of the confidence interval.
    """

    if total == 0:
        return (0, 0)
    
    z = inverse_normal_cdf(1 - (1 - confidence_level) / 2)
    
    phat = successes / total
    denominator = 1 + (z**2 / total)
    centre_adjusted_probability = phat + (z**2 / (2 * total))
    adjusted_standard_deviation = math.sqrt((phat * (1 - phat) + (z**2 / (4 * total))) / total)
    
    lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator
    
    return lower_bound, upper_bound
