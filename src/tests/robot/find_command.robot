*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Welcome
Test Teardown  Reset

***Test Cases***
Test Find Command
    Add Bookmark  http://www.princess-mononoke.com
    Input  search
    Read Command
    Input  *elcome*
    Execute Command
    Prompt Should Contain  Term:${SPACE}
    Output Should Contain  1 Welcome to Princess Mononoke

Test Not Found With Title
    Add Bookmark  http://www.princess-mononoke.com
    Input  search
    Read Command
    Input  spirited-away
    Execute Command
    Output Should Contain  Could not find any bookmarks with that title