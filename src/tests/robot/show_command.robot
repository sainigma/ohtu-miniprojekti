*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Welcome
Test Teardown  Reset

*** Test Cases ***
Test Show Empty
    Input Show Command
    Output Should Contain  No bookmarks

Test Show One
    Add Bookmark  http://www.princess-mononoke.com
    Input Show Command
    Output Should Contain  1: Welcome to Princess Mononoke

Test Show Multiple
    Add Bookmark  http://www.princess-mononoke.com
    Add Bookmark  https://en.wikipedia.org
    Add Bookmark  https://fi.wikipedia.org
    Input Show Command
    Output Should Contain  1: Welcome to Princess Mononoke
    Output Should Contain  2: Wikipedia, the free encyclopedia
    Output Should Contain  3: Wikipedia, vapaa tietosanakirja
    