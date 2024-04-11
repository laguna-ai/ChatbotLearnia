install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

tests:
	pytest test/

format:
	autopep8 --in-place --recursive Learnia_whatsapp/
	autopep8 --in-place --recursive delete_blobs/
	autopep8 --in-place --recursive Dialogflow_webhook/
	autopep8 --in-place --recursive RAG/
	autopep8 --in-place --recursive simulation/
	autopep8 --in-place --recursive test/
	autopep8 --in-place --Postgres/
	black Learnia_whatsapp/
	black delete_blobs/
	black delete_blobs/
	black Dialogflow_webhook/
	black RAG/
	black simulation/
	black test/
	black Postgres

lint:
	pylint --disable=R,C Learnia_whatsapp/*.py
	pylint --disable=R,C delete_blobs/*.py
	pylint --disable=R,C Dialogflow_webhook/*.py
	pylint --disable=R,C RAG/*py
	pylint --disable=R,C simulation/*py
	pylint --disable=R,C test/*py
	pylint --disable=R,C Postgres/*py

all: install lint