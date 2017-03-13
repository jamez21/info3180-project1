"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, json, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import ProfileForm
from models import UserProfile

import os
import random
import time


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/profile', methods=['GET','POST'])
def add_profile():
    """Render form template"""
    form = ProfileForm()
    if(form.validate_on_submit()):
        fname=form.firstname.data
        lname=form.lastname.data
        uname=form.username.data
        uage=form.age.data
        gen=form.gender.data
        bio=form.biography.data
        
        imagefolder = app.config["UPLOAD_FOLDER"]
        img = form.image.data
        imagename = secure_filename(img.filename)
        img.save(os.path.join(imagefolder,imagename))
        
        uid = random.randint(1000,1999)
        ctime=timeinfo()
        
        profile = UserProfile(userid=uid,first_name=fname,last_name=lname,username=uname,age=uage,gender=gen,biography=bio,image=imagename,created_on=ctime)
        
        db.session.add(profile)
        db.session.commit()
    
        flash('User Profile Added','success')
        return redirect(url_for('home'))
        
    flash_errors(form)
        
    return render_template("add_profile.html", form=form)
    
@app.route('/profiles',methods=["GET","POST"])
def view_profiles():
    """ Display all profiles in database """
    profiles = db.session.query(UserProfile).all()
    
    if(request.method=="POST"):
        p_list = []
        
        for profile in profiles:
            user={'username':profile.username, 'userid':profile.userid}
            p_list.append(user)
            
        return jsonify(users=p_list)
    else:
        if not profiles:
            
            flash('No users have been added yet.')
            
            return redirect(url_for('add_profile'))
            
        return render_template('profiles.html', profiles=profiles)
    
@app.route('/profile/<userid>',methods=['GET','POST'])
def view_profile(userid):
    """ Display specific profile from database"""
    if(request.method=='POST'):
        user_profile = list(UserProfile.query.filter_by(userid=userid).first()).with_entities(UserProfile.username,UserProfile.firstname,UserProfile.lastname,UserProfile.userid,UserProfile.gender,UserProfile.age,UserProfile.biography)
        
        jres = json.dumps(user_profile)
        res=Response(response=jres,status=200,mimetype="application/json")
        return res
    else:
        profile=UserProfile.query.filter_by(userid=userid)
        return render_template('profile.html',profile=profile)

def timeinfo():
    td = time.strftime("%a, %d %b %Y")
    return td
   
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form,field).label.text,error), 'danger') 


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
