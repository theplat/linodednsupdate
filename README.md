# Linode DNS Updater

A Django-based application that automatically updates DNS records in Linode's DNS Manager. This application is designed to be run as a Docker container and can be used to maintain dynamic DNS records.

## Features

- Automatic DNS record updates for Linode DNS Manager
- Configurable update intervals
- Support for multiple domains and records
- Secure API key management
- Docker containerization

## Requirements

- Python 3.11+
- Django 5.0.2
- Docker (for containerized deployment)
- Linode API key with DNS management permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/linodednsupdate.git
cd linodednsupdate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t linodednsupdate .
```

2. Run the container:
```bash
docker run -d \
  -e LINODE_API_KEY=your_api_key \
  -e ALLOWED_HOSTS=your_domain \
  linodednsupdate
```

## Configuration

The application can be configured using environment variables:

- `LINODE_API_KEY`: Your Linode API key
- `UPDATE_INTERVAL`: How often to check for IP changes (in seconds)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DEBUG`: Set to True for development (default: False)

## License

MIT License 