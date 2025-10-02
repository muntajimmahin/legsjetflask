# Project Setup Instructions

This guide will walk you through setting up and running the application.

## Prerequisites

Python 3.11.9 

- pip (Python package installer)

## Setup Steps

### 1. Create Python Environment

First, create a virtual environment to isolate your project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

Install all required packages from the requirements file:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Start the application by running:

```bash
python old_app.py
```

The application should now be running and accessible.

### 4. WordPress API Configuration

To configure the WordPress API settings:

- Navigate to the `wp.py` file
- Update the WordPress API configurations as needed
- Modify endpoint URLs, authentication tokens, or other API-related settings

### 5. Create Admin Password

To set up admin credentials:

- Run the admin creation script:
  ```bash
  python create_admin.py
  ```
- Follow the prompts to create your admin password
- Store the credentials securely

## Troubleshooting

- If you encounter permission errors, make sure your virtual environment is activated
- Ensure all dependencies are installed correctly by checking `pip list`
- Verify that Python version is compatible with the requirements

## Additional Notes

- Always activate your virtual environment before running the application
- Keep your `requirements.txt` file updated when adding new dependencies
- Backup your configuration files before making changes

## Support

If you encounter any issues during setup, please check the error messages and ensure all steps have been followed correctly.