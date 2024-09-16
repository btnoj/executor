GIT_TAG ?= master
TAG ?= latest

.PHONY: executor

executor:
	docker build --build-arg TAG="${GIT_TAG}" -t btnoj/executor -t btnoj/executor:$(TAG) -t ghcr.io/btnoj/executor -t ghcr.io/btnoj/executor:$(TAG) .