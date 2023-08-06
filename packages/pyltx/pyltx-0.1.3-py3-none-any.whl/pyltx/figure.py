#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 19:46:52 2021

@author: n7
"""

from . import utils as ut
import os


def incl_image(path, width_ratio=1):
    """
    Generate LaTeX command for including an image in the figure.
    (includegraphics/includesvg)

    Parameters
    ----------
    path : str
        Full path of the image file in the LaTeX project.
    width_ratio : float, optional
        The ratio of the width of image to the width of line-width.
        The default is 1.

    Returns
    -------
    str
        LaTeX command for including an image.

    """
    if (path[-3:] == "svg"):
        cmd = "includesvg"
    else:
        cmd = "includegraphics"
    cmd += "[width=" + str(width_ratio) + r"\linewidth]"
    return ut.tagln(cmd, path)


def fig(filenames, loc="Body/figures", stretch=False,
              pos="h!", caption=None, ref=None):
    """
    Generate LaTeX code for figure.

    Parameters
    ----------
    filenames : str or list
        If str is supplied, the specified image will be added to the figure.
        If list is supplied, all the images in the images will be added to the
        figure.
    loc : str, optional
        Location of the directory containing the figures in the LaTeX project.
        The default is "Body/figures".
    stretch : bool, optional
        Specifies whether the image should be expanded to occupy the entire
        page width in multicolumn layouts. The default is False.
    pos : str, optional
        LaTeX positioning scheme. The default is "h!".
    caption : str or None, optional
        Caption for the figure. If None, the caption will not be added to the
        LaTeX figure code. The default is None.
    ref : str or None, optional
        Label for adding a reference tag to the figure. If None, no label will
        be added. The default is None.

    Returns
    -------
    ltx : str
        LaTeX code for the figure.

    """
    if type(filenames) is str:
        filenames = [filenames]
    tag = "figure"
    if stretch:
        tag += "*"
    pos = "[" + pos + "]"

    width_ratio = round(1/len(filenames), 2) - 0.01
    ltx = ""
    for filename in filenames:
        ltx += incl_image(os.path.join(loc, filename), width_ratio)

    # Encapsulate in "figure" tags
    ltx = ut.encapsln(tag, ltx, pos, True, caption, "bottom", ref)

    return ltx
