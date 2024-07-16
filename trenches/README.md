## 1. Create a Python Virtual Environment
First, create a virtual environment to manage your project's dependencies.

`python -m venv env` 

## 2. Activate the Virtual Environment

Activate the virtual environment. The command varies depending on your operating system.

**For Windows:**

`.\env\Scripts\activate`

**For macOS and Linux:**

`source env/bin/activate` 

## 3. Install Required Packages

Install the necessary packages listed in your `requirements.txt` file.

`pip install -r requirements.txt` 

## 4. Run Your Flask Application

Run your Flask application using the following command:

`flask --app app run` 

## 5. Access the Application in Your Browser

Open your web browser and go to:

`http://127.0.0.1:8000/apology`
