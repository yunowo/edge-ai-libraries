# How to Build from Source

This section shows how to build the Video Search and Summary sample application from source.

> **Note:** The dependent microservices must be built separately from their respective microservice folders.

## Prerequisites

1. Address all [prerequisites](./get-started.md#-prerequisites).
2. If the setup is behind a proxy, ensure `http_proxy`, `https_proxy`, and `no_proxy` are properly set on the shell.

## Steps to Build from Source

1. **Clone the Repository**:
    - Clone the Video Summary Sample Application repository:
      ```bash
      git clone https://github.com/open-edge-platform/edge-ai-libraries.git
      ```

2. **Navigate to the Directory**:
    - Go to the directory where the Dockerfile is located:
      ```bash
      cd edge-ai-libraries/sample-applications/video-search-and-summarization
      ```

3. **Build the Docker Image**:

    If you need to customize the application or build your own images, you can use the `build.sh` script included in the repository.

    ### ⚙️ Customizing Build Configuration

    The application uses registry URL, project name, and tag to build the images.

      ```bash
      export REGISTRY_URL=<your-container-registry-url>    # e.g. "docker.io/username/"
      export PROJECT_NAME=<your-project-name>              # e.g. "video-search-and-summarization"
      export TAG=<your-tag>                                # e.g. "rc4" or "latest"
      ```

    > **_IMPORTANT:_** These variables control how image names are constructed. If `REGISTRY_URL` is **docker.io/username/** and `PROJECT_NAME` is **video-search-and-summarization**, an image would be pulled or built as **docker.io/username/video-search-and-summarization/\<application-name>:tag**. The `<application-name>` is hardcoded in _image_ field of each service in all docker compose files. If `REGISTRY_URL` or `PROJECT_NAME` are not set, blank string will be used to construct the image name. If `TAG` is not set, **latest** will be used by default.

    ### 🔨 Building Images

    The build script provides options to build and push the images. Build script provides option to build only the application microservices or build together with all the dependent microservices. The dependent microservices are the following microservices: [Multimodal Embedding](../../../../microservices/multimodal-embedding-serving/), [Audio Analyzer](../../../../microservices/audio-analyzer/), [VDMS based data preparation](../../../../microservices/visual-data-preparation-for-retrieval/vdms/), and [VLM microservice](../../../../microservices/vlm-openvino-serving/). 

    ```bash

    # Build the sample applications services
    ./build.sh 

    # Build the sample applications dependencies
    ./build.sh --dependencies

    # Push all built images to the configured registry
    ./build.sh --push
    ```

    After building, you can verify the created images with:

    ```bash
    docker images | grep <your-project-name>
    ```


4. **Run the Docker Container**:

    The Video Search and Summary application offers multiple stacks and deployment options, to verify the newly created images run the below command to run the application:

    ```bash
    source setup.sh --summary
    ```

5. 🌐 Accessing the Application

    After successfully starting the application, open a browser and go to `http://<host-ip>:12345` to access the application dashboard.

## Verification

- Ensure that the application is running by checking the Docker container status:
  ```bash
  docker ps
  ```
- Access the application dashboard and verify that it is functioning as expected.

## Troubleshooting

- If you encounter any issues during the build or run process, check the Docker logs for errors:
  ```bash
  docker logs <container-id>
  ```
