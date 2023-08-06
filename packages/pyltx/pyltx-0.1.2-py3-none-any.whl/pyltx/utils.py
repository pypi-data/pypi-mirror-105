#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 17:54:01 2021

@author: n7
"""

import numpy as np
import os


def tag(name, content, arg=None, newline=False):
    """
    Generate LaTeX code for the specified tag name, content and an optional
    additional argument

    Parameters
    ----------
    name : str
        Name of the LaTeX command.
    content : str
        Content to be put inside the command braces.
    arg : str or None, optional
        Additional argument to be added after the command. The default is None.
    newline : bool, optional
        Specifiec whether to add a line-break after the command.
        The default is False.

    Returns
    -------
    str
        LaTeX code for the given command parameters.

    """
    if arg is None:
        arg = ""
    else:
        if not ((arg[0] == "{" and arg[-1] == "}") or
                (arg[0] == "[" and arg[-1] == "]")):
            arg = "{" + arg + "}"
    return ("\\" if name[0] != "\\" else "") + name + "{" + content + "}" + \
        arg + (os.linesep if newline is True else "")


def tagln(name, content, arg=None):
    """
    Generate LaTeX code for the specified tag name, content and an optional
    additional argument with a line-break at the end.

    Parameters
    ----------
    name : str
        Name of the LaTeX command.
    content : str
        Content to be put inside the command braces.
    arg : str or None, optional
        Additional argument to be added after the command. If None, no extra
        argument will be added. The default is None.

    Returns
    -------
    str
        LaTeX code for the given command parameters.

    """
    return tag(name, content, arg, True)


def begin(content, arg=None):
    """
    Generate LaTeX code for the "\begin" tag, and an optional additional
    argument.

    Parameters
    ----------
    content : str
        Content to be put inside the "\begin" command braces.
    arg : str or None, optional
        Additional argument to be added after the "\begin" command. If None,
        no additional argument is used. The default is None.

    Returns
    -------
    str
        LaTeX code for the "\begin" command.

    """
    return tagln("begin", content, arg)


def end(content):
    r"""
    Generate LaTeX code for the "\end" tag.

    Parameters
    ----------
    content : str
        Content to be put inside the "\end" command braces.

    Returns
    -------
    str
        LaTeX code for the "\end" command.

    """
    return tagln("end", content)


def capt(content):
    r"""
    Generate LaTeX caption code.

    Parameters
    ----------
    content : str
        Content to be put inside the "\caption" command braces.

    Returns
    -------
    str
        LaTeX code for the caption.

    """
    return tagln("caption", content)


def label(content):
    r"""
    Generate LaTeX label code.

    Parameters
    ----------
    content : str
        Content to be put inside the "\label" command braces.

    Returns
    -------
    str
        LaTeX code for the label.

    """
    return tagln("label", content)


def inline_math_pts(content):
    """
    Find start and end points of inline math in the given content.

    Parameters
    ----------
    content : str
        Content in which inline math points need to be found.

    Returns
    -------
    numpy.ndarray
        Break-points of inline math in the given content.

    """
    return np.array([i for i in range(0, len(content)) if content[i] == "$"])


def escape(content):
    """
    Replace special characters ("&, "%", "_") in the given string by their
    escape sequences.

    Parameters
    ----------
    content : str
        Content in which special characters need to be replaced.

    Returns
    -------
    content : str
        Content with escape sequences for special characters.

    """
    non_math_pts = np.concatenate([[-1] + inline_math_pts(content) +
                                   [len(content)]]).reshape(-1, 2)
    non_math_pts[:, 0] += 1
    for pts in non_math_pts:
        pre = content[:pts[0]]
        main = content[pts[0]:pts[1]]
        post = content[pts[1]:]
        main = main.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")
        content = pre + main + post
    return content


def encaps(env, content, arg=None, center=False, caption=None,
           capt_pos="bottom", ref=None, addl_newline=False):
    r"""
    Encapsulate the given content within "\begin" and "\end" commands of the
    specified environment.

    Parameters
    ----------
    env : str
        Name of the LaTeX environment in which the content needs to be
        encapsulated.
    content : str
        The LaTeX content to be encapsulated.
    arg : str or None, optional
        Additional argument to be added after the "\begin" command. If None,
        no additional argument is used. The default is None.
    center : bool, optional
        Specifies whether centering should be applied to the environment.
        The default is False.
    caption : str or None, optional
        Caption for the environment. If None, no caption is added.
        The default is None.
    capt_pos : str, optional
        Specifies the position of the caption in the environment. The
        accepted values are "top" and "bottom". The default is "bottom".
    ref : str or None, optional
        Tag for adding a reference label to the table. If None, no label is
        be added. The default is None.
    addl_newline : bool, optional
        Specifies whether to add a line-break after the ending the environment.
        The default is False.

    Returns
    -------
    ltx : str
        LaTeX code for the given environment parameters.

    """
    prefix = begin(env, arg) + \
        (("\\centering" + os.linesep) if center is True else "")
    suffix = (label(env + ":" + ref) if ref is not None else "") + end(env)
    if caption is not None:
        if (capt_pos == "top"):
            prefix += capt(caption)
        elif (capt_pos == "bottom"):
            suffix = capt(caption) + suffix
    if addl_newline:
        suffix += "\n"
    ltx = prefix + content + suffix
    return ltx


def encapsln(env, content, arg=None, center=False, caption=None,
             capt_pos="bottom", ref=None):
    r"""
    Encapsulate the given content within "\begin" and "\end" commands of the
    specified environment., an add an line-break the end

    Parameters
    ----------
    env : str
        Name of the LaTeX environment in which the content needs to be
        encapsulated.
    content : str
        The LaTeX content to be encapsulated.
    arg : str or None, optional
        Additional argument to be added after the "\begin" command. If None,
        no additional argument is used. The default is None.
    center : bool, optional
        Specifies whether centering should be applied to the environment.
        The default is False.
    caption : str or None, optional
        Caption for the environment. If None, no caption is added.
        The default is None.
    capt_pos : str, optional
        Specifies the position of the caption in the environment. The
        accepted values are "top" and "bottom". The default is "bottom".
    ref : str or None, optional
        Tag for adding a reference label to the table. If None, no label is
        be added. The default is None.

    Returns
    -------
    ltx : str
        LaTeX code for the given environment parameters.

    """
    return encaps(env, content, arg, center, caption, capt_pos, ref, True)
