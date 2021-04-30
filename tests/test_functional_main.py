"""
This module contains the functional tests for the main blueprint (ie, the core functionality of the scrub my list application)
"""

import pytest
import io
import os
from flask import current_app
import json
import requests



@pytest.mark.file_upload
def test_get_file_upload_form_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/upload_email_list' is received from a user who is not logged in
    THEN check that the user is redirected to the login page
    """

    response = test_client.get('/upload_email_list', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data


@pytest.mark.file_upload
def test_get_file_upload_form_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request for '/upload_email_list' is received from a user who is logged in
    THEN check that the page is rendered correctly
    """

    response = test_client.get('upload_email_list', follow_redirects=True)

    assert response.status_code == 200
    assert b'Email List Upload' in response.data
    assert b'Only csv files are allowed.' in response.data
    assert b'Files can have multiple columns of data.' in response.data
    assert b'Make sure that the name of the column for the email addresses is called "email"' in response.data
    assert b'Select a file to upload' in response.data
    assert b'Submit' in response.data


@pytest.mark.file_upload
def test_post_file_upload_form_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/upload_email_list' is received from a user who is not logged in
    THEN check that the user is redirected to the login page
    """

    csv_file_data = b'id,first_name,last_name,email,gender,ip_address\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n'

   

    data = dict(csv_file=(io.BytesIO(csv_file_data), "subscribers.csv"))

    response = test_client.post('/upload_email_list', 
                               data=data,
                               content_type='multipart/form-data', 
                               follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data

@pytest.mark.file_upload
def test_post_file_upload_file_too_big(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request for '/upload_email_list' is received from a user who is logged in but the file exceeds the size stipulated by app.config['MAX_CONTENT_LENGTH]
    THEN check that a 413 error is raised
    """
    csv_file_data = b'id,first_name,last_name,email,gender,ip_address\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n'

   

    data = dict(csv_file=(io.BytesIO(csv_file_data), "subscribers.csv"))

    response = test_client.post('/upload_email_list', 
                               data=data,
                               content_type='multipart/form-data', 
                               follow_redirects=True)

    assert response.status_code == 413
    assert b'File Too Big' in response.data

