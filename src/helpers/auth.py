def check_auth(session):
    return session.get('user')