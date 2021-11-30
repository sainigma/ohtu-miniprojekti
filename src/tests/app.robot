*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Start
Test Teardown  Reset

*** Test Cases ***
Test Welcome
    Output Should Contain  Welcome to Bookmarker!


Test Add Command
    Input Add Command
    Prompt Should Contain  Title:${SPACE}
    Input  Tuntematon sotilas
    Read Title
    Output Should Be  Bookmark "Tuntematon sotilas" created!


Test Show Empty Command
    Input Show Command
    Output Should Be  No bookmarks

Test Show Command
    Add Bookmark  Tuntematon Sotilas
    Input Show Command
    Output Should Be  Tuntematon Sotilas

Test Find Command
    Add Bookmark  Tuntematon Sotilas
    Input Find Command
    Prompt Should Contain  Term:${SPACE}
    Input  Tuntema
    Read Search Term
    Output Should Be  Tuntematon Sotilas

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