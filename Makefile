install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

tests:
	pytest test/

format:
	autopep8 --in-place --recursive DesarrolloColibri/
	autopep8 --in-place --recursive delete_blobs/
	black DesarrolloColibri/
	black delete_blobs/

lint:
	pylint --disable=R,C DesarrolloColibri/*.py
	pylint --disable=R,C delete_blobs/*.py

all: install lint