#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 02:33:15 2021

@author: danish
"""
import pandas as pd
import numpy as np


def atr(price_data, n=14):
    price_data = price_data['<close>']
    high_price, low_price, close_price = price_data['<high>'], price_data['<low>'], price_data['<close>']
    tr = np.amax(np.vstack(((high_price - low_price).to_numpy(), (abs(high_price - close_price)).to_numpy(), (abs(low_price - close_price)).to_numpy())).T, axis=1)
    return pd.Series(tr).rolling(n).mean().to_numpy()

