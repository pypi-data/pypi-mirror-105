#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 18:45:27 2021

@author: n7
"""

from . import utils as ut


def bf(content):
    """
    Generate LaTeX code for the bold text.

    Parameters
    ----------
    content : str
        Text to be represented in bold.

    Returns
    -------
    str
        LaTeX bold format code for the given text.

    """
    return ut.tag("textbf", content)


def it(content):
    """
    Generate LaTeX code for the italisized text.

    Parameters
    ----------
    content : str
        Text to be represented in italics.

    Returns
    -------
    str
        LaTeX italicisized format code for the given text.

    """
    return ut.tag("textit", content)


def tt(content):
    """
    Generate LaTeX code for the courier text.

    Parameters
    ----------
    content : str
        Text to be represented in courier.

    Returns
    -------
    str
        LaTeX courier format code for the given text.

    """
    return ut.tag("texttt", content)


def ul(content):
    """
    Generate LaTeX code for the underlined text.

    Parameters
    ----------
    content : str
        Text to be represented with a underline.

    Returns
    -------
    str
        LaTeX underlined format code for the given text.

    """
    return ut.tag("underline", content)
