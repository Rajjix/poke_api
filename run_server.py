import argparse
from poke_api import app



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Welcome to pokermon api!!')

    parser.add_argument('-p', '--port', default=5000, type=int, help='port number to run the server')
    parser.add_argument('-d', '--debug', const=True, default=True, nargs='?', help='turn on debugging')

    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)


