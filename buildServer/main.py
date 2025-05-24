import os
git_url = os.getenv('GIT_URL')
cmd = os.getenv('CMD', 'npm start') 
print(f"Original cmd: {cmd}")
cmd_list = cmd.split(' ')  
cmd = str(cmd_list).replace("'", '"')  

print(f"Command: {cmd}")

env_content=os.getenv('ENV_CONTENT')


print("Running python script to generate Dockerfile")
def write_env_file(repo_path, env_content):
    env_path = os.path.join(repo_path, '.env')
    with open(env_path, 'w') as env_file:
        env_file.write(env_content)
    print(f".env file created at {env_path}")

def detect_project_type(files):
    if any(file in files for file in ['index.html', 'webpack.config.js', 'vite.config.js', 'frontend','App.jsx',"main.jsx"]):
        return 'frontend'
    if 'package.json' in files:
        return 'node'
    if any(file in files for file in ['requirements.txt', 'Pipfile', 'setup.py', 'pyproject.toml']):
        return 'python'
    if any(file in files for file in ['pom.xml', 'build.gradle']):
        return 'java'
    if 'Gemfile' in files:
        return 'ruby'
    if 'composer.json' in files:
        return 'php'
    if 'go.mod' in files:
        return 'go'
    if 'Cargo.toml' in files:
        return 'rust'
    if any(file in files for file in ['CMakeLists.txt', 'Makefile']):
        return 'cpp'
    if any(file.endswith('.csproj') for file in files):
        return 'csharp'
    return 'unknown'


def generate_dockerfile(project_type, cmd, include_env):
    env_copy = "COPY .env ./\n" if include_env else ""
    templates = {
        'node': f'''
# Node.js Dockerfile
FROM node:alpine
WORKDIR /app
COPY package*.json ./
{env_copy}RUN npm install
COPY . .
EXPOSE 3000
CMD {cmd}
''',
        'python': f'''
# Python Dockerfile
FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt ./
{env_copy}RUN pip install  -r requirements.txt
COPY . .
CMD {cmd}
''',
        'java': f'''
# Java Dockerfile
FROM openjdk:11-jre-slim
WORKDIR /app
{env_copy}COPY . .
RUN javac Main.java
CMD {cmd}
''',
        'ruby': f'''
# Ruby Dockerfile
FROM ruby:3.0-alpine
WORKDIR /app
COPY Gemfile Gemfile.lock ./
{env_copy}RUN bundle install
COPY . .
CMD {cmd}
''',
        'php': f'''
# PHP Dockerfile
FROM php:8.0-apache
WORKDIR /var/www/html
{env_copy}COPY . .
RUN docker-php-ext-install mysqli
CMD {cmd}
''',
        'go': f'''
# Go Dockerfile
FROM golang:1.17-alpine
WORKDIR /app
{env_copy}COPY . .
RUN go build -o main .
CMD {cmd}
''',
        'rust': f'''
# Rust Dockerfile
FROM rust:1.65-alpine
WORKDIR /app
{env_copy}COPY . .
RUN cargo build --release
CMD {cmd}
''',
        'cpp': f'''
# C++ Dockerfile
FROM gcc:11-alpine
WORKDIR /app
{env_copy}COPY . .
RUN make
CMD {cmd}
''',
        'csharp': f'''
# C# Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /app
{env_copy}COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o out
FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=build /app/out .
CMD {cmd}
''',
        'frontend': f'''
# Frontend Dockerfile
FROM node:alpine
WORKDIR /app
COPY package*.json ./
{env_copy}RUN npm install
COPY . .
CMD {cmd}
''',
    }
    return templates.get(project_type, '# Unsupported project type. Please define a custom Dockerfile.')

def save_dockerfile(repo_path, content):
    dockerfile_path = os.path.join(repo_path, 'Dockerfile')
    with open(dockerfile_path, 'w') as dockerfile:
        dockerfile.write(content)
    print(f"Dockerfile generated at {dockerfile_path}")

def from_path_to_file_list(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), directory))
    return files


def auto_generate_dockerfile(repo_path, include_env=True):
    print(f"Generating Dockerfile for {repo_path}")
    files = from_path_to_file_list(repo_path)
    print(f"Files detected: {files}")
    project_type = detect_project_type(files)
    print(f"Detected project type: {project_type}")

    if project_type == 'unknown':
        print("Unsupported project type. Exiting.")
        return

    dockerfile_content = generate_dockerfile(project_type, cmd, include_env)
    print(cmd)
    print(f"Dockerfile content:\n{dockerfile_content}")
    save_dockerfile(repo_path, dockerfile_content)

# Example Usage

repo_name = git_url.split('/')[-1].replace('.git', '')
repo_path = f'./{repo_name}'

include_env = True  # Set to True if you want to include .env file
print(repo_path)
write_env_file(repo_path,env_content )
print("ENV is completed.........")

#generate Dockerfile if not present;
if not os.path.exists(os.path.join(repo_path, 'Dockerfile')):
    auto_generate_dockerfile(repo_path, include_env)
else:
    print("Dockerfile already exists. Skipping generation...")


#print .env content  here
def print_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Content of {file_path}:\n{content}")
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except IOError:
        print(f"Error: An issue occurred while reading the file at {file_path}.")
