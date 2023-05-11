from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DateTimeField, SelectMultipleField, SubmitField, \
    FieldList, IntegerField, validators,BooleanField
from wtforms.validators import DataRequired, Length


class BaseFrom(FlaskForm):
    class Meta:
        locales=['zh']

class LoginFrom(FlaskForm):
    userno = StringField('usernno', validators=[
                           DataRequired(), Length(1, 20)])
    password = StringField('password', validators=[
                           DataRequired(), Length(1, 128)])


class RoleFrom(FlaskForm):
    parent_id = StringField('parent_id', validators=[DataRequired()])
    menu_name = StringField('menu_name', validators=[DataRequired()])
    menu_type = StringField('menu_type', validators=[DataRequired()])
    menu_path = StringField('menu_path', validators=[DataRequired()])
    component = StringField('component', validators=[DataRequired()])
    # menu_perm=StringField('menu_perm',validators=[DataRequired()])
    menu_visible = StringField('menu_visible',)
    menu_icon = StringField('menu_icon', validators=[DataRequired()])
    redirect_url = StringField('redirect_url')

    def getdict(self):
        parent_id = self.parent_id
        menu_name = self.menu_name
        menu_type = self.menu_type
        menu_path = self.menu_path
        component = self.component
        menu_visible = self.menu_visible
        menu_icon = self.menu_icon
        redirect_url = self.redirect_url


class RoleMenuFrom(FlaskForm):
    roleid = StringField('roleid', validators=[DataRequired()])
    checkedMenuIds = FieldList(IntegerField('checkedMenuIds'), validators=[
                               validators.DataRequired()])


class AssetsFrom(FlaskForm):
    assetsname = StringField('assetsname', validators=[DataRequired()])
    assetstype = StringField('assetstype', validators=[DataRequired()])
    brandid = StringField('roleid', validators=[DataRequired()])
    suppilerid = StringField('suppilerid', validators=[DataRequired()])
    cpu = StringField('cpu',)
    ram = StringField('ram')
    rom = StringField('rom')
    qty = StringField('qty', validators=[DataRequired()])
    remark = StringField('remark',)
    warrantydate = StringField('warrantydate', validators=[DataRequired()])


class DictItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type_code = StringField('type_code', validators=[DataRequired()])
    value = StringField('value', validators=[DataRequired()])


class MenuForm(BaseFrom):
    id =StringField('id', validators=[DataRequired()])
    parent_id =StringField('parent_id', validators=[DataRequired()])
    menu_name = StringField('menu_name', validators=[DataRequired()])
    menu_type = StringField('menu_type', validators=[DataRequired()])
    menu_path = StringField('menu_path', validators=[DataRequired()])
    component = StringField('component', validators=[DataRequired()])
    menu_visible = BooleanField('menu_visible', validators=[DataRequired()])
    menu_sort = StringField('menu_sort', validators=[DataRequired()])
    menu_icon =StringField('menu_icon', validators=[DataRequired()])
    redirect_url = StringField('redirect_url' )
