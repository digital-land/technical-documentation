SHELL := bash
.PHONY: init clean

init: 
	npm install

# old commands for plant uml that could be  useful fin the future
# .bin:
# 	@mkdir -p .bin/

# .bin/plantuml.jar: .bin
# 	@echo "Downloading version $(PLANTUML_VERSION) of plantuml"
# 	@curl -sL -o .bin/plantuml.jar "https://github.com/plantuml/plantuml/releases/download/v$(PLANTUML_VERSION)/plantuml-$(PLANTUML_VERSION).jar"

# PLANTUML_VERSION := $(shell curl --silent "https://api.github.com/repos/plantuml/plantuml/releases/latest" | jq -rc '.name | .[1:]')


clean:
	@rm -rf .bin/

serve:
	npx eleventy --serve

build:
	npx eleventy




