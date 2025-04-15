pipeline {
    agent any

    environment {
        SONARQUBE_SCANNER = 'SonarScanner' 
        SONARQUBE_SERVER  = 'SonarQube'
        DEPLOY_USER = 'ubuntu'          
        DEPLOY_HOST = '103.173.15.147'   
        DEPLOY_PATH = '/var/www/ecomm'    
        SSH_CRED_ID = 'nginx-ssh'  
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/sanidhya19/E-Commerce-Website.git', branch: 'main'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh "/opt/sonar-scanner/bin/sonar-scanner"
                }
            }
        }

        stage('Wait for Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt || true
                python3 manage.py migrate --noinput
                python3 manage.py collectstatic --noinput
                deactivate
                '''
            }
        }

        stage('Deploy to Nginx') {
            steps {
                sshagent (credentials: ["${SSH_CRED_ID}"]) {
                    sh '''

                    echo "Packaging project..."
                    tar czf app.tar.gz *

                    echo "Transferring to server..."
                    scp app.tar.gz $DEPLOY_USER@$DEPLOY_HOST:/tmp/

                   echo "Extracting on server..."
                   ssh $DEPLOY_USER@$DEPLOY_HOST <<EOF
                   rm -rf $DEPLOY_PATH/*
                   mkdir -p $DEPLOY_PATH
                   tar xzf /tmp/app.tar.gz -C $DEPLOY_PATH
                   EOF
                   '''
                }
            }
        }

        stage('Restart Services (optional)') {
            steps {
                sshagent (credentials: ["${SSH_CRED_ID}"]) {
                    sh '''
                    ssh $DEPLOY_USER@$DEPLOY_HOST <<EOF
                    sudo systemctl restart gunicorn
                    sudo systemctl restart nginx
                    EOF
                    '''
                }
            }
        }
    }
}

