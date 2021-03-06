.PHONY: help

.DEFAULT_GOAL := help

PROJECT_ID := ${PROJECT_ID}

ENV=dev
GCR_LETTER=jty67w5vzq
CLOUD_RUN_FQDN=https://mc-chimera-$(ENV)-$(GCR_LETTER)-an.a.run.app


build: ## build
	docker compose build

server: build ## start server
	docker compose up $(shell basename $(PWD))

test: build ## test
	docker compose run --rm $(shell basename $(PWD)) \
		pytest -v tests

curl_to_local: ## curl to local (TXT)
	curl -X POST "http://localhost:18001/" \
                -H "accept: */*" \
                -H "Content-Type: application/json" \
                --data-raw '$(TXT)'

curl_to_cloud_run: ## curl to Cloud Run (hint: ENV=pr-xxx)
	curl "$(CLOUD_RUN_FQDN)" \
		-H "accept: application/json" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer $(shell gcloud auth print-identity-token)"

build_and_push_git_lfs: ## build and push git lfs image (PROJECT_ID)
	echo $(PROJECT_ID) | grep $(PROJECT_ID)
	docker build -t gcr.io/$(PROJECT_ID)/git-lfs ./git-lfs/
	docker push gcr.io/$(PROJECT_ID)/git-lfs

help: ## help lists
	@grep -E '^[a-zA-Z_0-9-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

