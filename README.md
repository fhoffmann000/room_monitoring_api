# Room Monitoring API

A FastAPI project developed in early 2022 as a learning exercise to explore FastAPI's features and capabilities. The API provides POST and GET endpoints for adding and retrieving room condition data (temperature, humidity, and air quality), which is stored in a PostgreSQL database.

This project utilizes older versions of FastAPI and its dependencies (e.g., FastAPI 0.73.0, Alembic 1.7.6, and Uvicorn 0.15.0) because it was built with the latest versions available at the time. Since this was a personal learning project, it has not been actively maintained or updated to align with newer versions of its dependencies.

Despite its outdated setup, the project demonstrates core concepts like authentication, user roles, and a simple data ingestion pipeline from IoT devices such as a Raspberry Pi. It remains a snapshot of a beginner’s exploration into building APIs with FastAPI.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)

---

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/fhoffmann000/room-monitoring-api.git
   cd room-monitoring-api
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv monitor_env
   source monitor_env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

Follow these steps to set up the project and prepare the database with example data:


#### **1. Create the `.env` File**

In the root directory of the project, create a file named `.env` with the following content:

```plaintext
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Fill in the appropriate values for your PostgreSQL database credentials (`DATABASE_USERNAME`, `DATABASE_PASSWORD`, etc.).

---

#### **2. Prepare the Database and Seed Example Data**

1. **Initialize Alembic:**

   Run the following command to initialize Alembic for database migrations:

   ```bash
   alembic init alembic
   ```

2. **Update Alembic Configuration:**

   Open the `alembic.ini` file and modify the `sqlalchemy.url` setting:

   - Delete the default line:
     ```plaintext
     sqlalchemy.url = driver://user:pass@localhost/dbname
     ```
   - Replace it with an empty value:
     ```plaintext
     sqlalchemy.url =
     ```

3. **Configure Database Connection in `env.py`:**

   Open the `env.py` file in the `alembic` directory and modify it as follows:

   - Import the necessary modules and set the database URL dynamically:
     ```python
     from app.models import Base
     from app.config import settings

     config.set_main_option("sqlalchemy.url", f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")

     target_metadata = Base.metadata
     ```

4. **Run Alembic Migrations:**

   Execute the following commands in sequence:

   - Create an initial migration file:
     ```bash
     alembic revision --autogenerate -m "create tables"
     ```
   - Apply the migration to create the database tables:
     ```bash
     alembic upgrade head
     ```
   - Create a migration file for seeding example data:
     ```bash
     alembic revision -m "insert initial data"
     ```

5. **Edit the Initial Data Migration File:**

   Open the generated migration file for "insert initial data." Note that the **Revision ID** and **Down Revision** values (e.g., `Revision ID: 2c0ed796456f` and `down_revision = '45cd0c3eda49'`) will be unique for each migration. Replace the contents of the file with the following code:

   ```python
   """insert initial data

   Revision ID: <your_revision_id>
   Revises: <your_down_revision_id>
   Create Date: <your_timestamp>

   """
   from alembic import op
   import sqlalchemy as sa
   from sqlalchemy.sql import table, column
   from sqlalchemy import String, Float, Integer, TIMESTAMP
   from random import randint, uniform

   # revision identifiers, used by Alembic.
   revision = '<your_revision_id>'
   down_revision = '<your_down_revision_id>'
   branch_labels = None
   depends_on = None

   data_points = [
       {
           'id': i,
           'location': f'Room {randint(1, 4)}',
           'temperature': round(uniform(18.0, 30.0), 1),
           'air_quality': round(uniform(20.0, 80.0), 1),
           'humidity': round(uniform(40.0, 70.0), 1),
           'created_at': 'now()',
           'owner_id': randint(1, 2)
       }
       for i in range(1, 51)
   ]

   def upgrade():
       op.bulk_insert(
           table(
               'users',
               column('id', Integer),
               column('username', String),
               column('password', String),
               column('usertype', String),
               column('created_at', TIMESTAMP(timezone=True))
           ),
           [
               {'id': 1, 'username': 'raspberry', 'password': '$2b$12$ZnuwS/cFbpe2Qg091YAp4.Q6IuUIn1s/dsGMlomzFp/7zK.bmnxzy', 'usertype': 'write', 'created_at': 'now()'},
               {'id': 2, 'username': 'test_user', 'password': '$2b$12$N71WehDkn6qJYDwg09CgLeNH25dI8BO.OwqQNZHm5G1GSDNWZNQda', 'usertype': 'readonly', 'created_at': 'now()'}
           ]
       )

       op.bulk_insert(
           table(
               'room_data',
               column('id', Integer),
               column('location', String),
               column('temperature', Float),
               column('air_quality', Float),
               column('humidity', Float),
               column('created_at', TIMESTAMP(timezone=True)),
               column('owner_id', Integer)
           ),
           data_points
       )

   def downgrade():
       op.execute("DELETE FROM room_data WHERE id IN (1, 2)")
       op.execute("DELETE FROM users WHERE id IN (1, 2)")
   ```

6. **Apply the Data Migration:**

   Run the following command to seed the example data:

   ```bash
   alembic upgrade head
   ```

7. **Fix the Auto-Increment Sequence for IDs:**

   Execute the following SQL command to adjust the sequence for the `room_data` table:

   ```sql
   SELECT setval('room_data_id_seq', (SELECT MAX(id) FROM room_data));
   ```


Your database is now prepared with tables and example data. You can proceed to start the API and test its functionality.


---


## Usage

Follow these steps to start and test the API and explore its core functionalities:

### **Starting the API**

To start the API, run the following command in your terminal:

```bash
uvicorn app.main:app --reload
```

By default, the API will be accessible locally at `http://127.0.0.1:8000`.

---

### **Testing the API**

The easiest way to explore and test the API is by using **Swagger UI**, which is automatically generated by FastAPI. Open the following link in your browser:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The Swagger UI provides a complete overview of the available endpoints, their expected inputs and outputs, and allows you to interact with the API directly.

---

### **Default Users**

The API comes with two preconfigured users for testing:

1. **Write User**:
   - **Username**: `raspberry`
   - **Password**: `password123`
   - **Permissions**: Can send data to the API.

2. **Read-Only User**:
   - **Username**: `test_user`
   - **Password**: `password456`
   - **Permissions**: Can only retrieve data but not modify it.

---

#### **Available Functionalities**

Once logged in, you can access the following endpoints to interact with the API. Refer to the Swagger UI documentation for detailed descriptions of the required inputs and outputs for each endpoint.

##### **1. Retrieve Data**
- **Endpoint**: `GET /data`  
- **Description**: Retrieve stored room condition data (temperature, humidity, air quality) with support for pagination.

##### **2. Add Data**
- **Endpoint**: `POST /data`  
- **Description**: Add new room condition data to the database. Requires authentication as a write user.

##### **3. Retrieve Users**
- **Endpoint**: `GET /users`  
- **Description**: Retrieve a list of registered users. Requires authentication.

##### **4. Create a Read-Only User**
- **Endpoint**: `POST /users`  
- **Description**: Create a new read-only user for viewing data. This endpoint is accessible even without authentication.

#### **Note on Authentication**

The API uses OAuth2 with JWT tokens for secure access. To use protected endpoints:
1. Log in using the `POST /login` endpoint with your username and password.
2. Retrieve the access token from the response.
3. Include the token in the `Authorization` header when making requests to protected endpoints.

For more details and examples, see the Swagger UI documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
