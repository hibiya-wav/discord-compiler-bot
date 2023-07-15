#!/bin/bash

if [[ -e "code.py"  || -e "code.cpp" || -e "code.sh" || -e "Main.java" || -e "Main.class" ]]; then
    rm code.py code.cpp code.sh Main.java Main.class 2>/dev/null # makes sure that missing files being rm'd don't confuse with actual errors in script
                                                                 # use nul on windows
fi
