SHELL:=/bin/bash

.ONESHELL:
.DEFAULT=all
.PHONY: help test

export VERSION 			:= 0.1
export PROJECT_NAME := notebook_cloze
export ADDON_PATH := ${HOME}/Library/Application\ Support/Anki2/addons
export MENU_NAME := Notebook\ Cloze
help: ## This help.
	@echo "CURRENT VERSION: ${VERSION}"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## copy files to anki add on folder
	# launching docker containers
	mkdir -p ${ADDON_PATH}/${PROJECT_NAME}
	cp -rf ./src/. ${ADDON_PATH}/${PROJECT_NAME}/.
	cp ./notebook_cloze.py ${ADDON_PATH}/${MENU_NAME}.py
