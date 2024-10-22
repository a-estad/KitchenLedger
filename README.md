How to run:
1. Create a virtual environment: python -m venv .venv
2. Activate the environment: .venv\Scripts\activate
3. Install the requirements: pip install -r requirements.txt
4. Apply migrations: python manage.py migrate
5. Run the sever: python manage.py runserver
6. Run the frontend: npm start --prefix frontend
6. Deactivate the virtual environment: deactivate

DB diagram
![db diagram](dbdiagram.PNG)