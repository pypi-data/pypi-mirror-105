#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:29:08 2021

@author: danish
"""
import pandas as pd
import numpy as np
from gt_lib.rsi import rsi


def stochastic_rsi(price_data, n=14):
    n = abs(n)
    rsi_data = rsi(price_data)
    period_max_rsi = rsi_data.rolling(n).max()
    period_min_rsi = rsi_data.rolling(n).min()
    return (rsi - period_min_rsi) / (period_max_rsi - period_min_rsi)
