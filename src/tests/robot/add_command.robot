*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Welcome
Test Teardown  Reset

***Test Cases***

Test Add Command
    Input  add
    Read Command
    Input  http://www.princess-mononoke.com
    Input  n
    Execute Command
    Prompt Should Contain  Url:${SPACE}
    Output Should Contain  Bookmark "1 Welcome to Princess Mononoke" created!
