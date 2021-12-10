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
    Input  y
    Execute Command
    Prompt Should Contain  Url:${SPACE}
    Output Should Contain  Bookmark "1: Welcome to Princess Mononoke

Test Add With Usergiven Title
    Input  add
    Read Command
    Input  http://www.princess-mononoke.com
    Input  n
    Input  Not Spirited Away
    Execute Command
    Prompt Should Contain  Do you want to keep the title "Welcome to Princess Mononoke
    Prompt Should Contain  y/n
    Prompt Should Contain  Title:
    Output Should Contain  Bookmark "1: Not Spirited Away

Test Add With Url Not Found
    Input  add
    Read Command
    Input  https://princess-mononoke-this-definitely-does-not-exist.fi
    Execute Command
    Output Should Contain  Invalid url