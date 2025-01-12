# Configurable Variables
PYTHON_NAME := python
VENV_NAME := .venv
ENTRY_POINT_NAME := main
REQUIREMENTS_FILE_NAME := requirements

# VENV Paths
VENV_PATH_WINDOWS := $(VENV_NAME)\Scripts
VENV_PATH_UNIX := $(VENV_NAME)/bin

# Execute Custom Commands
execute_custom:
	echo 'run command 1'; \
	echo 'run command 2';

# Setup VENV
setup_venv:
ifeq ($(OS),Windows_NT)
	if not exist $(VENV_NAME) $(PYTHON_NAME) -m venv $(VENV_NAME) && \
	$(VENV_PATH_WINDOWS)\python -m pip install --upgrade pip && \
	$(VENV_PATH_WINDOWS)\pip install pipdeptree
else
	test -d $(VENV_NAME) || $(PYTHON_NAME) -m venv $(VENV_NAME) && \
	$(VENV_PATH_UNIX)/python -m pip install --upgrade pip && \
	$(VENV_PATH_UNIX)/pip install pipdeptree
endif

# Install Requirements
install_packages: setup_venv
ifeq ($(OS),Windows_NT)
	$(VENV_PATH_WINDOWS)\pip install -r $(REQUIREMENTS_FILE_NAME).txt && \
	$(VENV_PATH_WINDOWS)\pip freeze > $(REQUIREMENTS_FILE_NAME)-lock.txt && \
	$(VENV_PATH_WINDOWS)\python -m pipdeptree && \
	$(VENV_PATH_WINDOWS)\python -m pipdeptree > $(REQUIREMENTS_FILE_NAME)-pipdeptree.txt
else
	$(VENV_PATH_UNIX)/pip install -r $(REQUIREMENTS_FILE_NAME).txt && \
	$(VENV_PATH_UNIX)/pip freeze > $(REQUIREMENTS_FILE_NAME)-lock.txt && \
	$(VENV_PATH_UNIX)/python -m pipdeptree && \
	$(VENV_PATH_UNIX)/python -m pipdeptree > $(REQUIREMENTS_FILE_NAME)-pipdeptree.txt
endif

# Show Installed Packages
show_packages: setup_venv
ifeq ($(OS),Windows_NT)
	$(VENV_PATH_WINDOWS)\python -m pipdeptree
else
	$(VENV_PATH_UNIX)/python -m pipdeptree
endif

# Uninstall Virtual Environment
clean_venv:
ifeq ($(OS),Windows_NT)
	if exist $(VENV_NAME) rmdir /s /q $(VENV_NAME)
else
	test -d $(VENV_NAME) && rm -rf $(VENV_NAME)
endif
