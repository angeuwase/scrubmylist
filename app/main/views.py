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
       
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            if filename != " ":
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                
                new_filename = current_user.email+' '+filename
                upload_path = os.path.join(current_app.config['UPLOAD_PATH'], new_filename)
                uploaded_file.save(upload_path)
 
                with open(upload_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    file_headers = reader.fieldnames

                    if "email" in file_headers:
                        for row in reader:
                            print(row['email'])
                        flash('File has been received!')
                        return redirect(url_for('main.upload_email_list'))
                    flash('No column named email in the csv file.')
                    return redirect(url_for('main.upload_email_list'))
  
        flash("Please upload a csv file.")
        current_app.logger.info(f'No file attached when uploading email list:{current_user.email}')
        return redirect(url_for('main.upload_email_list'))
  
        
        #data = pd.read_csv(f)
       # email_data = data['email']
       # for email in email_data:
           # print(email)
        #email_data_duplicates_removed = email_data.drop_duplicates()
        #duplicates = email_data.count()-email_data_duplicates_removed.count()
        #print('duplicates', duplicates)

        #for email in email_data_duplicates_removed:
           # print(email)

        
        #filename = f.filename

            
            #for row in reader:
            #    print(row['email'])
            
        


            #print(row['first_name'], row['last_name'])
        #fstring = f.read()
        #print('text', fstring)
        #
        #return fstring
        #current_app.logger.info(f'Email list uploaded by {current_user.email}:{request.files['file'].filename}')
       # return redirect(url_for('main.upload_email_list'))

    return render_template('main/upload_list.html')