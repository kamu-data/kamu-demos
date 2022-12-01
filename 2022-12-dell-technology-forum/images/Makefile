IMAGE_JUPYTER=docker.io/kamudata/demo-2022-12-dtf-jupyter:0.1.0

jupyter:
	docker build \
		-t $(IMAGE_JUPYTER) \
		.

jupyter-push:
	docker push $(IMAGE_JUPYTER)

jupyter-version:
	@echo $(IMAGE_JUPYTER)
