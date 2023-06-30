from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired
from apps.authentication.models import Movies


class PredictGrossForm(FlaskForm):
    genre = SelectField('Thể loại', choices=[], validators=[DataRequired()])
    budget = IntegerField('Ngân sách', validators=[DataRequired()])
    rating = FloatField('Đánh giá', validators=[DataRequired()])
    runtime = IntegerField('Thời gian dự kiến công chiếu', validators=[DataRequired()])
