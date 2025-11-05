pipeline {
    agent {
        docker {
            image 'docker:27-cli'
            args '-v /var/run/docker.sock:/var/run/docker.sock --add-host=host.docker.internal:host-gateway'
        }
    }

    environment {
        DOCKER_USERNAME = 'sashafefler'
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials as secret text
        DOCKER_IMAGE = 'sashafefler/first_task_ynet'
        VM_HOST = '192.168.1.20'
        VM_USER = 'jenkinsuser'
    }

    stages {

        stage ('Docker Hub auth') {
            steps {
                echo 'Docker hub authentication running...'
                sh '''
                    set -x # Log commands
                    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                '''
            } 
        }

        // echo 'checking success. Logged in as:'
        // docker info | grep username

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
                    docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
                    echo "logged in DH"
                    docker push $DOCKER_IMAGE:latest
                '''
            }
        }

        stage('Test - run container on host') {
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
                apk add --no-cache curl
                echo "Waiting for container to start..."
                sleep 5
                echo "Checking response..."
                if curl -s -o /dev/null -w "%{http_code}" http://host.docker.internal:5000 | grep 200; then
                echo "Test passed: App is responding with HTTP 200"
                else
                    echo "Test failed: App is not responding with HTTP 200"
                    exit 1
                fi
                '''
            }
        } //was just a -> curl -s -o /dev/null -w "%{http_code}" http://host.docker.internal:5000 | grep 200. Wrapped it in the same way in final project

        stage('Connect to prod') {
            steps {
                echo "connecting to vm on host..."
                withCredentials([sshUserPrivateKey(credentialsId: 'ynet-vm-ssh', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                    dir('first_task_ynet/app') {
                        sh '''
                            scp -o StrictHostKeyChecking=no -i "$SSH_KEY" docker-compose.yaml $SSH_USER@$VM_HOST:/home/$SSH_USER/ynet/

                            # install docker & compose if missing, login, pull & run
                            ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" $SSH_USER@$VM_HOST <<'EOF'
                                set -e
                                # Install Docker CE + compose plugin (Ubuntu/Debian)
                                if ! command -v docker >/dev/null 2>&1; then
                                    sudo apt-get update
                                    sudo apt-get install -y ca-certificates curl gnupg
                                    sudo install -m 0755 -d /etc/apt/keyrings
                                    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
                                    sudo chmod a+r /etc/apt/keyrings/docker.gpg
                                    echo \
                                    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                                    $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                                    sudo apt-get update
                                    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
                                fi

                                # Login to Docker Hub (uses short-lived token via stdin)
                                echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

                                cd ~/ynet
                                # ensure compose file points to your image tag or latest
                                docker compose pull
                                docker compose up -d
                                docker compose ps
                            EOF
                        '''
                    }
                }
                //connect via ssh (using jenkins credential) to a running, preconfigured vm for now 
                //then clone the same git repo? nah maybe do it right and use dockerhub 
            }
        }

    }
}