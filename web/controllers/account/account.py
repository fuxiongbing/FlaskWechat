from flask import Blueprint, request, redirect
from common.libs.Helper import ops_render, iPagination
from common.models.User import User
from application import app
from common.libs.UrlManager import UrlManager

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = User.query

    # if 'mix_kw' in req:
    #     rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
    #     query = query.filter(rule)
    #
    # if 'status' in req and int(req['status']) > -1:
    #     query = query.filter(User.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    # resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", resp_data)


@route_account.route('/info')
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id', 0))
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(reback_url)

    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(reback_url)

    # access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    resp_data['info'] = info
    # resp_data['access_list'] = access_list
    return ops_render("account/info.html", resp_data)


@route_account.route("/set", methods=["GET", "POST"])
def set():
    return ops_render("account/set.html")
