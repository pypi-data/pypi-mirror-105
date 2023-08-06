#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 22:45:08 2021

@author: n7
"""

import os
from . import utils as ut


def sbscr(content):
    """
    Get LaTeX code for displaying the given content in subscript.

    Parameters
    ----------
    content : str
        Content to be displayed in subscript.

    Returns
    -------
    str
        LaTeX code for subscripted content.

    """
    return "_{" + content + "}" if content is not None else ""


def spscr(content):
    """
    Get LaTeX code for displaying the given content in superscript.

    Parameters
    ----------
    content : str
        Content to be displayed in superscript.

    Returns
    -------
    str
        LaTeX code for superscripted content.

    """
    return "^{" + content + "}" if content is not None else ""


def sigma(sb=None, sp=None):
    """
    Generate LaTeX code for summation sign.

    Parameters
    ----------
    sb : str or None, optional
        Subscript content (start condition) for the summation. If None, no
        subscript is added. The default is None.
    sp : str or None, optional
        Superscript content (end condition) for the summation. If None, no
        superscript is added. The default is None.

    Returns
    -------
    str
        LaTeX code for summation sign.

    """
    return r"\sum" + sbscr(sb) + spscr(sp)


def mxm(sb=None):
    """
    Generate LaTeX code for max function.

    Parameters
    ----------
    sb : str or None, optional
        Subscript content (constraint) for max. If None, no
        subscript is added. The default is None.

    Returns
    -------
    str
        LaTeX code for summation sign.

    """
    return r"\max" + sbscr(sb)


def mnm(sb=None):
    """
    Generate LaTeX code for min function.

    Parameters
    ----------
    sb : str or None, optional
        Subscript content (constraint) for the min. If None, no
        subscript is added. The default is None.

    Returns
    -------
    str
        LaTeX code for summation sign.

    """
    return r"\min" + sbscr(sb)


def Pi(sb=None, sp=None):
    """
    Generate LaTeX code for product sign.

    Parameters
    ----------
    sb : str or None, optional
        Subscript content (start condition) for the product. If None, no
        subscript is added. The default is None.
    sp : str or None, optional
        Superscript content (end condition) for the product. If None, no
        superscript is added. The default is None.

    Returns
    -------
    str
        LaTeX code for product sign.

    """
    return r"\Pi" + sbscr(sb) + spscr(sp)


def floor(content):
    """
    Generate LaTeX code for data within floor braces.

    Parameters
    ----------
    content : str
        String to be encapsulated within the floor sign.

    Returns
    -------
    str
        LaTeX code for data within floor braces.

    """
    return ut.tag("floor", content)


def ceil(content):
    """
    Generate LaTeX code for data within ceiling braces.

    Parameters
    ----------
    content : str
        String to be encapsulated within the ceil sign.

    Returns
    -------
    str
        LaTeX code for data within ceiling braces.

    """
    return ut.tag("ceil", content)


def curved(content):
    """
    Generate LaTeX code for data within curved braces.

    Parameters
    ----------
    content : str
        String to be encapsulated within the curved braces.

    Returns
    -------
    str
        LaTeX code for data within curved braces.

    """
    return "(" + content + ")"


def box(content):
    """
    Generate LaTeX code for data within box braces.

    Parameters
    ----------
    content : str
        String to be encapsulated within the box braces.

    Returns
    -------
    str
        LaTeX code for data within box braces.

    """
    return "[" + content + "]"


def curly(content):
    """
    Generate LaTeX code for data within curly braces.

    Parameters
    ----------
    content : str
        String to be encapsulated within the curly braces.

    Returns
    -------
    str
        LaTeX code for data within curly braces.

    """
    return "\\{" + content + "\\}"


def frac(n, d):
    """
    Generate LaTeX fraction.

    Parameters
    ----------
    n : str
        Numerator for the fraction.
    d : str
        Denominator for the fraction.

    Returns
    -------
    str
        LaTeX code for fraction.

    """
    return ut.tag("frac", n, d)


def times(a, b):
    """
    Generate LaTeX code for multiplication.

    Parameters
    ----------
    a : str
        First operand of multiplication.
    b : str
        Second operand of multiplication.

    Returns
    -------
    str
        LaTeX code for multiplication.

    """
    return a + r" \times " + b


def eqn(eq, caption=None, ref=None, tag=False):
    """
    Generate LaTeX code for equation.

    Parameters
    ----------
    eq : str
        Content to be encapsulated in the equation tags.
    caption : str or None, optional
        Caption for the equation. If None, the caption will not be added to the
        LaTeX equation code. The default is None.
    ref : str or None, optional
        Label for adding a reference tag to the equation. If None, no label
        will be added. The default is None.
    tag : bool, optional
        Specifies whether equation number should be added.

    Returns
    -------
    str
        LaTeX code for the equation.

    """
    if tag is False:
        eq += r" \notag"
    return ut.encapsln("equation", eq + os.linesep, None, False, caption,
                       "bottom", ref)


def align(eqs, caption=None, ref=None, tag=False):
    """
    Generate LaTeX code for align environment.

    Parameters
    ----------
    eqs: list
        List of equations to be included in the align environment.
    caption : str or None, optional
        Caption for the align environment. If None, the caption will not be
        added to the LaTeX align code. The default is None.
    ref : str or None, optional
        Label for adding a reference tag to the align environment. If None,
        no label will be added. The default is None.
    tag : bool, optional
        Specifies whether equation numbers should be added.

    Returns
    -------
    str
        LaTeX align environment.

    """
    signs = ["=", "<", ">", r"\leq", r"\geq"]
    line_end = " " + (r"\notag" if tag is False else "") + r"\\" + os.linesep
    ltx = ""
    for eq in eqs:
        sign_pts = [eq.find(sign) for sign in signs]
        break_pt = min([pt for pt in sign_pts if pt >= 0])
        ltx += (eq[:break_pt] + "&" + eq[break_pt:] + line_end)
    ltx = "".join(ltx.rsplit(r"\\", 1))
    return ut.encapsln("align", ltx, None, False, caption, "bottom", ref)


def inline(content):
    """
    Generate LaTeX code for inline math content.

    Parameters
    ----------
    content : str
        String to be encapsulated within the $ sign.

    Returns
    -------
    str
        LaTeX code for inline math.

    """
    return "$" + content + "$"
