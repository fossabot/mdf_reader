import pandas as pd
import numpy as np

from .. import properties


# 1. dtype must be defined in dtype_properties.data_types
#>>> if not np.dtype('int8'):
#...     print('No data type')
#...
#>>> if not np.dtype('int786'):
#...     print('No data type')
#...
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#TypeError: data type "int786" not understood
#
#   Watch this, for my objects I want to catch both empty and blank strings as missing
#   empty_string = ''
#   blank_string = '     '
#   len(empty_string) == 0
#   len(blank_string) != 0
#   len(empty_string) == len(blank_string.lstrip()) == 0
#   So, we'll eval: len(value.lstrip())
#
# return data.astype(self.dtype, casting = 'safe')
# safe casting specifies, otherwise converts np.nan to some real number depending on dtype.



class df_converters():
    def __init__(self, dtype):
        self.dtype = dtype
        self.numeric_scale = 1. if self.dtype in properties.numpy_floats else 1
        self.numeric_offset = 0. if self.dtype in properties.numpy_floats else 0
    def object_to_numeric(self, data, scale = None, offset = None):
        
        scale = scale if scale else self.numeric_scale
        offset = offset if offset else self.numeric_offset
        # First do the appropriate managing of white spaces, to the right, they mean 0!
        data = data.replace(r'^\s*$', np.nan, regex=True)
        data = data.str.replace(' ', '0')
        #  Convert to numeric, then scale (?!) and give it's actual int type
        data = pd.to_numeric(data,errors = 'coerce') # astype fails on strings, to_numeric manages errors....!
        data = offset + data * scale
        try:
            return data.astype(self.dtype, casting = 'safe')
        except:
            return data

    def object_to_object(self,data,disable_white_strip = False):
        # With strip() an empty element after stripping, is just an empty element, no NaN...
        if not disable_white_strip:
            return data.str.strip()
        else:
            if disable_white_strip == 'l':
                return data.str.rstrip()
            elif disable_white_strip == 'r':
                return data.str.lstrip()
            else:
                return data

    def object_to_datetime(self,data, datetime_format = "%Y%m%d"):
        data = pd.to_datetime(data, format = datetime_format, errors = 'coerce')
        return data

converters = dict()
for dtype in properties.numeric_types:
    converters[dtype] = df_converters(dtype).object_to_numeric
converters['datetime'] = df_converters('datetime').object_to_datetime
converters['str'] = df_converters('str').object_to_object
converters['object'] = df_converters('object').object_to_object
converters['key'] = df_converters('key').object_to_object
