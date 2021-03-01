from PyInquirer import prompt

django_questions = [
    {
        'type': 'checkbox',
        'name': 'libs',
        'message': 'Which packages/settings do you want to use with Django?',
        'choices': [
            {'name': 'drf', 'message': 'Install Django REST Framework'},
            {'name': 'docker', 'message': 'Create docker files for project images build'}
        ]
    }
]

drf_questions = [
    {
        'type': 'checkbox',
        'name': 'libs',
        'message': 'Which packages or settings do you want to use with DRF?',
        'choices': [
            {'name': 'paging', 'message': 'Setup automatic pagination in your project?'},
            {'name': 'simplejwt', 'message': 'Simple JWT to manage tokens'},
        ]
    }
]

is_configure_db = [
    {
        'type': 'confirm',
        'name': 'confirm',
        'message': 'Do you want to configure Postgres DB? (If not default settings will be used)'
    }
]

db_questions = [
    {
        'type': 'input',
        'name': 'db_name',
        'message': 'Database name:',
        'default': 'django_db',
    },
    {
        'type': 'input',
        'name': 'db_user',
        'message': 'DB user name:',
        'default': 'db_user'
    },
    {
        'type': 'password',
        'name': 'db_password',
        'message': 'DB user password:',
    },
]


def get_parameters():
    answers = {'main': prompt(django_questions)['libs']}
    if 'drf' in answers['main']:
        answers['drf'] = prompt(drf_questions)['libs']
    if 'docker' in answers['main']:
        if prompt(is_configure_db)['confirm']:
            answers['db'] = prompt(db_questions)
    return answers
