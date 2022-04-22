from flask.app import Flask
from app import app
import datetime as dt
from flask import flash, render_template, redirect, url_for
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import Post, Comment, User, State
from app.classes.forms import StateForm, CommentForm
from flask_login import login_required, current_user

# make an array with the names of every state
stateList = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming'
]

@app.route('/state/list', methods=['GET', 'POST'])
def state_list():
    states = State.objects()
    return render_template('states.html',states=states)

@app.route('/state/new', methods=['GET', 'POST'])
@login_required
def new_state():
    state = StateForm()
    states = State.objects()
    if state.validate_on_submit():
        newState = State(
            stateName = state.stateName.data,
            author = current_user.id,
            totalBudget = state.totalBudget.data,
            perCapitaBudget = state.perCapitaBudget.data,
            budgetGrowth = state.budgetGrowth.data,

            modifydate = dt.datetime.utcnow()
        )

        newState.save()
        return redirect(url_for('state',stateID=newState.id))
    
    return render_template('stateform.html',state=state, states=states, stateList=stateList)

@app.route('/state/<stateID>')
# This route will only run if the user is logged in.
@login_required
def state(stateID):
    # retrieve the post using the postID
    thisState = State.objects.get(id=stateID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to posts meaning that every comment contains a reference to a post. In this case
    # there is a field on the comment collection called 'post' that is a reference the Post
    # document it is related to.  You can use the postID to get the post and then you can use
    # the post object (thisPost in this case) to get all the comments.
    theseComments = Comment.objects(post=thisState)
    # Send the post object and the comments object to the 'post.html' template.
    return render_template('state.html',post=thisState,comments=theseComments)

@app.route('/state/edit/<postID>', methods=['GET', 'POST'])
@login_required
def stateEdit(postID):
    editPost = State.objects.get(id=postID)
    # if the user that requested to edit this post is not the author then deny them and
    # send them back to the post. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editPost.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('post',postID=postID))
    # get the form object
    form = StateForm()
    # If the user has submitted the form then update the post.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editPost.update(
            stateName = form.stateName.data,
            totalBudget = form.totalBudget.data,
            perCapitaBudget = form.perCapitaBudget.data,
            budgetGrowth = form.budgetGrowth.data,
            modifydate = dt.datetime.utcnow
        )

        # After updating the document, send the user to the updated post using a redirect.
        return redirect(url_for('state',stateID=postID, state=form, states=stateList, currState=form.stateName.data))

    # if the form has NOT been submitted then take the data from the editPost object
    # and place it in the form object so it will be displayed to the user on the template.
    form.stateName.data = editPost.stateName
    form.totalBudget.data = editPost.totalBudget
    form.perCapitaBudget.data = editPost.perCapitaBudget
    form.budgetGrowth.data = editPost.budgetGrowth

    # Send the user to the post form that is now filled out with the current information
    # from the form.
    return render_template('stateform.html',state=form, stateList=stateList, currState=form.stateName.data)

# @app.route('/comment/new/<postID>', methods=['GET', 'POST'])
# @login_required
# def commentNew(postID):
#     post = Post.objects.get(id=postID)
#     form = CommentForm()
#     if form.validate_on_submit():
#         newComment = Comment(
#             author = current_user.id,
#             post = postID,
#             content = form.content.data
#         )
#         newComment.save()
#         return redirect(url_for('post',postID=postID))
#     return render_template('commentform.html',form=form,post=post)

# @app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
# @login_required
# def commentEdit(commentID):
#     editComment = Comment.objects.get(id=commentID)
#     if current_user != editComment.author:
#         flash("You can't edit a comment you didn't write.")
#         return redirect(url_for('post',postID=editComment.post.id))
#     post = Post.objects.get(id=editComment.post.id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         editComment.update(
#             content = form.content.data,
#             modifydate = dt.datetime.utcnow
#         )
#         return redirect(url_for('post',postID=editComment.post.id))

#     form.content.data = editComment.content

#     return render_template('commentform.html',form=form,post=post)   

# @app.route('/comment/delete/<commentID>')
# @login_required
# def commentDelete(commentID): 
#     deleteComment = Comment.objects.get(id=commentID)
#     deleteComment.delete()
#     flash('The comments was deleted.')
#     return redirect(url_for('post',postID=deleteComment.post.id)) 