@pytest.mark.file_upload
def test_post_file_upload_unsupported_extension(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request for '/upload_email_list' is received from a user who is logged in but the file is an unsupported file extension
    THEN check that a 400 error is raised
    """
    csv_file_data = b'id,first_name,last_name,email,gender,ip_address\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n'

   

    data = dict(csv_file=(io.BytesIO(csv_file_data), "subscribers.jpg"))

    response = test_client.post('/upload_email_list', 
                               data=data,
                               content_type='multipart/form-data', 
                               follow_redirects=True)

    assert response.status_code == 400
    assert b'Bad Request' in response.data


@pytest.mark.file_upload
def test_post_successful_file_upload(test_client, login_default_user, delete_uploaded_file):
    """
    GIVEN a flask application
    WHEN a POST request for '/upload_email_list' is received from a user who is logged in
    THEN check that server gets the file successfully
    """
    csv_file_data = b'id,first_name,last_name,email,gender,ip_address\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n'

   

    data = dict(csv_file=(io.BytesIO(csv_file_data), "subscribers.csv"))

    response = test_client.post('/upload_email_list', 
                               data=data,
                               content_type='multipart/form-data', 
                               follow_redirects=True)

    assert response.status_code == 200
    assert b'File has been received!' in response.data

@pytest.mark.file_upload
def test_post_successful_file_upload_no_email_column(test_client, login_default_use, delete_uploaded_file):
    """
    GIVEN a flask application
    WHEN a POST request for '/upload_email_list' is received from a user who is logged in but there is no column called "email"
    THEN check that the user is told about the missing column
    """
    csv_file_data = b'id,first_name,last_name,user_email,gender,ip_address\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n'

    data = dict(csv_file=(io.BytesIO(csv_file_data), "subscribers.csv"))

    response = test_client.post('/upload_email_list', 
                               data=data,
                               content_type='multipart/form-data', 
                               follow_redirects=True)
    print(response.data.decode())

    assert response.status_code == 200
    assert b'No column named email in the csv file.' in response.data

@pytest.mark.using_uploaded_file
def test_get_my_email_lists_page_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/mylists' from a user who is not logged in
    THEN check that they are redirected to the login page
    """

    response = test_client.get('/mylists', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data

@pytest.mark.using_uploaded_file
def test_get_my_email_lists_page_logged_in_no_email_lists(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/mylists' from a user who has not uploaded any email lists
    THEN check that the page is rendered appropriately
    """

    response = test_client.get('/mylists', follow_redirects=True)

    assert response.status_code == 200
    assert b'My Email Lists' in response.data
    assert b'You have not uploaded any email list.' in response.data
    assert b'Upload an email list' in response.data

@pytest.mark.using_uploaded_file
def test_get_my_email_lists_page_logged_in_has_email_lists(test_client, login_default_user, upload_email_list_for_default_user, delete_uploaded_file):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/mylists' from a user who has uploaded email lists
    THEN check that the page is rendered appropriately
    """

    response = test_client.get('/mylists', follow_redirects=True)

    headers = [b'File Name', b'Date Uploaded', b'Action' ]
    data = [b'subscribers.csv', b'Delete', b'Verify'  ]

    assert response.status_code == 200
    for header in headers:
        assert header in response.data
    for element in data:
        assert element in response.data

@pytest.mark.using_uploaded_file
def test_delete_email_list_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/delete_email_list/<int:email_list_id>' is received from a user who is not logged in 
    THEN check that they get redirected to the login page
    """
    
    response = test_client.get('/delete_email_list/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Login' in response.data

@pytest.mark.using_uploaded_file
def test_delete_email_list_logged_in(test_client, login_default_user,upload_email_list_for_default_user):
    """
    GIVEN a flask application
    WHEN a GET request for '/delete_email_list/<int:email_list_id>' is received from a user who is logged in 
    THEN check that the email list gets deleted from the database as well as the server
    """

    response = test_client.get('/delete_email_list/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'The email list has been deleted.' in response.data
    assert b'My Email Lists' in response.data
    files = os.listdir(current_app.config['UPLOAD_PATH'])
    assert 'default@gmail.com subscribers.csv' not in files


@pytest.mark.using_uploaded_file
def test_successful_api_call(new_validation_result, mock_requests_get_success):
    """
    GIVEN a flask application and a monkey-patched version of the requests module
    WHEN an API call is made and a successful result received
    THEN check that the validation result gets updated with the validation results
    """

    new_validation_result.get_validation_results()

    assert new_validation_result.is_free == 'True'
    assert new_validation_result.is_syntax == 'True'
    assert new_validation_result.is_domain == 'True'
    assert new_validation_result.is_smtp == 'True'
    assert new_validation_result.is_verified == 'True'
    assert new_validation_result.is_server_down == 'False' 
    assert new_validation_result.is_greylisted == 'False' 
    assert new_validation_result.is_disposable == 'False' 
    assert new_validation_result.is_suppressed == 'False' 
    assert new_validation_result.is_role == 'False'
    assert new_validation_result.is_high_risk == 'True'
    assert new_validation_result.is_catchall == 'False'
    assert new_validation_result.status == 'False'
    assert new_validation_result.mailboxvalidator_score == '0.45'


@pytest.mark.using_uploaded_file
def test_unsuccessful_api_call(new_validation_result, mock_requests_get_failure):
    """
    GIVEN a flask application and a monkey-patched version of the requests module
    WHEN an API call is made and a failure result received
    THEN check that the validation result object does not get updated with the validation results
    """

    new_validation_result.get_validation_results()
    assert new_validation_result.is_free == None
    assert new_validation_result.is_syntax == None
    assert new_validation_result.is_domain == None
    assert new_validation_result.is_smtp == None
    assert new_validation_result.is_verified == None
    assert new_validation_result.is_server_down == None
    assert new_validation_result.is_greylisted == None
    assert new_validation_result.is_disposable == None
    assert new_validation_result.is_suppressed == None
    assert new_validation_result.is_role == None
    assert new_validation_result.is_high_risk == None
    assert new_validation_result.is_catchall == None
    assert new_validation_result.status == None
    assert new_validation_result.mailboxvalidator_score == None

@pytest.mark.using_uploaded_file
def test_successful_validation(test_client, login_default_user, upload_email_list_for_default_user, delete_uploaded_file):
    """
    GIVEN a flask application 
    WHEN a GET request for '/validate_email_list' is received from a logged in user
    THEN check that the email list gets verified correctly
    """

    response = test_client.get('/validate_email_list/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'Email list has successfully been verified' in response.data
    assert b'My Email Lists' in response.data
   
    headers = [b'File Name', b'Date Uploaded', b'Action', b'Date Verified']
    data = [b'subscribers.csv', b'Delete', b'Download Results']
    for header in headers:
        assert header in response.data
    for element in data:
        assert element in response.data





