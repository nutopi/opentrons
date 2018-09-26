# opentrons app makefile

SHELL := /bin/bash

# add node_modules/.bin to PATH
PATH := $(shell cd .. && yarn bin):$(PATH)

# set NODE_ENV for a command with $(env)=environment
env := cross-env NODE_ENV

DEFS_BUILD_DIR := build
CLI_BUILD_DIR := js/cli/dist

#######################################

.PHONY: install
install:
	yarn
	$(MAKE) build

.PHONY: build
build:
	shx mkdir -p $(DEFS_BUILD_DIR) && node js/scripts/build.js $(DEFS_BUILD_DIR)

.PHONY: dist-cli
dist-cli:
	$(env)=production webpack --profile

.PHONY: clean
clean:
	shx rm -rf $(DEFS_BUILD_DIR) $(CLI_BUILD_DIR)
