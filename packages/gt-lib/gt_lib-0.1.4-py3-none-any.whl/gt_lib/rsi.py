#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 01:37:25 2021

@author: danish
"""
import pandas as pd
import numpy as np


def gain(x):
    return ((x > 0) * x).sum()


def loss(x):
    return ((x < 0) * x).sum()


def rsi(price_data, n):
    n = abs(n)
    pct_chang = price_data.pct_change()
    avg_gain = pct_chang.rolling(n).apply(gain, raw=True)
    avg_loss = pct_chang.rolling(n).apply(loss, raw=True)
    return (100 - (100/(1+(avg_gain/avg_loss)))).to_numpy()
