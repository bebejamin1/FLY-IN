# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbeaurai <bbeaurai@student.42lehavre.fr    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 13:20:39 by bbeaurai          #+#    #+#              #
#    Updated: 2026/05/01 13:20:43 by bbeaurai         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

FLAKE8 = venv/lib/python3.10/site-packages/flake8
MYPY = venv/lib/python3.10/site-packages/mypy
ARCADE = venv/lib/python3.10/site-packages/arcade
TYPING = venv/lib/python3.10/site-packages/typing-extensions

RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
PINK = \033[35m
NC = \033[0m

all : run

venv/bin/activate : 
	@echo ""
	@echo "$(YELLOW)VENV ACTIVATION$(NC)"
	python3 -m venv venv

$(FLAKE8) : 
	@echo ""
	@echo "$(PINK)DEPENDENCY INSTALL"
	@$(PIP) install -q -r requirement.txt

$(MYPY) : 
	@$(PIP) install -q -r requirement.txt
	
$(ARCADE) :
	@$(PIP) install -q -r requirement.txt

$(TYPING) :
	@$(PIP) install -q -r requirement.txt
	
install : venv/bin/activate requirement.txt $(FLAKE8) $(MYPY) $(ARCADE) $(TYPING)


run : install
	@echo ""
	@echo "$(GREEN)LAUNCH IN PROGRESS...$(NC)"
	@$(PYTHON) main.py

debug :
	$(PYTHON) -m pdb main.py

lint : install
	@echo ""
	@echo "$(RED)TESTING FLAKE8 / MYPY...$(NC)"
	@. ./venv/bin/activate && \
	flake8 --exclude venv && \
	mypy . --exclude venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo ""

lint-strict : install
	@echo ""
	@echo "$(RED)TESTING FLAKE8 / MYPY STRICT...$(NC)"
	@. ./venv/bin/activate && \
	flake8 . --exclude venv && \
	mypy . --strict --exclude venv
	@echo ""

clean : 
	@echo ""
	@echo "$(RED)CLEANING...$(NC)"
	@find . -name "__pycache__" -exec rm -rf {} \+
	@find . -name ".mypy_cache" -exec rm -rf {} \+
	@find . -name ".vscode" -exec rm -rf {} \+
	@find . -name "venv" -exec rm -rf {} \+
	@echo "$(GREEN)DELETE [OK]...$(NC)"

uninstall : requirement.txt
	$(PIP) uninstall -r requirement.txt

uninstall_venv :
	rm -rf venv

.PHONY: clean lint run install uninstall
