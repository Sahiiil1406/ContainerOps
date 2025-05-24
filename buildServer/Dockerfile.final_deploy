FROM docker:dind

# Install git using apk
RUN apk add --no-cache git python3 py3-pip

WORKDIR /app
COPY main.py .

# Use JSON array for CMD
CMD ["sh", "-c", "git clone $GIT_URL && python3 main.py && cd $(basename $GIT_URL .git) && docker build -t $IMAGE_NAME . && docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD && docker tag $IMAGE_NAME $DOCKER_USERNAME/$IMAGE_NAME && docker push $DOCKER_USERNAME/$IMAGE_NAME"]
