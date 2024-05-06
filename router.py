from decsvr import DecServerRouter, ContentType, HttpException
import os
import io
import uuid
from cgi import FieldStorage

TMP_STORAGE = 'tmp/'
DATA_STORAGE = 'data/'

def parse_multipart_form(headers, body):
    fp = io.BytesIO(body)
    environ = {'REQUEST_METHOD': 'POST'}

    low_headers = {}
    for key in headers:
        low_headers[key.lower()] = headers[key]

    fs = FieldStorage(fp=fp, environ=environ, headers=low_headers)

    return fs

router = DecServerRouter.DecServerRouter()

@router.get('/api/v1/hello')
def hello(req):
    return {
        'message': 'Hello, World!'
    }

@router.post('/api/upload', content_type=ContentType.APPLICATION_JSON)
def echo(req):
    fs = parse_multipart_form(req.headers, req.body)
    path_list = []
    
    for f in fs.list:
        prefix = uuid.uuid4().hex
        extension = f.filename.split('.')[-1]
        path = prefix + '.' + extension

        with open(TMP_STORAGE + path, 'wb') as o:
            o.write(f.value)
        
        path_list.append(path)

    return {
        'path_list': path_list
    }

@router.put('/api/move', content_type=ContentType.APPLICATION_JSON, reqiure_params=['from', 'to'])
def move(req):
    from_path = TMP_STORAGE + req.query['from'][0]
    to_path = DATA_STORAGE + req.query['to'][0].decode('utf-8')

    if not os.path.isfile(from_path):
        raise HttpException.Http404Exception()

    # if to_path includes ".." then it is not allowed
    if '..' in to_path:
        raise HttpException.Http403Exception()

    to_dir = os.path.dirname(to_path)
    if not os.path.isdir(to_dir):
        os.makedirs(to_dir)

    os.rename(from_path, to_path)

    return {
        'new_path': to_path
    }