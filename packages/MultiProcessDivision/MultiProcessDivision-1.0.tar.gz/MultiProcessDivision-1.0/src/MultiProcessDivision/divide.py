#!/usr/bin/env python3

import numpy as np
import pandas as pd
import multiprocessing as mp


def divide(data, axis=0, series=False, range_setter=None):
    if range_setter is None:
        range_setter = mp.cpu_count()
    l = []
    if float(len(data.index)/range_setter).is_integer() and axis == 0 or series is True:
        """
        solution from:
        https://stackoverflow.com/questions/6239967/determining-whether-an-value-is-a-whole-number-in-python/6239987#6239987
        the index of the resulting dataframe must be shorter than the original index, since these are the passed 
        values of an apply function
        """
        if axis == 0 or series is True:
            chunklength = len(data.index)/range_setter
        elif axis == 1:
            chunklength = len(data.columns)/range_setter
        else:
            return None
        for x in range(range_setter):
            # these are the batches, which are supposedly supplied to the processing queue
            if x == 0:
                start = np.int64(x * chunklength)
                """
                Since the control number starts with 0, the first batch of rows also starts at 
                index 0
                """
            else:
                start = np.int64(x * chunklength) - 1
            stop = np.int64((x + 1) * chunklength - 1)
            """
            The -1 at the end is necessary to avoid multiple processing of the same set and 
            to avoid index errors in the final batch, when the length is too long otherwise.
            Since the basic laws of math also apply here, the multiplication is executed prior 
            to the subtraction.
            """
            if axis == 0 and series is False:
                l.append(data.iloc[start:stop,:])
            elif axis == 1 and series is False:
                l.append(data.iloc[:,start:stop])
            elif axis == 0 and series is True:
                l.append(data.iloc[start:stop])
            else:
                return None
    else:
        if axis == 0:
            chunklength = np.ceil(len(data.index)/range_setter)
            """
            The chunklength is set to be longer than actually required, thus allowing all chunks
            to be filled in the following loop under the first condition and only the last chunk
            to be shorter, when compared to the other chunks. Using the np.ceil() function allows 
            clear determination, which outcome will occur while processing of datasets, which differs
            from only converting to np.int, which does not safeguard which direction the conversion 
            will take.
            """
        elif axis == 1:
            chunklength = np.ceil(len(data.columns)/range_setter)
        for x in range(range_setter):
            if len(l) < range_setter - 1:
                if x == 0:
                    start = np.int64(x * chunklength)
                else:
                    start = np.int64(x * chunklength) - 1
                stop = np.int64((x + 1) * chunklength - 1)
            else:
                start = np.int64(x * chunklength)
                stop = len(data.index)
                # only refers to the last row of the dataset, since the previously used 
                # value -1 included only the second last value, I resorted to the lenght
                # of the index, which is used to determine the range to select.
                # The idea was proposed in the following stackoverflow post:
                # https://stackoverflow.com/questions/54409477/selecting-numpy-array-range-including-the-last-element/54415268#54415268
            if axis == 0 and series is False:
                l.append(data.iloc[start:stop,:])
            elif axis == 1 and series is False:
                l.append(data.iloc[:,start:stop])
            elif axis == 0 and series is True:
                l.append(data.iloc[start:stop])
            else:
                return None
    return l
