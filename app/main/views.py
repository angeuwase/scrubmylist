from . import main_blueprint
from ..tasks import reverse_name
from flask import render_template, request, flash, current_app, url_for, redirect, abort, send_file
from flask_login import login_required, current_user
import csv
import os
import pandas as pd
from werkzeug.utils import secure_filename
from .. import db
from ..models import EmailList, ValidationResult
from datetime import datetime





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

                    # Create a new email list object and add it to the database
                    new_email_list = EmailList(upload_path, current_user.id, total_emails, duplicates, datetime.now())
                    db.session.add(new_email_list)
                    db.session.commit()

                    flash('File has been received!')
                    return redirect(url_for('main.mylists'))

                flash('No column named email in the csv file.')
                current_app.logger.info(f'No email column in file uploaded:{current_user.email}')
                return redirect(url_for('main.upload_email_list'))

        flash("Please upload a csv file.")
        current_app.logger.info(f'No file attached when uploading email list:{current_user.email}')
        return redirect(url_for('main.upload_email_list'))

    return render_template('main/upload_list.html')


@main_blueprint.route('/mylists')
@login_required 
def mylists():

    # Get the list of email lists that belong to the user
    email_lists = EmailList.query.order_by(EmailList.id).filter_by(owner_id=current_user.id).all()

    return render_template('main/mylists.html', email_lists=email_lists)

@main_blueprint.route('/delete_email_list/<int:email_list_id>')
@login_required
def delete_email_list(email_list_id):
    email_list = EmailList.query.filter_by(id=email_list_id).first()
    file_name = email_list.file_name    # file_name is the full path to the file
    db.session.delete(email_list)
    db.session.commit()
    os.remove(file_name)
    flash('The email list has been deleted.')
    return redirect(url_for('main.mylists'))

@main_blueprint.route('/validate_email_list/<int:email_list_id>')
@login_required
def validate_email_list(email_list_id):

    email_list = EmailList.query.filter_by(id=email_list_id).first()

    file_name = email_list.file_name    # file_name is the full path to the file
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_validation_result = ValidationResult(row['email'], email_list_id)
            new_validation_result.get_validation_results()
            db.session.add(new_validation_result)

    email_list.is_verified = True
    email_list.date_verified = datetime.now()
    db.session.add(email_list)
    db.session.commit()
    flash('Email list has successfully been verified')
    return redirect(url_for('main.mylists'))

    
@main_blueprint.route('/download_results/<int:email_list_id>')
@login_required
def download_results(email_list_id):

    results = ValidationResult.query.filter_by(email_list_id=email_list_id).all()

    email_list = EmailList.query.filter_by(id=email_list_id).first()
    
    new_file_name = 'results_'+current_user.email+' ' +email_list.file_name.split()[1] # file_name is the full path to the file

    upload_path = os.path.abspath(os.path.join(current_app.config['UPLOAD_PATH'], new_file_name))

    results_list = []

    for result in results:
        data = {'id':result.id, 'email_address':result.email_address, 'email_list_id':result.email_list_id, 'is_free':result.is_free, 'is_syntax': result.is_syntax, 'is_domain':result.is_domain, 'is_smtp':result.is_smtp, 'is_verified':result.is_verified, 'is_server_down':result.is_server_down, 'is_greylisted':result.is_greylisted, 'is_disposable':result.is_disposable, 'is_suppressed':result.is_suppressed, 'is_role':result.is_role, 'is_high_risk':result.is_high_risk, 'is_catchall':result.is_catchall, 'status':result.status, 'mailboxvalidator_score':result.mailboxvalidator_score}
        results_list.append(data)

    df = pd.DataFrame(results_list)
  
    df.to_csv(upload_path, index=False)
    
    return send_file(upload_path,
                     mimetype='text/csv',
                     as_attachment=True)
