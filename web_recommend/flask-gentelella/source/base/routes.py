import sys
sys.path.append('./../../../../Recommend_system_python/')
import interface
from system_object import User
 
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user
)
from .forms import LoginForm, CreateAccountForm


# start the login system
login_manager = LoginManager()

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

# from database import db
# from .models import User


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')


@blueprint.route('/fixed_<template>')
@login_required
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

# Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    #########增加了判断请求方式
    if 'GET' == request.method:
        #return render_template('login/login.html')
        return render_template(
            'login/login.html',
            login_form=login_form,
            create_account_form=create_account_form
        )
    ###########
    if 'login' in request.form:
        username = str(request.form['username'])
        password = str(request.form['password'])
        print("*****************login**********************")
        result = interface.accessCheck(username, password)
        print("result:", result)
        if result > 0:
            user_obj = User(result)
            print("user_obj_type", type(user_obj))
            print(user_obj.ID)
            login_user(user_obj)
            print("current_user:", current_user.ID)
            #return redirect(url_for('base_blueprint.route_default')) # 怎么能重定向到跟目录呢
            return redirect(url_for('home_blueprint.recommend')) # 登录验证成功，定向到主页面
        return render_template('errors/page_403.html')
    elif 'create_account' in request.form:
        login_form = LoginForm(request.form)
        username = str(request.form['username'])
        password = str(request.form['password'])

        # user = User(**request.form)
        # db.session.add(user)
        # db.session.commit()
        return redirect(url_for('base_blueprint.login'))
    if not current_user.is_authenticated:
        return render_template(
            'login/login.html',
            login_form=login_form,
            create_account_form=create_account_form
        )
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", current_user.ID)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500