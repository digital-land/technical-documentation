SHELL := bash
PLANTUML_VERSION := $(shell curl --silent "https://api.github.com/repos/plantuml/plantuml/releases/latest" | jq -rc '.name | .[1:]')
.PHONY: init clean

init: .bin/plantuml.jar

.bin:
	@mkdir -p .bin/

.bin/plantuml.jar: .bin
	@echo "Downloading version $(PLANTUML_VERSION) of plantuml"
	@curl -sL -o .bin/plantuml.jar "https://github.com/plantuml/plantuml/releases/download/v$(PLANTUML_VERSION)/plantuml-$(PLANTUML_VERSION).jar"

clean:
	@rm -rf .bin/

dev: init
	@bundle exec middleman server

build: init
	@bundle exec middleman build
