#!/bin/bash

# Return checked input value. 
# param_1: printed text
# param_2: regular expression to check
# param_3: message if input invalid 
function checked_input {
	read -p "$1": value 
	while true; do	
		if ! [[ $value =~ $2 ]]; then
			read -p "$3": value 
		else
			break
		fi
	done
	echo "$value"
}


# Create directories and virtual environment. 
# param_1: project name 
function create_venv {
	echo Create virtual environment
	mkdir -p $1/app
	cd $1
	python3 -m venv venv
}

# Activate virtual environment in current directory
function activate_venv {
  source venv/bin/activate
}

# Install Django
function install_django {
	echo Update pip and install wheel
	pip install --upgrade pip
	pip install wheel

	echo "Do you wish to specify version of django (or use latest)?"
	select yn in "Yes" "No"; do
		case $yn in
			Yes ) django_version=$(checked_input "Version of Django" "^[0-9]{1}\.[0-9]{1}\.[0-9]{1,2}$" "Invalid version x.x.xx possble");
			      echo "Install Django v${django_version}"
			      pip install Django==$django_version;
			      break;;
			No )  echo "Install Django latest "
			      pip install Django;
			      break;;  
		esac
	done
}

# Create Django project and application
function create_project_with_app {
	cd "app"
  pwd
	django-admin startproject $1 .
	python manage.py startapp $2
	cd ..
}

#####################################################################################################
#	MAIN CODE										    #
#####################################################################################################

echo This is DRF project creator. Let create a new project.
project_name=$(checked_input "Project name" ^[a-z_]+$ "Invalid project name only [a-z_] possble")
app_name=$(checked_input "Application name" ^[a-z_]+$ "Invalid app name only [a-z_] possble")

create_venv $project_name

activate_venv

install_django

create_project_with_app "$project_name" "$app_name"

cd ..

pip install PyInquirer
pip install django_project_builder-0.0.1-py3-none-any.whl

python -m dp_builder -p "$project_name" -a "$app_name"

echo "The project ${project_name} was built successfull."
echo "You can go to app dir: 'cd ${poject_name}/app' and start it: 'python manage.py runserver'"
echo "If you use Docker build go to project dir: 'cd ${project_name}' and run: 'docker-compose up --build -d'"
