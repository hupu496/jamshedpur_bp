<img width="1572" height="840" alt="ezgif com-speed" src="https://github.com/user-attachments/assets/7add06d1-770e-486e-b79f-494a229f49c5" />
<img width="1357" height="612" alt="head_2" src="https://github.com/user-attachments/assets/b18d46eb-df30-4a84-a24e-a8d1ceadb29a" />
<img width="1572" height="840" alt="head_1" src="https://github.com/user-attachments/assets/88e6be9d-a306-45c1-a5bf-6e8d3b1bb798" />


> 👉 Download the code  

```bash
$ git clone https://github.com/app-generator/django-material-kit.git
$ cd django-material-kit
```

<br />

> 👉 Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                  # Project Configuration  
   |    |-- urls.py                      # Project Routing
   |
   |-- home/
   |    |-- views.py                     # APP Views 
   |    |-- urls.py                      # APP Routing
   |    |-- models.py                    # APP Models 
   |    |-- tests.py                     # Tests  
   |    |-- templates/                   # Theme Customisation 
   |         |-- pages                   # 
   |              |-- custom-index.html  # Custom Footer      
   |     
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

🤝 Hire the Developer
Looking for a custom Django solution for your business? Let's connect!

📧 Email: aadarsh629@gmail.com

📞 Phone: +91 7999669691

💼 Availability: Freelance / Contract Projects Available




