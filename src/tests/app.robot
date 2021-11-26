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

Test Empty Command
    Input Empty Command
    Output Should Contain  Acceptable commands:
    Output Should Contain  'q' - quit,
    Output Should Contain  'add' - add a new bookmark,
    Output Should Contain  'show' - show given amount of bookmarks,
    Output Should Contain  'edit' - edit a bookmark


*** Keywords ***
Start
    Welcome
