from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, new_user):
        user_exist = User.query.filter_by(username=new_user.data).first()
        if user_exist:
            raise ValidationError('Username already exists')

    def validate_email_address(self, new_email):
        email_exists = User.query.filter_by(email_address=new_email.data).first()
        if email_exists:
            raise ValidationError('Email already exists')

    username = StringField(label='username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password1', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='password2', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='submit')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item !')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item !')


class FacultyForm(FlaskForm):
    name = StringField(label='name:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='email:', validators=[Email(), DataRequired()])
    designation = StringField(label="Design:", validators=[DataRequired()])
    submit = SubmitField(label='submit')


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileRequired('File was empty!')])
    submit = SubmitField('Upload')


class EmpForm(FlaskForm):
    name = StringField(label='name:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='email:', validators=[Email(), DataRequired()])
    designation = StringField(label="Design:", validators=[DataRequired()])
    photo = FileField(validators=[FileRequired('File was empty!')])
    submit = SubmitField(label='submit')