FROM ubuntu:latest

RUN apt update && apt upgrade -y
RUN apt install python3-dev cmake git libffi-dev -y

RUN apt install -y liblzma-dev
RUN apt install build-essential -y
RUN apt install libvulkan1 mesa-vulkan-drivers -y

RUN apt install wget -y
RUN wget -qO- https://packages.lunarg.com/lunarg-signing-key-pub.asc | tee /etc/apt/trusted.gpg.d/lunarg.asc
RUN wget -qO /etc/apt/sources.list.d/lunarg-vulkan-jammy.list http://packages.lunarg.com/vulkan/lunarg-vulkan-jammy.list
RUN apt update
RUN apt install vulkan-sdk -y
RUN apt install python3-pip -y
RUN cd /tmp && git clone --recurse-submodules https://github.com/nomic-ai/gpt4all &&  cd gpt4all/gpt4all-backend/ && mkdir build && cd build && cmake .. &&   cmake --build . --parallel  && cd ../../gpt4all-bindings/python && pip install -e .
WORKDIR .
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["runner.py"]

EXPOSE 8765