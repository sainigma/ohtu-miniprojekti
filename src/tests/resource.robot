*** Settings ***
Library  ../app.py
Library  ../AppLibrary.py

*** Keywords ***
Input Quit Command
    Input  q
    Read Input

Input Add Command
    Input  add
    Read Input

Input Show Command
    Input  show
    Read Input


