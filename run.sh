# Tag of the Docker image
IMAGE_TAG="tczhong/my_telegram_bot"

# Find the container ID of the running container with the specified image tag
CONTAINER_ID=$(sudo docker ps -q --filter "ancestor=$IMAGE_TAG")

# Check if the container ID is not empty
if [ -n "$CONTAINER_ID" ]; then
    echo "Stopping container with ID $CONTAINER_ID..."
    sudo docker stop $CONTAINER_ID
else
    echo "No running container found for image $IMAGE_TAG"
fi

# Build a new Docker image with the same tag
echo "Building a new Docker image with tag $IMAGE_TAG..."
sudo docker build -t $IMAGE_TAG .

echo "Build process completed."

sudo docker run $IMAGE_TAG