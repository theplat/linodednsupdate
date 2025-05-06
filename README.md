# Linode DNS Updater

A Django-based application that automatically updates DNS records in Linode's DNS Manager. This application is designed to be run as a Docker container and can be used to maintain dynamic DNS records.

## Currently working
- Input API key and store in DB
- default creds uid: admin  pass: temppass      (UPDATE THIS)
- runs on port 8000
- shows list of all domains accessable via API key and allows for updating A names either via manual input or by webcheck for current IP
- password changing. Though I don't believe the DB will, as of yet, survive a kill and restart of the container


## Features To Come

- Automatic DNS record updates for Linode DNS Manager
- Configurable update intervals
- Support for multiple domains and records
- Secure API key management
- Docker containerization
- implement persistant sortage for DB

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


## License

MIT License 
