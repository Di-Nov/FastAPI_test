help:
	@echo 'Makefile for managing web application                              '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo ' make build            build images                                '
	@echo ' make up               creates containers and starts service       '
	@echo ' make start            starts service containers                   '
	@echo ' make stop             stops service containers                    '
	@echo ' make down             stops service and removes containers        '
	@echo '                                                                   '
	@echo ' make migration        create migration m="message"                '
	@echo ' make migrate-up       run all migration                           '
	@echo ' make migrate-dow      roll back last migration                    '
	@echo ' make test             run tests                                   '
	@echo ' make test-cov         run tests with coverage.py                  '
	@echo ' make test-fast        run tests without migrations                '
	@echo ' make lint             run flake8 linter                           '
	@echo '                                                                   '
	@echo ' make attach           attach to process inside service            '
	@echo ' make logs             see container logs                          '
	@echo ' make shell            connect to api container in new bash shell  '
	@echo ' make shell-ipython    connect to api container in new bash shell  '
	@echo ' make shell-db         shell into psql inside database container   '
	@echo ' make view-dash        view task queue dashboardd                  '
	@echo '                                                                   '

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

shell: ## Shell into web container
	docker-compose exec scheduler bash

shell-root:  # Shell into web container as root
	docker-compose exec -u root scheduler bash

shell-ipython: ## Shell into ipython with falcon context
	docker-compose exec scheduler ipython

shell-db: ## Shell into postgres process inside db container
	docker-compose exec db psql -w --username "sivdev_user" --dbname "airflow"

migration: ## Create migrations using alembic
	docker-compose exec api alembic revision --autogenerate -m "$(m)"

migrate-up: ## Run migrations using alembic
	docker-compose exec api alembic upgrade head

migrate-down: ## Rollback migrations using alembic
	docker-compose exec api alembic downgrade -1

test: migrate-up
	docker-compose exec api pytest

test_fast:
	docker-compose exec api pytest

test-cov: migrate-up
	docker-compose exec api pytest --verbose --cov

test-cov-view: migrate-up
	docker-compose exec api pytest --cov --cov-report html && open ./htmlcov/index.html

test-fast: ## Can pass in parameters using p=''
	docker-compose exec api pytest $(p)

view-dash:
	open http://0.0.0.0:9181/

# Flake 8
# options: http://flake8.pycqa.org/en/latest/user/options.html
# codes: http://flake8.pycqa.org/en/latest/user/error-codes.html
max_line_length = 99
lint: up
	docker-compose exec api flake8 \
		--max-line-length $(max_line_length)

mypy:
	docker-compose exec api mypy .