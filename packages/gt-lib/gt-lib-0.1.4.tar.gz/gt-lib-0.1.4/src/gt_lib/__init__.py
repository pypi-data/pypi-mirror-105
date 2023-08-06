from gt_lib.ema import ema
from gt_lib.sma import sma
from gt_lib.period_high import n_period_high
from gt_lib.period_low import n_period_low
from gt_lib.ema_crossover import ema_crossover
from gt_lib.volatility import volatility
from gt_lib.bollinger_band import bollinger_band
from gt_lib.macd import macd
from gt_lib.reversal import reversal
from gt_lib.rsi import rsi
from gt_lib.atr import atr
from gt_lib.trailing_stop_loss import t_stop_loss
from gt_lib.double_ema import double_ema
from gt_lib.money_flow_index import mfi
from gt_lib.fractal import fractal
from gt_lib.ease_of_movement import ease_of_movement
from gt_lib.donchian_channel import donchian_channel
from gt_lib.stochastic_rsi import stochastic_rsi
from gt_lib.weighted_moving_average import wma
from gt_lib.hull_moving_avg import hull_moving_avg
from gt_lib.ichimoku_cloud import ichimoku_cloud

input_mapping_dict = {
                    'ema': ['<close>'],
                    'sma': ['<close>'],
                    'n_period_high': ['<high>'],
                    'n_period_low': ['<low>'],
                    'ema_crossover': ['<close>'],
                    'volatility': ['<close>'],
                    'bollinger_band': ['<close>'],
                    'macd': ['<close>'],
                    'reversal': ['<close>', '<open>'],
                    'rsi': ['<high>', '<low>', '<close>'],
                    't_stop_loss': ['<close>'],
                    'double_ema': ['<close>'],
                    'mfi': ['<high>', '<low>', '<close>', '<volume>'],
                    'fractal': ['<high>', '<low>'],
                    'ease_of_movement': ['<high>', '<low>', '<volume>'],
                    'donchian_channel': ['<high>', '<low>'],
                    'stochastic_rsi': ['<close>'],
                    'wma': ['<close>'],
                    'hull_moving_avg': ['<close>'],
                    'ichimoku_cloud': ['<high>', '<low>', '<close>'],
                      }
                      
output_mapping_dict = {
                    'bollinger_band': ['upper', 'mean', 'low'],
                    'donchian_channel': ['upper', 'mean', 'low'],
                    'fractla': ['bearish', 'bullish'],
                    'ichimoku_cloud': ['conv', 'base', 'span_a', 'span_b'],
                    'macd': ['macd', 'signal', 'hist']
                      }

