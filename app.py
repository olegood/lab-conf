from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return health()


@app.route('/health', methods=['GET'])
def health():
    return {"status": "UP"}


@app.route('/configs/<service>/<environment>', methods=['GET'])
def get_config(service, environment):
    return f'GET(Config: {service}-{environment})'


@app.route('/configs/<service>/<environment>', methods=['POST'])
def save_config(service, environment):
    return f'POST(Config: {service}-{environment})'


@app.route('/configs/<service>/<environment>/versions', methods=['GET'])
def list_versions(service, environment):
    return f'GET(Versions: {service}-{environment})'


if __name__ == '__main__':
    app.run(debug=True)
