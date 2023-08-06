import jwt
from jwt.exceptions import ExpiredSignatureError
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .settings import REDIRECT_URL, JWT_PUB_KEY, REQUIRED_ROLES


def jwt_check_redirect_view(request: HttpRequest):
    jwt_token = request.GET.get('TOKEN')
    if jwt_token is None:
        return render(request, template_name='jwt-redirect-error.html',
                      context={
                          'status_code': 401,
                          'reason': 'Not Authorized',
                          'back_url': REDIRECT_URL,
                          'text': '''
                          <h3>没有提供TOKEN参数，认证失败！</h3>
                          '''
                      },
                      status=401)

    header = jwt.get_unverified_header(jwt_token)
    if 'alg' not in header or header['alg'] != 'RS256':
        return render(request, template_name='jwt-redirect-error.html',
                      context={
                          'status_code': 401,
                          'reason': 'Not Authorized',
                          'back_url': REDIRECT_URL,
                          'text': '''
                          <h3>JWT的格式不支持，认证失败！</h3>
                          '''
                      })

    try:
        decoded = jwt.decode(jwt_token, JWT_PUB_KEY, algorithms=["RS256"])
    except ExpiredSignatureError:
        return render(request, template_name='jwt-redirect-error.html',
                      context={
                          'status_code': 401,
                          'reason': 'Not Authorized',
                          'back_url': REDIRECT_URL,
                          'text': '''
                          <p>你的TOKEN已过期，登录失败！</p>
                          '''
                      },
                      status=401)

    roles = decoded.get('roles', [])
    if not isinstance(roles, list):
        return render(request, template_name='jwt-redirect-error.html',
                      context={
                          'status_code': 401,
                          'reason': 'Not Authorized',
                          'back_url': REDIRECT_URL,
                          'text': '''
                          <h3>JWT的格式不支持，认证失败！</h3>
                          '''
                      })

    missing_roles = [role for role in REQUIRED_ROLES if role not in roles]
    if len(missing_roles) > 0:
        html_roles = [f'<li>{role}</li>' for role in missing_roles]
        return render(request, template_name='jwt-redirect-error.html',
                      context={
                          'status_code': 403,
                          'reason': 'Forbidden',
                          'back_url': REDIRECT_URL,
                          'text': f'''
                          <p>你缺少了登录此应用所必须的角色：</p>
                          <ul>
                          {''.join(html_roles)}
                          </ul>
                          <p>公司的管理员可以处理此问题。</p>
                          '''
                      })

    response: HttpResponse = render(request, 'redirect.html', {
        'redirect_url': REDIRECT_URL
    })
    response.set_cookie('JWT_TOKEN', jwt_token)

    return response




