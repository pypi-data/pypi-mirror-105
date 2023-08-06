from typing import List, Tuple

import pandas as pd

from model_quality_report.quality_report.base import QualityReportBase, QualityReportType
from model_quality_report.quality_report.quality_report_error import QualityReportError

ExperimentKeyType = dict
ModelComparisonReportType = List[Tuple[ExperimentKeyType, QualityReportType]]


class ModelComparisonReport:
    """Model comparison report.

    It takes four lists of equal size: `QualityReportBase` instances, `X_data_list`, `y_data_list`,
    and flat dictionaries `experiment_keys`. The class now has only two public methods:
      - `create_reports` that simply returns the list quality reports for each experiment, and
      - `get_metrics` that extracts a single metrics DataFrame from multiple quality reports obtained above.
       The resulting DataFrame has experiment keys in corresponding columns.
    """

    lbl_metrics = QualityReportBase.lbl_metrics
    lbl_metric_value = QualityReportBase.lbl_metric_value
    lbl_experiment_key = "experiment_key"

    def __init__(
        self,
        quality_reports: List[QualityReportBase],
        X_data_list: List[pd.DataFrame],
        y_data_list: List[pd.Series],
        experiment_keys: List[ExperimentKeyType],
    ) -> None:
        """

        :param quality_reports: list of `QualityReportBase` instances
        that would produce a quality report for each experiment.
        :param X_data_list: list of X data
        :param y_data_list: list of y data
        :param experiment_keys: list of flat dictionaries that provide a description for each experiment
        """
        self._quality_reports = quality_reports
        self._X_data_list = X_data_list
        self._y_data_list = y_data_list
        self._experiment_keys = experiment_keys
        self._errors = QualityReportError()

    def create_reports(self) -> ModelComparisonReportType:
        """
        Given a list of experiments compute quality reports for each and combine them in one dictionary.

        :return: dict containing the quality report
        """
        results = list()
        experiments = zip(self._experiment_keys, self._quality_reports, self._X_data_list, self._y_data_list)
        for experiment_key, quality_report, X, y in experiments:
            results.append((experiment_key, quality_report.create_quality_report(X=X, y=y)))
        return results

    def get_metrics(self, reports: ModelComparisonReportType) -> pd.DataFrame:
        """Convert quality reports (only metrics part) into a single DataFrame.

        :return: DataFrame containing metric values for each experiment

        Example output
        --------------
                            metrics     value  model  exogenous
        0  explained_variance_score  0.949841  Model1      a, b
        1                      mape  0.177778  Model1      a, b
        2       mean_absolute_error  1.000000  Model1      a, b
        3        mean_squared_error  1.240000  Model1      a, b
        4     median_absolute_error  1.000000  Model1      a, b
        5                  r2_score  0.911429  Model1      a, b
        0  explained_variance_score  0.992172  Model2         a
        1                      mape  0.187302  Model2         a
        2       mean_absolute_error  0.952381  Model2         a
        3        mean_squared_error  1.142857  Model2         a
        4     median_absolute_error  1.142857  Model2         a
        5                  r2_score  0.992172  Model2         a
        0  explained_variance_score  0.973807  Model3         b
        1                      mape  0.158055  Model3         b
        2       mean_absolute_error  0.861451  Model3         b
        3        mean_squared_error  0.957465  Model3         b
        4     median_absolute_error  0.577017  Model3         b
        5                  r2_score  0.883552  Model3         b

        """
        results = list()
        for quality_report_instance, quality_report in zip(self._quality_reports, reports):
            report_df = quality_report_instance.get_metrics(report=quality_report[1]).assign(**quality_report[0])
            results.append(report_df)
        return pd.concat(results)
