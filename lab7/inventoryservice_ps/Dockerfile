# Using python:3.7-slim-buster image
FROM python:3.7-slim-buster
# Defining working directory and copy the requirements file
WORKDIR /usr/src/myapp
RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install g++
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Enviroment Variables - Here use your project id
ENV project_id your_project_id
EXPOSE 5000
CMD ["python3","app.py"]