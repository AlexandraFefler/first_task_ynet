pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'sashafefler' // Your Docker Hub username
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials
    }

    stages {
        stage('Ensuring Docker access') {
            steps {
                echo 'Ensuring Docker access...'
                sh '''
                    if ! docker info > /dev/null 2>&1; then
                        echo "Docker daemon not accessible. Ensure the Jenkins user is in the Docker group."
                        exit 1
                    else
                        echo "Docker is accessible."
                    fi
                '''
            }
        }
    }
}