## GoCode

**GoCode** is an innovative platform for programming practice, created in the spirit of well-known services like LeetCode. This project offers users a wide range of tasks to solve online, helping them develop skills in algorithms, coding, and testing solutions.

### Key Features of GoCode:

1. **User-friendly Task System**:
   - Users can choose tasks based on difficulty: *Easy*, *Medium*, *Hard* (EASY, MEDIUM, HARD).
   - Each task includes detailed descriptions, constraints, and built-in tests.
   - The ability to submit solutions for evaluation, where automated tests are run on the server.

2. **Account System**:
   - Support for user profiles with avatars, descriptions, and achievement histories.

3. **Tools for Programmers**:
   - Support for custom tests via the web interface.
   - Logging of solution attempts with visual success statistics.
   - A built-in ranking system and status display for tasks (solved, not solved).

4. **Technological Foundation**:
   - Backend built on Django, with PostgreSQL as the database.
   - Docker containerization for reliable and secure execution of solutions.
   - Data handling between containers using shared JSON files through a common volume.

5. **Minimalist Design**:
   - The user interface is designed with a focus on simplicity and efficiency.
   - A minimalist logo inspired by LeetCode's style.

6. **Reliability**:
   - To ensure the server can handle load during task testing, it has been optimized with a queue system.

7. **Ease of use**:
   - In order to lift such a container you will only have to do a couple of steps

GoCode is ideal for both beginner programmers and experienced developers looking to refine their skills and compete with others. It's the perfect platform for learning, practicing, and professional growth.

----

## How to raise this platform?
### **instructions:**

#### 1. Сopy the repository
```git
git clone https://github.com/snickyyy/GoCode.git
```
#### 1. Load the .env file
```dotenv
Fields:

MODE=
DJANGO_SETTINGS_MODULE=
SECRET_KEY=

LOCAL_PORT=
WSGI_WORKERS=
WSGI_PORT=
WSGI_LOG_LEVEL=

CELERY_LOG_LEVEL=
CELERY_WORKERS_NUMBER=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=

PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=

MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
MONGO_INITDB_DATABASE=

ME_CONFIG_MONGODB_SERVER=
ME_CONFIG_MONGODB_PORT=
ME_CONFIG_MONGODB_ADMINUSERNAME=
ME_CONFIG_MONGODB_ADMINPASSWORD=
ME_CONFIG_BASICAUTH_USERNAME=
ME_CONFIG_BASICAUTH_PASSWORD=

REDIS_DB=
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=


just copy and fill these fields
```
#### 3. Adjust the files (Dockerfile, docker-compose ...) to suit you
#### 4. To start services, enter into the console:
```shell
docker-compose up --build
```
#### *(as needed) you can generate files for tests (app.models.Model.generate...), before that I advise you to look at these files






