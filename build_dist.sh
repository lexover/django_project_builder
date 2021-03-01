#############################################################
#       Check python command and version 3                  #
#############################################################
function get_python_command {
    version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(3.+)')
    if [[ -z "$version" ]]; then
        version=$(python -V 2>&1 | grep -Po '(?<=Python )(3.+)')
        if [[ -n "$version" ]]; then
            python_command="python"
        fi
    else
        python_command="python3"
    fi
    echo "$python_command"
}

#############################################################
#       Build django_creator in 'dist' folder.              #
#############################################################
ENV_DIR=venv
if [ -d "$ENV_DIR" ]; then
  echo "Dir '$ENV_DIR' exist, activate venv"
  source venv/bin/activate
  
else
  echo "Dir '$ENV_DIR' doesn't exist, start to create venv and install requirements"
  python_command=$( get_python_command )
  if [ -z "$python_command" ]; then
    echo "Python 3 not found. The programm cannot be continued"
    exit 1 
  fi
  $python_command -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi


echo "Create 'django_creator' package"
python -m pep517.build .

echo "Copy 'create.sh' to 'dist'"
cp start_project.sh dist/start_project.sh
