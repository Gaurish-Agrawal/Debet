from flask import render_template, Blueprint, request, make_response, jsonify, url_for
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms.fields import DateField, DateTimeLocalField, TimeField
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import redirect
from wtforms import StringField, EmailField
from wtforms.validators import InputRequired, Length
from app.db import db, Debate, Message
from random import choice
from datetime import datetime, timedelta
import openai

openai.api_key = "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"

def judge_client(prompt) -> str:

     # Get response from text-davinci-003
     response =  openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
     responseText = response.choices[0].text

     return responseText




# Create services blueprint
services_blueprint = Blueprint('services', __name__, template_folder='templates')
images = UploadSet('photos', IMAGES)

class Debate_Form(FlaskForm):
    title = StringField('Name', validators=[InputRequired(), Length(min=4, max=300)])
    description = StringField('Email', validators=[InputRequired(), Length(max=200)])
    date = DateTimeLocalField(
        'Date Time', 
        format = "%Y-%m-%dT%H:%M:%S", # secend needeed or its returning None
        default= datetime.utcnow
    )



@services_blueprint.route('/debates/winner', methods=["GET", "POST"])
@login_required
def winner(): 
    winner = judge_client("Argument 1: The prison system should be reformed because previous offenders offend again as they typically have no other places to live. There are over 20,000 prisoners who reoffend because of a lack of housing and stability in their lives after being released from prison.  \n Second Argument: The prison system should not be changed as it disciplines imnates and reforms them. \n Which argument is better?")
    return render_template("winner.html", winner=winner, argument="Argument 1: The prison system should be reformed because previous offenders offend again as they typically have no other places to live. \n Second Argument: The prison system should not be changed as it disciplines imnates and reforms them. \n Which argument is better?")

@services_blueprint.route('/debates/create', methods=["GET", "POST"])
@login_required
def create_debate():
    form = Debate_Form()
    if form.validate_on_submit():
        date_format = datetime.strptime(str(form.date.data), "%Y-%m-%d %H:%M:%S").isoformat()
        new_debate = Debate(name=form.title.data, description=form.description.data, attacker=None, defendent=None, attacker_amount=0, defender_amount=0, created_by = current_user.name, responded_by=None,total_amount = 0, closed=False, ongoing = True, timestamp=date_format)
        db.session.add(new_debate)
        db.session.commit()
        return redirect(url_for("services.join_debate"))
    return render_template("create_debate.html", form=form)

@services_blueprint.route('/debates/gallery', methods=["GET", "POST"])
@login_required
def dashboard():
    if request.args:
        page_num = int(request.args.get("c")) + 1
        posts = db.session.query(Debate).filter(Debate.answered == False, Debate.closed == False).order_by(
            Debate.id.desc()).paginate(page_num, 5, error_out=False).items
        posts_json = []
        for i in posts:
            post_json = {"id": i.id, "timestamp": i.timestamp.isoformat(), "title": i.title,
                         "description": i.description, "closed": i.closed}
            posts_json.append(post_json)
        return make_response(jsonify(posts_json), 200)

    return render_template('debates.html')


@services_blueprint.route('/debates/join', methods=["GET", "POST"])
@login_required
def join_debate():
    debate_list = db.session.query(Debate).filter(Debate.closed == False, Debate.ongoing == True).all()
    return render_template("join_debate.html", debate_list=debate_list)

@services_blueprint.route('/debates/bet', methods=["GET", "POST"])
@login_required #filter
def bet():
    debate_list = db.session.query(Debate).filter(Debate.attacker!=None,Debate.defendent!=None).all()
    if len(request.args) > 0:
        filtering = request.args.get('filter_query')
        if filtering == "Topics(A-Z)":
            debate_list = db.session.query(Debate).filter(Debate.closed == False, Debate.ongoing == True).order_by(Debate.name).all()
        elif filtering == "Topics(Z-A)":
            debate_list = db.session.query(Debate).filter(Debate.closed == False, Debate.ongoing == True).order_by(Debate.name.desc()).all()
        elif filtering == "Popularity":
            debate_list = db.session.query(Debate).filter(Debate.closed == False, Debate.ongoing == True).order_by(Debate.total_amount.desc()).all()
        else:
            debate_list = db.session.query(Debate).filter(Debate.closed == False, Debate.ongoing == True).all()

    return render_template("bet.html", debate_list=debate_list)



    #keep track of which side the user bets on

    print(current_user.tokens)
    print(side)

    return redirect(url_for("services.bet"))
    

    


@services_blueprint.route('/debates/register/<int:debate_id>', methods=["GET", "POST"])
@login_required
def register_debate(debate_id):

    
    chosen_post = Debate.query.get(debate_id)

    print(chosen_post.attacker, chosen_post.defendent)

    if (chosen_post.attacker):
        chosen_post.defendent = current_user.name
    else:
        chosen_post.attacker = current_user.name


    db.session.commit()

    return redirect(url_for("services.join_debate"))

    


@services_blueprint.route('/debates/ongoing/<int:debate_num>', methods=["GET", "POST"])
@login_required
def ongoing(debate_num):
    chosen_post = Debate.query.get(debate_num)
    show_text_box = False
    if not chosen_post or chosen_post.ongoing == False:
        return redirect(url_for("services.join_debate"))
    elif (chosen_post.attacker == None and chosen_post.defender == None):
        show_text_box = True
        option = choice(["a", "d"])
        if option == "a":
            chosen_post.attacker = current_user.id
            chosen_post.defendent = chosen_post.created_by
            db.session.commit()
        elif option == "d":
            chosen_post.defendent = current_user.id
            chosen_post.attacker = chosen_post.created_by
            db.session.commit()

    elif (chosen_post.attacker == current_user.id or chosen_post.defendent == current_user.id):
        show_text_box = True
    messages = db.session.query(Message).filter(Message.debate_id==debate_num).order_by(Message.id).all()

    
    return render_template('ongoing_debate.html', messages = messages, show_text_box = show_text_box)



@services_blueprint.route('/debates/live_debates', methods=["GET", "POST"])
@login_required
def live_debate():
    
   debate_list = db.session.query(Debate).all()
   print(debate_list)
   live_debates = []
   for i in debate_list: 
        dt, _, us = i.timestamp.partition(".")
        
        d1 = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        d2 = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S")
        print(d1 < d2)
        if d1 < d2: 
            live_debates.append(i)

   print(live_debates)
   return render_template('live_debate.html', debate_list=live_debates)


@services_blueprint.route('/debates/place/<int:amount>/<int:debate_id>/<int:side>', methods=["GET", "POST"])
@login_required
def place_bet(amount,debate_id, side):    
    current_user.tokens -= amount    
    chosen_post = Debate.query.get(debate_id)    
    chosen_post.total_amount =  chosen_post.total_amount + amount    
    if side==1: #attacker        
        chosen_post.attacker_amount = chosen_post.attacker_amount + 1    
    else:        
        chosen_post.defendent_amount = chosen_post.defendent_amount + 1  
          
        #keep track of which side the user bets on    
    db.session.commit()
    print(current_user.tokens)    
    print(side)   
    return redirect(url_for("services.bet"))
