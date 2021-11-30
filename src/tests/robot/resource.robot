*** Settings ***
Library  ../../app.py
Library  AppLibrary.py

*** Variables ***
${EMPTY}   ""

*** Keywords ***
Input Quit Command
    Input  q
    Read Command
    Execute Command

Input Add Command
    Input  add
    Read Command
    Execute Command

Input Show Command
    Input  show
    Read Command
    Execute Command

Input Find Command
    Input  search
    Read Command
    Execute Command

Input Empty Command
    Input  ${EMPTY}
    Read Command
    Execute Command


