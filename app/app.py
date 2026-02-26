"""Flask application for managing service configurations.

This application provides a REST API for storing and retrieving
configuration data for different services and environments, with
versioning support.
"""
from flask import Flask, request, jsonify, abort

from models import ConfigCreateRequest, ConfigResponse
from storage import FileConfigStorage

app = Flask(__name__)
repo = FileConfigStorage(base_path="../data")


@app.get("/")
def index():
    """Root endpoint that redirects to health check."""
    return health()


@app.get("/health")
def health():
    """Health check endpoint.
    
    Returns:
        dict: Status dictionary indicating service health.
    """
    return {"status": "UP"}


@app.get("/configs/<service>/<environment>")
def get_config(service, environment):
    """Retrieve configuration for a service and environment.
    
    Args:
        service: Service name.
        environment: Environment name (e.g., "dev", "prod").
        
    Query Parameters:
        version: Optional version UUID. If not provided, returns the latest version.
        
    Returns:
        dict: Configuration data.
        
    Raises:
        404: If configuration is not found.
    """
    version = request.args.get("version")
    config = repo.get(service, environment, version)
    if not config:
        abort(404)
    return jsonify(config)


@app.post("/configs/<service>/<environment>")
def save_config(service, environment):
    """Create a new configuration version for a service and environment.
    
    Args:
        service: Service name.
        environment: Environment name (e.g., "dev", "prod").
        
    Request Body:
        JSON payload with "data" and "created_by" fields.
        
    Returns:
        tuple: Configuration response and HTTP 201 status.
        
    Raises:
        400: If the JSON payload is invalid or missing required fields.
    """
    payload = request.get_json()
    if not payload:
        abort(400, description="Invalid JSON payload")

    try:
        req = ConfigCreateRequest(**payload)
    except Exception as e:
        abort(400, description=str(e))

    created = repo.save(service, environment, req.data, req.created_by)
    return jsonify(ConfigResponse(**created).model_dump()), 201


@app.get("/configs/<service>/<environment>/versions")
def list_versions(service, environment):
    """List all available configuration versions for a service and environment.
    
    Args:
        service: Service name.
        environment: Environment name (e.g., "dev", "prod").
        
    Returns:
        dict: Dictionary containing service, environment, and the list of version UUIDs.
    """
    versions = repo.list_versions(service, environment)
    return {
        "service": service,
        "environment": environment,
        "versions": versions
    }


if __name__ == "__main__":
    app.run(debug=True)
