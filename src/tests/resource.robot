*** Settings ***
Library  ../app.py
Library  ../AppLibrary.py

*** Keywords ***
Input Quit Command
    Input  q
    Read Command

Input Add Command
    Input  add
    Read Command

Input Show Command
    Input  show
    Read Command


