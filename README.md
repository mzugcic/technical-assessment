## Fygo task

Here is a solution to a task which included creating APIs for:
- user token authentication
- handling & viewing operations
- viewing user balance

#### Used technologies
- [Python 3.7.9](https://www.python.org/downloads/release/python-379/)
- [PostgreSQL 12.6](https://www.postgresql.org/docs/12/index.html)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [Django 3.2.5](https://docs.djangoproject.com/en/3.2/)
- [Django REST Framework 3.12.4](https://www.django-rest-framework.org/)
- [Postman](https://www.postman.com/)

### Runing the project
To run the project you have to have _Python_, _PostgreSQL_ & _virtualenwrapper_ (you can use
 any tool for creating virtual environments for Python) installed on your machine. Please reference the
  documentation on the provided links for further information. _Django_ will be installed inside
   of the virtual environment with all the libraries needed for the project.
   
After you have everything of the above set up and working follow the next steps:
1. Create a virtual environment and call it whatever you want

2. Activate the same - if you used the same technologies as I did run:
    ```
    workon <env_name>
    ```
   
3. From the root of the project run:
    ```
    pip install -r requirements.txt
    ```
   This will also install Django.

4. Set up your environment variables as is shown in the _.env.example_ file & apply them by
 calling the next command from the project root folder:
    ```
   source .env
   ```

You should now be ready to run & test the project with the next command:
 ```
 python manage.py runserver
```

No UI was implemented expect for the default Django admin & DRF that work out of the box.

### APIs

The implemented APIs with request & response examples:
- obtain user token - POST - URL [127.0.0.1:8000/api/token/obtain/](127.0.0.1:8000/api/token/obtain/)
    - request
    ```
    {
        "username": "user",
        "password": "pass"
    }
  ```
    - response
     ```
    {
        "token": "9dba321b3cb51886bc0dbd88c578056ccc263e40"
    }
  ```

- list of operations done for the authenticated user with pagination - GET - local URL [127.0.0.1
:8000/api/operations/](127.0.0.1:8000/api/operations/)
    - request - empty

    - response
     ```
    {
        "count": 22,
        "next": "http://127.0.0.1:8000/api/operations/?p=2",
        "previous": null,
        "results": [
            {
                "transaction_id": null,
                "amount": "-125.45",
                "created": "2021-07-14T01:37:39.246643Z",
                "type": "Withdrawal"
            },
            {
                "transaction_id": 21,
                "amount": "242.00",
                "created": "2021-07-14T01:39:25Z",
                "type": "Purchase"
            }
        ]
    }
  ```

- users current wallet balance - GET - URL [127.0.0.1:8000/api/balance/](127.0.0.1:8000/api/balance/)
    - request - empty

    - response
     ```
    {
        "balance": "20.55"
    }
  ```

- funds withdrawal - POST - URL [127.0.0.1:8000/api/withdrawal/](127.0.0.1:8000/api/withdrawal/)
    - request
    ```
    {
        "amount": 1.14
    }
  ```
    - response
     ```
    {
        "msg": "Your withdrawal was successful."
    }
  ```

- incoming transactions handling - POST - URL [127.0.0.1:8000/api/transactions/](127.0.0.1:8000/api/transactions/)
    - request
    ```
    {
        "user_id": 1,
        "transaction_id": 3213,
        "amount": -520,
        "created": "2021-10-10 15:15:15.0025"
    }
  ```
    - response
    ```
    {
        "transaction_id": 3213,
        "amount": "-520.00",
        "created": "2021-07-14T03:10:36.551056Z",
        "type": "Refund",
        "user_id": 1
    }
  ```

### Deployment instructions
For deployment I would use Heroku because I used it before. 

Steps for deployment:
- set up the Heroku architecture
- add needed add-ons if any & set up environment variables
- export branch differences that happened between deployments using a tool that lists all commits that appeared after the last release
  - This information would be linked in the release notes, although for the first deploy they
   would not exist
- deploy through Git & Heroku CLI & Heroku UI

### Development duration
For the complete project as can be seen in the repo it took me about 4 and a half hours.

### Questions/issues/thoughts
Some of these are maybe not as much questions as they were thoughts during & after development.

These are in no particular order:
1. Should I maybe use the DRF `ViewSet` for all operations and handle them in one place with one
 serializer? It was faster & easier not using it now.
2. Since I was using Postman & DRF also recommended it, I changed `Authorization: Token <token>` to
 `Authorization: Bearer <token>` for sending the token headers for authentication.
3. Should I add a field validator or some other validation on serializers for the amount field to
 keep it DRY?
4. Responses should probably be different for APIs.
5. Maybe I got it wrong, but I was looking at the operations like this:
    - **Purchase** - the customer spends money & and it se removed from his balance
        - Shouldn't the value then be **negative**?
    - **Refund** - the customer gets money back to his balance
        - Shouldn't the value then be **positive**?
    - **Withdrawal** - the customer withdraws money from his account & the value is **negative
    ** as said in the assessment description
        - Did I get it wrong and this actually means the customer is withdrawing his payment? Is
         the payment in a state of pending?
