*** Settings ***
#Test Setup   Start App
Resource  resource.robot

*** Test Cases ***
Test Welcome
    Output Should Contain  Welcome to bookmarker!


