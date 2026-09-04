import statistics

class Calculate_mean:
    """
    This is the main class, it provides a Statistical calculation of mean, median,
    mode, standard deviation and variation for data analysis. All methods handle
    cases (empty data, insufficient samples) sufficiently.
    """
    @staticmethod
    def mean_value(inputs):
        """
        This is a Static method that takes only one parameter, Calculate the arithmetic mean
        (average) of a data file. we use the mean to aggregate multiple track features into a
        single artist profile,providing a representative vector for similarity calculations.
        Returns Mean value (float), or 0.0 if data is empty.
        """
        if not inputs:
            return 0.0
        try:
            return float(statistics.mean(inputs))
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def median_value(inputs):
        """
        This is a Static method that takes only one parameter, Calculate the median
        (middle value) of a data file. the median provides a more stable central
        value that better represents typical artist characteristics.
        Returns Median value (float), or 0.0 if data is empty.
        """
        if not inputs:
            return 0.0
        try:
            return float(statistics.median(inputs))
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def mode_value(inputs):
        """
        This is a Static method that takes only one parameter,Calculate the mode
        (most frequent value) of a data file. the mode can reveal dominant characteristics.
        Useful for identifying common patterns in artist feature distributions.
        Returns Mode value, first value if no unique mode, or 0.0 if data is empty
        """
        if not inputs:
            return 0
        try:
            return statistics.mode(inputs)
        except statistics.StatisticsError:
            return inputs[0] if inputs else 0  # If no unique mode, return first value as fallback
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def the_standard_deviation(inputs):
        """
        This is a Static method that takes only one parameter,Calculate the sample
        standard deviation of a data file.
        Returns Standard deviation (float), or 0.0 if insufficient data.
        """
        if len(inputs) < 2:
            return 0.0
        try:
            return float(statistics.stdev(inputs))
        except (TypeError, ValueError, statistics.StatisticsError):
            return 0.0

    @staticmethod
    def the_variance(inputs):
        """
        This is a Static method that takes only one parameter,Calculate the sample
        variance of a data file.
        Returns Variance (float), or 0.0 if insufficient data.
        """
        if len(inputs) < 2:
            return 0.0
        try:
            return float(statistics.variance(inputs))
        except (TypeError, ValueError, statistics.StatisticsError):
            return 0.0

    @staticmethod
    def min_value(inputs):
        """
        This is a Static method that takes only one parameter, Find the minimum value
        in a data file.
        Returns Minimum value, or 0.0 if data is empty.
        """
        if not inputs:
            return 0
        try:
            return min(inputs)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def max_value(inputs):
        """
        This is a Static method that takes only one parameter, Find the maximum
        value in a data file.
        Returns Maximum value, or 0.0 if data is empty.
        """
        if not inputs:
            return 0
        try:
            return max(inputs)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def range_value(inputs):
        """
        This is a Static method that takes only one parameter, Calculate the range
        (difference between max and min) of a data file. Wide ranges may indicate diverse
        artist characteristics, affecting similarity calculations.
        Returns Range value, or 0.0 if data is empty.
        """
        if not inputs:
            return 0
        try:
            return max(inputs) - min(inputs)
        except (TypeError, ValueError):
            return 0

    @classmethod
    def all_measures(cls, inputs):
        """
        This is a Class method that takes only one parameter, Calculate all statistical
        measures for a comprehensive data file summary. T0 understanding data distribution
        characteristics, evaluating similarity metric reliability, Justifying metric selection
        based on data properties, providing context for similarity score interpretation.
        Returns Dictionary containing all statistical measures.
        """
        if not inputs:
            return {}

        try:
            return {
                'mean': cls.mean_value(inputs),
                'median': cls.median_value(inputs),
                'mode': cls.mode_value(inputs),
                'std': cls.the_standard_deviation(inputs),
                'var': cls.the_variance(inputs),
                'min': cls.min_value(inputs),
                'max': cls.max_value(inputs),
                'range': cls.range_value(inputs)
            }
        except Exception:
            return {}
