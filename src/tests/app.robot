*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Start

*** Test Cases ***
Test Welcome
    Output Should Contain  Welcome to Bookmarker!


Test Quit
    Input Quit Command
    Output Should Contain  See you again!


Test Add Command
    Input Add Command
    Output Should Contain  Please give a title
    Input  Tuntematon sotilas
    Output Should Contain  Bookmark "Tuntematon sotilas" created!


Test Show Command
    Input Show Command
    Output Should Contain  Show-command is not yet implemented


*** Keywords ***
Start
    Welcome


