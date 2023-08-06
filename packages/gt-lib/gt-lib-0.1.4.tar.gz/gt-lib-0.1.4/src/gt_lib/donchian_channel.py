#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:27:42 2021

@author: danish
"""
import pandas as pd
import numpy as np


def donchian_channel(high_price, low_price, n=14):
    n = abs(n)
    uc = high_price.rolling(14).max()
    lc = low_price.rolling(14).min()
    mc = ((uc+lc)/2).to_numpy()
    return uc.to_numpy(), mc, lc.to_numpy()