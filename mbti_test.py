# Importing Packages
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import numpy as np
import pickle
import re


# Creating App 
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

# Database Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    cleaned_text = db.Column(db.String(), nullable=False)
    mbti_type = db.Column(db.String(4), nullable=False)

# loading the ml model
EI_model = pickle.load(open(r"C:\Users\USER\Desktop\mbti\Resources (weights-vectorizer)\E-I.pkl.txt", 'rb'))
NS_model = pickle.load(open(r"C:\Users\USER\Desktop\mbti\Resources (weights-vectorizer)\N-S.pkl.txt", 'rb'))
FT_model = pickle.load(open(r"C:\Users\USER\Desktop\mbti\Resources (weights-vectorizer)\F-T.pkl.txt", 'rb'))
JP_model = pickle.load(open(r"C:\Users\USER\Desktop\mbti\Resources (weights-vectorizer)\J-P.pkl.txt", 'rb'))
# loading the vectorizer model
vectorizer = pickle.load(open(r"C:\Users\USER\Desktop\mbti\Resources (weights-vectorizer)\vectorizer.pkl.txt", 'rb'))



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_content = request.form['message']
        
        # Text Cleaninig
        replacements = [
            (r"(http.*?\s)", " "),
            (r"[^\w\s]", " "),
            (r"\_", " "),
            (r"\d+", " ")]
        
        for old, new in replacements:
            cleand_message = re.sub(old, new, message_content)
    
        
        message = [cleand_message]

        # vectorize the cleaned text
        message_vectorized = vectorizer.transform(message)

        # Predict the vectorized message
        EI_pred = EI_model.predict(message_vectorized)
        NS_pred = NS_model.predict(message_vectorized)
        FT_pred= FT_model.predict(message_vectorized)
        JP_pred = JP_model.predict(message_vectorized)

        # convert the prediction result from 1 and 0 to letters
        EI_output = 'E' if EI_pred == 0 else "I"
        NS_output = 'N' if NS_pred == 0 else "S"
        FT_output = 'F' if FT_pred == 0 else "T"
        JP_output = 'J' if JP_pred == 0 else "P"

        # MBTI Character's Message Type
        Type = EI_output + NS_output + FT_output + JP_output

        new_message = Message(content=message_content,
                            cleaned_text=cleand_message, mbti_type=Type)

        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your message to the database.'
        
    else:
        messages = Message.query.order_by(Message.id).all()
        num_messages = Message.query.count()  # Counting the number of messages
            
        return render_template('index.html', messages=messages, num_messages=num_messages)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)