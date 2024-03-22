install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

tests:
	pytest test/

format:
	autopep8 --in-place --recursive Learnia_whatsapp/
	autopep8 --in-place --recursive delete_blobs/
	autopep8 --in-place --recursive Dialogflow_webhook/
	black Learnia_whatsapp/
	black delete_blobs/
	black delete_blobs/
	black Dialogflow_webhook/

lint:
	pylint --disable=R,C Learnia_whatsapp/*.py
	pylint --disable=R,C delete_blobs/*.py
	pylint --disable=R,C Dialogflow_webhook/*.py

all: install lint