pipeline {
    agent {
        docker {
            image 'docker:27-cli'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

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

        stage('Health check') {
            steps {
                sh '''
                echo "Waiting for container to start..."
                sleep 5
                echo "Checking response..."
                curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep 200
                '''
            }
        }


    }
}