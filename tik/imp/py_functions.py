#!/usr/bin/env python3

def get_param( filename , paramname ):
    with open( filename , 'r' ) as f:
        for line in f:
            if len( line.strip() )<len( paramname ): continue
            if line.strip()[ : len(paramname) ]==paramname: 
                return line.strip()[ len(paramname) + 1 : ]


def write_param( filename , paramname , paramvalue ):
    with open( filename , 'w+' ) as f:
        for line in f:
            if len( line.strip() )<len( paramname ): continue
            if 
