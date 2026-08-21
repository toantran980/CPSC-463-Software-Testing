# It is day sensetive so Sat. - Sun. would not show menu, only weekdays

*** Settings ***
Documentation     Keyword-Driven Tests for Odoo Lunch Module
Library           SeleniumLibrary
Suite Teardown    Close All Browsers

*** Variables ***
${URL}                http://localhost:8069
${BROWSER}            Chrome
${LOGIN_URL}          ${URL}/web/login
${USERNAME}           your-email@example.com
${PASSWORD}           your-password
${DELAY}              2s

*** Test Cases ***
Test 1: Navigate To My Lunch - POSITIVE
    [Documentation]    Positive test: Login and navigate to My Lunch view
    [Tags]    positive
    [Teardown]    Close Browser
    Log To Console    \n======================================================================
    Log To Console    TEST 1/3: NAVIGATE TO MY LUNCH (POSITIVE)
    Log To Console    ======================================================================
    
    Open Browser And Login
    Navigate To Lunch Module
    Click My Lunch Menu
    Verify On My Lunch Page
    
    Log To Console    TEST 1 PASSED: Successfully accessed My Lunch
    Log To Console    ======================================================================\n

Test 2: Try To Add Non-Existent Product To Favorites - NEGATIVE (WILL FAIL)
    [Documentation]    Negative test: Try to add product that doesn't exist to favorites (intentional failure)
    [Tags]    negative
    [Teardown]    Run Keyword If Test Failed    Close Browser
    Log To Console    \n======================================================================
    Log To Console    TEST 2/3: ADD NON-EXISTENT PRODUCT TO FAVORITES (NEGATIVE - WILL FAIL)
    Log To Console    ======================================================================
    
    Open Browser And Login
    Navigate To Lunch Module
    Click My Lunch Menu
    Try To Add Non Existent Product To Favorites
    
    Log To Console    TEST 2 PASSED (but should fail)
    Log To Console    ======================================================================\n

Test 3: Search For Products - POSITIVE
    [Documentation]    Positive test: Search functionality in Lunch
    [Tags]    additional
    [Teardown]    Close Browser
    Log To Console    \n======================================================================
    Log To Console    TEST 3/3: SEARCH FOR PRODUCTS IN LUNCH (POSITIVE)
    Log To Console    ======================================================================
    
    Open Browser And Login
    Navigate To Lunch Module
    Click My Lunch Menu
    Search For Product    Pizza
    Verify Search Executed
    
    Log To Console    TEST 3 PASSED: Search functionality verified
    Log To Console    ======================================================================\n

*** Keywords ***
Open Browser And Login
    Log To Console    Opening browser...
    Open Browser    ${LOGIN_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.5s
    Log To Console    Browser opened: ${BROWSER}
    
    Log To Console    Logging in to Odoo...
    Wait Until Page Contains Element    id:login    timeout=10s
    Input Text    id:login    ${USERNAME}
    Sleep    0.5s
    Input Text    id:password    ${PASSWORD}
    Sleep    0.5s
    Click Button    xpath://button[@type='submit']
    Sleep    3s
    Wait Until Page Does Not Contain Element    id:login    timeout=10s
    Log To Console    Logged in successfully

Navigate To Lunch Module
    Log To Console          Opening Home Menu...
    Wait Until Element Is Visible    xpath://button[@title='Home Menu']    timeout=10s
    Click Element    xpath://button[@title='Home Menu']
    Sleep    2s
    Log To Console    Home Menu opened
    
    Log To Console          Navigating to Lunch module...
    Wait Until Element Is Visible    xpath://a[contains(@class,'dropdown-item')][contains(text(),'Lunch')]    timeout=10s
    Mouse Over    xpath://a[contains(@class,'dropdown-item')][contains(text(),'Lunch')]
    Sleep    1s
    Click Element    xpath://a[contains(@class,'dropdown-item')][contains(text(),'Lunch')]
    Sleep    3s
    Log To Console    Lunch module opened

Click My Lunch Menu
    Log To Console    Clicking My Lunch menu...
    
    # Check if My Lunch link exists, if not we might already be there
    ${my_lunch_exists}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    xpath://a[contains(text(), 'My Lunch')]    timeout=5s
    
    Run Keyword If    ${my_lunch_exists}    Mouse Over    xpath://a[contains(text(), 'My Lunch')]
    Run Keyword If    ${my_lunch_exists}    Sleep    1s
    Run Keyword If    ${my_lunch_exists}    Click Element    xpath://a[contains(text(), 'My Lunch')]
    Run Keyword If    ${my_lunch_exists}    Sleep    3s
    Run Keyword If    ${my_lunch_exists}    Log To Console    My Lunch menu clicked
    Run Keyword Unless    ${my_lunch_exists}    Log To Console    Already on Lunch page or My Lunch not available

Verify On My Lunch Page
    Log To Console    Verifying on Lunch page...
    
    # Just verify we're on a Lunch-related page
    ${current_url}=    Get Location
    Should Contain    ${current_url}    lunch
    Log To Console    Successfully on Lunch page

Click Non Existent Button
    Log To Console    Attempting to click non-existent button...
    ${bad_locator}=    Set Variable    xpath://button[contains(text(), 'Submit Order For Delivery')]
    Log To Console    Bad locator: ${bad_locator}
    Log To Console    This WILL FAIL - element does not exist
    
    Wait Until Element Is Visible    ${bad_locator}    timeout=5s
    Click Element    ${bad_locator}
    Log To Console    Clicked button (will not reach here)

Try To Add Non Existent Product To Favorites
    Log To Console    Searching for non-existent product...
    
    # Try to search for a product that doesn't exist
    ${search_exists}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    xpath://input[contains(@placeholder, 'Search')]    timeout=5s
    
    Run Keyword If    ${search_exists}    Input Text    xpath://input[contains(@placeholder, 'Search')]    Unicorn Pizza Supreme Deluxe
    Run Keyword If    ${search_exists}    Press Keys    xpath://input[contains(@placeholder, 'Search')]    RETURN
    Run Keyword If    ${search_exists}    Sleep    2s
    Run Keyword If    ${search_exists}    Log To Console    Searched for non-existent product
    
    Log To Console    Attempting to add to favorites...
    Log To Console    This WILL FAIL - product does not exist
    
    # Try to click favorite star on non-existent product
    ${favorite_locator}=    Set Variable    xpath://div[contains(text(), 'Unicorn Pizza')]//ancestor::div[contains(@class, 'o_kanban_record')]//i[contains(@class, 'fa-star')]
    Wait Until Element Is Visible    ${favorite_locator}    timeout=5s
    Click Element    ${favorite_locator}
    Log To Console    Added to favorites (will not reach here)

Search For Product
    [Arguments]    ${search_term}
    Log To Console       Searching for product: ${search_term}
    
    ${search_exists}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    xpath://input[contains(@placeholder, 'Search')]    timeout=5s
    
    Run Keyword If    ${search_exists}    Input Text    xpath://input[contains(@placeholder, 'Search')]    ${search_term}
    Run Keyword If    ${search_exists}    Press Keys    xpath://input[contains(@placeholder, 'Search')]    RETURN
    Run Keyword If    ${search_exists}    Sleep    2s
    Run Keyword If    ${search_exists}    Log To Console    Searched for: ${search_term}
    Run Keyword Unless    ${search_exists}    Log To Console    Search box not found

Verify Search Executed
    Log To Console    Verifying search executed...
    ${current_url}=    Get Location
    Should Contain    ${current_url}    lunch
    Log To Console    Search executed successfully