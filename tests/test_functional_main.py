"""
This module contains the functional tests for the main blueprint (ie, the core functionality of the scrub my list application)
"""

import pytest
import io
from werkzeug.datastructures import FileStorage
import io
import json


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
def test_post_successful_file_upload_no_email_column(test_client, login_default_user, delete_uploaded_file):
    """
    GIVEN a flask application
    WHEN a POST request for '/upload_email_list' is received from a user who is logged in
    THEN check that server gets the file successfully
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