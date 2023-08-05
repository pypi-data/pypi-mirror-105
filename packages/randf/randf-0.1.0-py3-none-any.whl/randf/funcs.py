# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2021 Manoel Elpidio Pereira de Queiroz Filho.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from decimal import Decimal, localcontext

import numpy as np
import pandas as pd

def randec(order, prec=8, size=None):
    '''
    A function to generate random decimal numbers, given `order` and
    `prec`.

    Parameters
    ----------
    order : int
        Order of magnitude of the decimal to be generated (e.g., 100
        will output a decimal between 0 incluse and 101 exclusive).
    prec : int, default 8
        Precision of the output decimal number.
    size : int or tuple of ints, optional
        Output shape, accepting integers or a tuple of 2 integers. In
        case of a single integer ``m`` provided, outputs a NumPy ndarray
        of length ``m``. In case of a ``(m, n)`` tuple provided, outputs
        a NumPy ndarray with ``m * n`` values. The default value is
        None, which outputs a single `decimal.Decimal` object.

    Returns
    -------
        decimal.Decimal or numpy.ndarray of decimal.Decimal.
    '''

    if isinstance(order, int):
        if order <= 0:
            raise ValueError('Order can not be null or negative')
        inteiro = range(len(str(order)))
    else:
        raise TypeError(f"Order parameter does not accept {type(order)}")
    if size is None:
        size = 1

    def sing():
        rs = ''
        for _ in inteiro:
            rs += str(np.random.randint(10))
        rs += '.'
        for _ in range(prec):
            rs += str(np.random.randint(10))

        with localcontext() as ctx:
            ctx.prec = prec
            d = +Decimal(rs)

        return d

    def check_size(n):
        if n <= 0:
            raise ValueError('Size can not be null or negative')

    if isinstance(size, int):
        check_size(size)

        if size == 1:
            return sing()
        else:
            ls = [sing() for i in range(size)]

            return np.array(ls)
    elif isinstance(size, tuple) and len(size) == 2:
        for e in size:
            check_size(e)
        ls = [[sing() for j in range(size[1])] for i in range(size[0])]

        return np.array(ls)
    else:
        raise TypeError(f"Size parameter does not accept {type(size)}")

def randf(rows, cols, ntype='rand', order=100, dcols=None, names=None):
    '''
    A function to generate a pandas DataFrame with random numbers.

    Parameters
    ----------
    rows : int
        Number of rows in the DataFrame.
    cols : int
        Number of numerical columns in the DataFrame.
    ntype : {'decimal', 'int', 'float', 'rand'}, default 'rand'.
        Number type of numerical columns output.

        * decimal: uses the `randec` function to create columns of
        `decimal.Decimal`, stored as `object` in pandas.
        * int: uses the `numpy.random.randint` function to create
          columns of `numpy.int32`.
        * float: combines `numpy.random.rand` and `numpy.random.randint`
          with the provided `order` argumento to generate random floats
          that can be greater than 1.
        * rand: uses the `numpy.random.rand` function to create columns
          of `np.float64` type between 0 and 1 inclusive.
    order : int, default 100
        The order of magnitude for output numbers. In case of type
        'decimal' provided, uses as the order argument in the `randec`
        function. For all others except 'rand', uses as the upper bound
        of the NumPy random functions. If order provided is 2 and nytpe
        is 'int', will produce a boolean DataFrame.
    dcols : dict or array-like, optional
        Additional discrete columns (classes) to include. In case of a
        dictionary of sequences, such as lists, tuples and NumPy
        ndarrays (integers will also work), uses the
        `numpy.random.choice` function to create classes named after the
        dictionary's keys. In case of a single sequence provided,
        creates a single column named 'class'. In case of a string
        provided, its characters are converted to a sequence to create
        the 'class' column. All classes are presented to the left of the
        generated DataFrame.
    names : array-like, optional
        Sequence containing the custom names of the numerical columns.
        Will raise an error if `len(names) != cols` and must be provided
        for random DataFrames with 27 numerical columns or more.

    Returns
    -------
        pandas.DataFrame
    '''

    if names is None:
        if cols > 26:
            raise ValueError('To generate more than 26 columns, names must be '
                             'provided')

        names = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()\
            [:cols]
    elif isinstance(names, str):
        names = list(names.replace(' ', ''))

    if len(names) != cols:
        raise ValueError('Names and size must be of equal length')

    if ntype == 'decimal':
        base = randec(order, size=(rows, cols))
    elif ntype == 'int':
        base = np.random.randint(order, size=(rows, cols))
        if order == 2:
            base = base.astype(bool)
    elif ntype == 'float':
        base = np.random.rand(rows, cols)\
            + np.random.randint(order, size=(rows, cols))
    elif ntype == 'rand':
        base = np.random.rand(rows, cols)
    else:
        raise ValueError(f"{ntype} is not valid for ntype")

    cont = pd.DataFrame(base, columns=names)

    if dcols is not None:
        if isinstance(dcols, dict):
            acols = []
            for k, v in dcols.items():
                acols.append(pd.Series(np.random.choice(v, size=rows), name=k))

            df = pd.concat(acols, axis=1).join(cont)
        else:
            if isinstance(dcols, str):
                dcols = list(dcols.replace(' ', ''))

            df = pd.DataFrame(np.random.choice(dcols, size=rows),
                              columns=['class']).join(cont)
    else:
        df = cont

    return df
