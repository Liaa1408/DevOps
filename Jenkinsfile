
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'suhitasv/devops-week12:latest'
        APP_PORT = '5001'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    (python3 app.py > flask.log 2>&1 &)
                    echo $! > flask.pid
                '''

                sh '''
                    for i in $(seq 1 20); do
                        if curl -fsS http://127.0.0.1:5001/ >/dev/null; then
                            exit 0
                        fi
                        sleep 1
                    done
                    cat flask.log
                    exit 1
                '''

                sh 'TEST_URL=http://127.0.0.1:5001/ python3 -m pytest -v'
            }

            post {
                always {
                    sh 'if [ -f flask.pid ]; then kill $(cat flask.pid) 2>/dev/null || true; fi'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '/usr/local/bin/docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Login and Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$DOCKERHUB_TOKEN" |
                            docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push "$DOCKER_IMAGE"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
                sh 'kubectl rollout status deployment/devops-week12-deployment --timeout=120s'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get deployments'
                sh 'kubectl get pods'
                sh 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
