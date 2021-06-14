# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 13:31:34 2021

@author: Anziko Fred
"""
from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/gidlogin")
        return f(*args, **kwargs)
    return decorated_function