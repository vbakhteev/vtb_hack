cp -r ../api/src .
docker build -t topic_calculation -f dockerfiles/Dockerfile_tagger .
