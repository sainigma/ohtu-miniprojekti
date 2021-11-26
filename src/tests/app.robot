*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Start

*** Test Cases ***
Test Welcome
    Output Should Contain  Welcome to Bookmarker!


Test Add Command
    Input Add Command
    Prompt Should Contain  Title: 
    Input  Tuntematon sotilas
    Read Title
    Output Should Contain  Bookmark "Tuntematon sotilas" created!


Test Show Command
    Input Show Command
    Output Should Contain  Tuntematon sotilas


*** Keywords ***
Start
    Welcome
