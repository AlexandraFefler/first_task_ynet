pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'sashafefler' // Your Docker Hub username
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials
    }

    stages {
        // stage('Ensuring Docker access') {
        //     steps {
        //         echo 'Ensuring Docker access...'
        //         sh '''
        //             if ! docker info > /dev/null 2>&1; then
        //                 echo "Docker daemon not accessible. Ensure the Jenkins user is in the Docker group."
        //                 exit 1
        //             else
        //                 echo "Docker is accessible."
        //             fi
        //         '''
        //     }

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

        }

    }
}