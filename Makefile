install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

tests:
	pytest test/

format:
	autopep8 --in-place --recursive Learnia_whatsapp/
	autopep8 --in-place --recursive delete_blobs/
	black Learnia_whatsapp/
	black delete_blobs/

lint:
	pylint --disable=R,C Learnia_whatsapp/*.py
	pylint --disable=R,C delete_blobs/*.py

all: install lint