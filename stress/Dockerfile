FROM waggle/plugin-base:1.1.1-ml

COPY . .

RUN apt-get update
RUN apt-get install stress-ng

ENTRYPOINT [ "python3", "controller.py" ]