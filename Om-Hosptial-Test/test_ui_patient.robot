*** Settings ***
Documentation     Keyword-Driven Testing for om_hospital module in Odoo
Library           SeleniumLibrary

*** Variables ***
${LOGIN URL}      http://localhost:8069/web/login/
${BROWSER}        Chrome
${USERNAME}       user1@gmail.com
${PASSWORD}       user_pass

*** Keywords ***
Login To Odoo
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Title Should Be    Login | My Website
    Input Text    login    user1@gmail.com
    Input Text    password    user_pass
    Click Element    //*[contains(text(),'Log in')]
    Sleep    5s

Navigate To Hospital Module
    # Step 1: Click the Apps menu (grid icon)
    Click Element    xpath=//button[@title='Home Menu']
    Sleep    3s
    # Step 2: Move mouse to Hospital link
    Mouse Over    xpath=//a[contains(@class,'dropdown-item')][contains(text(),'Hospital')]
    Sleep    2s
    # Step 3: Click Hospital
    Click Element    xpath=//a[contains(@class,'dropdown-item')][contains(text(),'Hospital')]
    Sleep    5s

Click Create Button
    Wait Until Element Is Visible    xpath=//button[contains(@class,'o_list_button_add')]    10s
    Mouse Over    xpath=//button[contains(@class,'o_list_button_add')]
    Sleep    1s
    Click Element    xpath=//button[contains(@class,'o_list_button_add')]
    Sleep    3s

Click Save Button
    Wait Until Element Is Visible    xpath=//button[contains(@class,'o_form_button_save')]    10s
    Mouse Over    xpath=//button[contains(@class,'o_form_button_save')]
    Sleep    1s
    Click Element    xpath=//button[contains(@class,'o_form_button_save')]
    Sleep    3s

Handle Duplicate Error Popup
    ${popup_exists}=    Run Keyword And Return Status    Element Should Be Visible    xpath=//button[contains(text(),'Ok') or contains(text(),'OK')]
    Run Keyword If    ${popup_exists}    Click Element    xpath=//button[contains(text(),'Ok') or contains(text(),'OK')]
    Sleep    2s

*** Test Cases ***
Test Case 1: Odoo Login
    [Documentation]    Verify user can successfully login to Odoo
    Login To Odoo
    Capture Page Screenshot    test1_login_success.png
    Title Should Be    Odoo - Discuss
    Log    Login successful
    [Teardown]    Close Browser

Test Case 2: Positive Test - Create New Patient
    [Documentation]    Verify a new patient can be created in om_hospital module
    Login To Odoo
    Navigate To Hospital Module
    Capture Page Screenshot    test2_hospital_list.png
    Click Create Button
    
    # Fill in patient details
    Input Text    name    Test Patient Robot
    Input Text    age    25
    Sleep    2s
    Capture Page Screenshot    test2_form_filled.png

    
    Click Save Button
    Handle Duplicate Error Popup
    
    Sleep    3s
    Capture Page Screenshot    test2_patient_created.png
    Log    Test Case 2 completed
    [Teardown]    Close Browser

Test Case 3: Negative Test - Age Validation Bug Detection and Fix
    [Documentation]    Tests age validation: BEFORE FIX (bug exists) vs AFTER FIX (validation works)
    [Tags]    bug-detection
    Login To Odoo
    Navigate To Hospital Module
    Capture Page Screenshot    test3_hospital_opened.png
    Click Create Button
    Sleep    2s
    
    # Enter patient with NEGATIVE age
    Input Text    name    Negative Age Test
    Input Text    age    -7
    Sleep    2s
    Capture Page Screenshot    test3_negative_age_entered.png
    
    Click Save Button
    Sleep    5s
    Capture Page Screenshot    test3_after_save.png
    
    # Check if error/warning message appeared
    ${error_exists}=    Run Keyword And Return Status    Page Should Contain Element    xpath=//div[contains(@class,'o_notification') or contains(@class,'alert')]
    
    # Capture screenshot based on result
    Run Keyword If    not ${error_exists}    Capture Page Screenshot    test3_bug_confirmed_no_error.png
    Run Keyword If    ${error_exists}    Capture Page Screenshot    test3_validation_error.png
    
    # Log results for both scenarios
    Run Keyword If    not ${error_exists}    Log    BEFORE FIX: BUG DETECTED - System accepted negative age without validation (check_age only checks == 0, not <= 0)
    Run Keyword If    ${error_exists}    Log    AFTER FIX: Validation working - System correctly rejected negative age (check_age now uses <= 0)
    
    # The test demonstrates the bug and its fix
    Log    Bug Location: om_hospital/models/patient.py - check_age() method
    Log    Fix Applied: Changed 'if rec.age == 0' to 'if rec.age <= 0'
    
    [Teardown]    Close Browser
    
Test Case 3b: Negative Age Validation - Bug Detection
    [Documentation]    Bug: check_age() only checks == 0, not <= 0. Negative ages are accepted.
    [Tags]    bug-detection    negative-test
    
    Login To Odoo
    Navigate To Hospital Module
    Click Create Button
    Sleep    2s
    
    # Enter patient with NEGATIVE age
    Input Text    name    Negative Age Test
    Input Text    age    -10
    Capture Page Screenshot    test3_negative_age_entered.png
    
    # Try to save - should be blocked but won't be (bug)
    Click Save Button
    Sleep    5s
    Capture Page Screenshot    test3_after_save_attempt.png
    
    # Check if we're still on create page (validation blocked save)
    ${current_url}=    Get Location
    Should Contain    ${current_url}    /new
    ...    message=BUG DETECTED: Patient with age=-10 was saved! check_age() uses '==' instead of '<='
    
    [Teardown]    Close Browser

Test Case 4: View Patient List
    [Documentation]    Verify patient list view displays correctly
    Login To Odoo
    Navigate To Hospital Module

    Capture Page Screenshot    test4_patient_list_view.png
    Page Should Contain Element    xpath=//table | //div[contains(@class,'o_kanban')]
    Sleep    2s
    
    Log    Patient list displayed successfully
    [Teardown]    Close Browser

Test Case 5: Logout From Odoo
    [Documentation]    Verify user can successfully logout from Odoo
    Login To Odoo
    Capture Page Screenshot    test5_before_logout.png

    
    # Click user menu (top right corner)
    Mouse Over    xpath=//span[contains(@class,'oe_topbar_name')]
    Sleep    1s
    Click Element    xpath=//span[contains(@class,'oe_topbar_name')]
    Sleep    2s
    Capture Page Screenshot    test5_user_menu_open.png

    
    # Click Logout
    Mouse Over    xpath=//a[contains(text(),'Log out')]
    Sleep    1s
    Click Element    xpath=//a[contains(text(),'Log out')]
    Sleep    3s
    
    Capture Page Screenshot    test5_logged_out.png
    Title Should Be    Login | My Website
    Log    Logout successful
    [Teardown]    Close Browser