*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Welcome
Test Teardown  Reset

***Test Cases***

Test Select
    Add Bookmark  http://www.princess-mononoke.com
    Input  select
    Read Command
    Input  1
    Execute Command
    Prompt Should Contain  Id:${SPACE}
    Output Should Contain  Welcome to Princess Mononoke selected

Test Select Incorrect Id
    Add Bookmark  http://www.princess-mononoke.com
    Input  select
    Read Command
    Input  2
    Execute Command
    Prompt Should Contain  Id:${SPACE}
    Output Should Contain  Invalid id

Test delete
    Add Bookmark  http://www.princess-mononoke.com
    Select By Id  1
    Input  delete
    Read Command
    Execute Command
    Output Should Contain  Bookmark 1 deleted successfully

Test Delete In Incorrect State
    Add Bookmark  http://www.princess-mononoke.com
    Input  delete
    Read Command
    Execute Command
    Output Should Contain  Please select a bookmark to delete it
