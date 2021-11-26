*** Settings ***
#Test Setup   Start App
Resource  resource.robot
Test Setup  Start

*** Test Cases ***
Test Welcome
    Output Should Contain  Welcome to Bookmarker!

*** Keywords ***
Start
    Welcome


