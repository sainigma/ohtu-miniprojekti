*** Settings ***
Library  ../app.py
Library  ../AppLibrary.py

*** Variables ***
${EMPTY}   ""

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

Input Find Command
    Input  search
    Read Command

Input Empty Command
    #[Arguments]  ${EMPTY}
    Input  ${EMPTY}
    Read Command


