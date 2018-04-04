#! /usr/bin/env bash

export C_FORCE_ROOT="true"
celery -A main.celery worker -l info
