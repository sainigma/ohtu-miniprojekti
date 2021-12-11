*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Welcome
Test Teardown  Reset


*** Test Cases ***

Test delete
    Add Bookmark  http://www.princess-mononoke.com
    Input  delete 1
    Read Command
    Execute Command
    Output Should Contain  Bookmark 1 deleted successfully

Test Select
    Add Bookmark  http://www.princess-mononoke.com
    Input  select 1
    Input  b
    Read Command
    Execute Command
    Output Should Contain  1: Welcome to Princess Mononoke

Test Select Incorrect Id
    Add Bookmark  http://www.princess-mononoke.com
    Input  select 2
    Read Command
    Execute Command
    Output Should Contain  Invalid id

Test Delete In Incorrect State
    Add Bookmark  http://www.princess-mononoke.com
    Input  delete
    Read Command
    Execute Command
    Output Should Contain  Please select a bookmark to delete it
