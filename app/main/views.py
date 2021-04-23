from . import main_blueprint
from ..tasks import reverse_name
from flask import render_template, request, flash, current_app, url_for, redirect, abort
from flask_login import login_required, current_user
import csv
import os
import pandas as pd
from werkzeug.utils import secure_filename






@main_blueprint.route('/')
def index():
    #result = reverse_name.apply_async(args=[name])
    return render_template('main/index.html')


@main_blueprint.route('/upload_email_list', methods=['GET', 'POST'])
@login_required
def upload_email_list():
    if request.method == 'POST':
        uploaded_file = request.files['csv_file'] 
       
        # First make sure the form submission actually has a file
        if uploaded_file:

            # If there was a file submitted with the form sanitize the file name
            filename = secure_filename(uploaded_file.filename)

            # Check the file extension and reject any unsupported file types
            if filename != " ":
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    abort(400)

                # Create a pandas dataframe of the csv file
                data = pd.read_csv(uploaded_file)

                # Isolate the headings in the dataframe and check to make sure that the expected 'email' column is present in the file
                file_headers = list(data.columns.values.tolist())

                if "email" in file_headers:

                    # Discard all unnecessary data columns so that we only work with the email column
                    email_data = data['email']

                    # Remove duplicate emails and take note how many of the original emails were duplicates
                    email_data_duplicates_removed = email_data.drop_duplicates()
                    total_emails = email_data.count()
                    duplicates = total_emails - email_data_duplicates_removed.count()

                    # Create a pandas dataframe of the list of non-duplicate emails
                    cleaned_email_list = {'email':[]}
                    for email in email_data_duplicates_removed:
                        cleaned_email_list['email'].append(email)
                    df = pd.DataFrame(cleaned_email_list)

                    # Prepend the user's email address to the file name before saving it to the server to distinguish files uploaded by different users
                    new_filename = current_user.email+' '+filename

                    # Define the absolute path to the location where the csv file should be saved on the server
                    upload_path = os.path.join(current_app.config['UPLOAD_PATH'], new_filename)

                    # Write the pandas dataframe to a csv file to be saved on the server
                    df.to_csv(upload_path, index=False)
                    current_app.logger.info(f'New csv file uploaded to the server:{upload_path}')

                    flash('File has been received!')
                    return redirect(url_for('main.upload_email_list'))

                flash('No column named email in the csv file.')
                current_app.logger.info(f'No email column in file uploaded:{current_user.email}')
                return redirect(url_for('main.upload_email_list'))

        flash("Please upload a csv file.")
        current_app.logger.info(f'No file attached when uploading email list:{current_user.email}')
        return redirect(url_for('main.upload_email_list'))

    return render_template('main/upload_list.html')