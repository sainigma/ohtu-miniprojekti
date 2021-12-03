*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Start
Test Teardown  Reset

*** Test Cases ***
Test Welcome
    Output Should Contain  Welcome to Bookmarker!
    Output should Contain  Type 'h' for help

Test Help
    Input Help Command
    Output Should Contain  To delete a bookmark, first select 'edit' and then 'delete'
    Output Should Contain  (Not implemented yet)

Test Show Empty Command
    Input Show Command
    Output Should Contain  No bookmarks

Test Show Command
    Add Bookmark  http://www.princess-mononoke.com
    Input Show Command
    Output Should Contain  1 Welcome to Princess Mononoke

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

Test Empty Command
    Input Empty Command
    Output Should Contain  Acceptable commands:
    Output Should Contain  'q' - quit,
    Output Should Contain  'h' - help,
    Output Should Contain  'add' - add a new bookmark,
    Output Should Contain  'show' - show given amount of bookmarks,
    Output Should Contain  'edit' - edit a bookmark

Test Delete Command
    Input Delete Command
    

*** Keywords ***
Start
    Welcome