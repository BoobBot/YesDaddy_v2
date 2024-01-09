import numpy as np


def levenshtein_distance(s: str, t: str, ratio_calc: bool = False) -> int:
    """
    Calculates the distance between two strings.

    Parameters
    ----------
    s: str
        The string to compare.
    t: str
        The string being compared against.
    ratio_calc: bool
        Whether to compute the levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t

    Returns
    -------
    int
        The distance between the two strings.
    """
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype = int)

    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 2 if ratio_calc else 1

            distance[row][col] = min(distance[row - 1][col] + 1, distance[row][col - 1] + 1, distance[row - 1][col - 1] + cost)

    if ratio_calc:
        return ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))

    return distance[row][col]
