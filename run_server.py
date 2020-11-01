import argparse
from poke_api import create_app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Welcome to pokermon api!!')

    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port number to run the server')
    parser.add_argument('-d', '--debug', const=True,
                        default=True, nargs='?', help='turn on debugging')

    parser.add_argument('--migrate', const=True,
                        default=False, nargs='?', help='run migrations')
    args = parser.parse_args()

    app = create_app(args.migrate)

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
