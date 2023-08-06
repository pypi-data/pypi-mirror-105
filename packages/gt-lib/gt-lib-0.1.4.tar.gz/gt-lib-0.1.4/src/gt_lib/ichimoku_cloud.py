#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:32:29 2021

@author: danish
"""
import pandas as pd
import numpy as np


def ichimoku_cloud(high_price, low_price, close_price, conversion_line_period=9, base_line_period=26, leading_span_b_period=52):
    conversion_line_period = abs(conversion_line_period)
    base_line_period = abs(base_line_period)
    leading_span_b_period = abs(leading_span_b_period)
    conversion_line = (high_price.rolling(conversion_line_period).max() + low_price.rolling(conversion_line_period).min()) / 2
    base_line = (high_price.rolling(base_line_period).max() + low_price.rolling(base_line_period).min()) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (high_price.rolling(leading_span_b_period).max() + low_price.rolling(leading_span_b_period).min()) / 2
    return conversion_line, base_line, leading_span_a, leading_span_b
