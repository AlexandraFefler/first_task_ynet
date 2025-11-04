pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'sashafefler'
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials as secret text
    }

    stages {

        stage('Cleanup') {
            steps {
                echo 'Cleaning up before cloning...'
                sh '''
                    if [ -d "first_task_ynet" ]; then
                        echo "Directory exists, cleaning up..."
                        rm -rf first_task_ynet
                    else
                        echo "Directory does not exist, no cleanup needed."
                    fi
                '''
            }
        }

        stage('Clone') {
            steps {
                echo 'Cloning git repo...'
                sh 'git clone https://github.com/AlexandraFefler/first_task_ynet.git'
            }
        }

        stage('Install Docker cli and docker-compose cli') {
            steps {
                echo "Installing Docker cli and docker compose cli..."
                sh '''
                    which docker || {
                        apt-get update
                        apt-get install -y docker.io
                        apt-get install -y docker-compose-plugin
                    }
                    echo "docker ver:"
                    docker version
                    echo "docker compose ver:"
                    docker-compose version
                '''

            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    cd first_task_ynet/app
                    docker build -t sashafefler/first_task_ynet:latest .
                    echo "Built Docker image with tag sashafefler/first_task_ynet:latest"
                '''
            }
        }

        stage('Test- run container on host') {
            steps {
                sh '''
                    cd first_task_ynet/app
                    echo "runnning docker compose on host machine... (at least should be)"
                    docker compose down || true
                    docker compose up -d 
                ''' //do a --build instead of stage('Build') before?
            }
        }

    }
}