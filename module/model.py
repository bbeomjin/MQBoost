from typing import List, Union, Dict, Any

import numpy as np
import pandas as pd
import lightgbm as lgb
import xgboost as xgb

from module.abstract import MonotoneQuantileRegressor


class QuantileRegressorLgb(MonotoneQuantileRegressor):
    """
    Monotone quantile regressor which preserving monotonicity among quantiles
    Attributes
    ----------
    x: Union[pd.DataFrame, pd.Series, np.ndarray]
    y: Union[pd.Series, np.ndarray]
    alphas: Union[List[float], float]
    _model_name: str = "lightgbm"

    Methods
    -------
    train
    predict
    """

    def __init__(
        self,
        x: Union[pd.DataFrame, pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        alphas: Union[List[float], float],
        _model_name: str = "lightgbm",
    ):
        super().__init__(
            x=x,
            y=y,
            alphas=alphas,
            _model_name=_model_name,
        )

    def train(self, params: Dict[str, Any]) -> lgb.basic.Booster:
        """
        Train regressor and return model
        Args:
            params (Dict[str, Any]): params of lgb

        Returns:
            lgb.basic.Booster
        """
        super().train(params=params)
        self._params.update({"objective": self.fobj})
        self.model = lgb.train(
            train_set=self.dataset,
            params=self._params,
            feval=self.feval,
        )
        return self.model

    def predict(
        self,
        x: Union[pd.DataFrame, pd.Series, np.ndarray],
        alphas: Union[List[float], float],
    ) -> np.ndarray:
        """
        Predict x with alphas
        Args:
            x (Union[pd.DataFrame, pd.Series, np.ndarray])
            alphas (Union[List[float], float])

        Returns:
            np.ndarray
        """
        return super().predict(x=x, alphas=alphas)


class QuantileRegressorXgb(MonotoneQuantileRegressor):
    """
    Monotone quantile regressor which preserving monotonicity among quantiles
    Attributes
    ----------
    x: Union[pd.DataFrame, pd.Series, np.ndarray]
    y: Union[pd.Series, np.ndarray]
    alphas: Union[List[float], float]
    _model_name: str = "xgboost"

    Methods
    -------
    train
    predict
    """

    def __init__(
        self,
        x: Union[pd.DataFrame, pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        alphas: Union[List[float], float],
        _model_name: str = "xgboost",
    ):
        super().__init__(
            x=x,
            y=y,
            alphas=alphas,
            _model_name=_model_name,
        )

    def train(self, params: Dict[str, Any]) -> xgb.Booster:
        """
        Train regressor and return model
        Args:
            params (Dict[str, Any]): params of xgb

        Returns:
            xgb.Booster
        """
        super().train(params=params)
        self.model = xgb.train(
            dtrain=self.dataset,
            verbose_eval=False,
            params=self._params,
            obj=self.fobj,
        )
        return self.model

    def predict(
        self,
        x: Union[pd.DataFrame, pd.Series, np.ndarray],
        alphas: Union[List[float], float],
    ) -> np.ndarray:
        """
        Predict x with alphas
        Args:
            x (Union[pd.DataFrame, pd.Series, np.ndarray])
            alphas (Union[List[float], float])

        Returns:
            np.ndarray
        """
        return super().predict(x=x, alphas=alphas)