###Web-Based Workflow System
This project is an implementation of a web-based workflow system using Django and Python 3.7. The goal is to build a system capable of handling user input via HTML forms, process the input, and present the result in a visual manner.

**The application implements the following features:

*Customer Information
The user enters customer information through a simple HTML form. The information captured includes:

First name
Last name
Date of Birth
Excel File Upload
In addition to the customer information, the user uploads an Excel file containing the customer's financial income and expenses for the last 12 months.

*Temporal Graph
The system processes the uploaded Excel file and renders a temporal graph showing the customer's income and expenditure for the last 12 months.

*Extensibility
The design of the workflow system is made keeping extensibility in mind. The aim is to make the workflow easy to extend or change. The reasoning and architecture decisions are documented in the code as comments.

*Restraints and Considerations
The system is designed for a single user. There's no requirement for login or user management features.
The data storage solution implemented in this system is simple. An SQLite database is used for storing customer and financial data.
How to Run the Project
This project uses Django web framework. Please make sure you have Python 3.7 and pip installed on your system.

1.Clone the repository
https://github.com/samukele-dev/WorkflowSystem.git

2.Set up a virtual environment and install the dependencies

Copy code
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3.Run the Django migrations to set up your database

python manage.py makemigrations
python manage.py migrate

4.Start the Django development server

python manage.py runserver

5.Open your web browser and visit http://127.0.0.1:8000/

*Tests
To run the tests for the application, you can use Django's built-in test command:

python manage.py test

Please refer to the comments in the code and this README file to understand the reasoning behind architectural decisions and the workflow of the system. The project is open to extension and modifications as per the requirements.






