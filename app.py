import os
import sys
from flask import Flask, request

app = Flask(__name__)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('test.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        app.run(port=sys.argv[1])
    elif 'PORT' in os.environ:
        app.run(port=os.environ['PORT'])
    else:
        app.run()


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f'Method: {request.method}. Url: {request.url}. Data: {request.data}')
    return 'Error. Wrong path.'


@app.errorhandler(405)
def method_not_allowed(e):
    app.logger.error(
        f'Method: {request.method}. Message: Error, method not allowed. Url: {request.url}. Data: {request.data}')
    return 'Error. Method Not Allowed.'


@app.route('/api', methods=['GET'])
def api_view():
    if request.method != 'GET':
        app.logger.error(f'Method: {request.method}. Url: {request.url}. Data: {request.data}')
    else:
        app.logger.info(f'Method: {request.method}. Url: {request.url}. Data: {request.data}')
        try:
            if 'invalid' in request.args and request.args['invalid'] == '1':
                raise Exception('Error. Parameter invalid = 1.')
            process1(request.args)
            process2(request.args)
            process3(request.args)
            return "ok"
        except Exception as e:
            app.logger.error(f'Message: {e.__str__()}')
            return e.__str__()


def process1(args):
    app.logger.info(f'Process1 started')
    pass


def process2(args):
    app.logger.info(f'Process2 started')
    if 'notawaiting' in args and args['notawaiting'] == '1':
        raise Exception('Error. Parameter notawaiting = 1.')


def process3(args):
    app.logger.info(f'Process3 started')
