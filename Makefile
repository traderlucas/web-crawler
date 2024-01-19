export TAP_NAME=$(shell python setup.py --name)
export TAP_VERSION=$(shell python setup.py --version)

lint:
	flake8 tap_produtos_crawler

test:
	python3 -m unittest discover

# Public techindicium/TAP_NAME:TAP_VERSION (requires TAP_NAME)
build_tap:
	docker build -f Dockerfile -t techindicium/$(TAP_NAME):$(TAP_VERSION) -t techindicium/$(TAP_NAME):latest --build-arg TAP_NAME=$(TAP_NAME)  --build-arg TAP_FOLDER=$(subst -,_,$(TAP_NAME)) .

publish_tap: build_tap
	docker login -u $(DOCKER_HUB_USER) -p $(DOCKER_HUB_PASSWORD)
	docker push techindicium/$(TAP_NAME):$(TAP_VERSION)
	docker push techindicium/$(TAP_NAME):latest