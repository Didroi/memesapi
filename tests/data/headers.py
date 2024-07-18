from tests.data import token as t


non_auth_header = {'Content-Type': 'application/json'}
auth_header = {
    'Content-Type': 'application/json',
    'authorization': t.tokens['active token']
}
