#!/usr/bin/env python3

import py_functions as pf
import subprocess


pf.equalize_lambdas_and_tmins_imp_ref()

subprocess.call( './0a_run' )
subprocess.call( './99_t_subtract.py' )
