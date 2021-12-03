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

Input Help Command
    Input  h
    Read Command
    Execute Command

Input Add Command
    Input  add
    Read Command

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

Input Delete Command
    Input  delete
    Read Command
    Execute Command
    
Add Bookmark
    [Arguments]  @{url}
    Input  add
    Read Command
    Input  @{url}
    Input  y
    Execute Command
