#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:25:51 2021

@author: danish
"""
import pandas as pd
import numpy as np


def ease_of_movement(price_data, volume):
    high_price = price_data['<high>']
    low_price = price_data['<low>']
    distance_moved = (high_price + low_price - high_price.shift(1) - low_price.shift(1))/2
    box_ratio = (volume / 1000) / (high_price - low_price)
    return (distance_moved/box_ratio).to_numpy()
