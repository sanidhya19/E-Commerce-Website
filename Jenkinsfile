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

       /* stage('Wait for Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        } */

        stage('Deploy') {
            steps {
                sshagent (credentials: ["${SSH_CRED_ID}"]) {
                    sh '''
                    set -x

                    tar --exclude=venv --exclude=app.tar.gz -czf app.tar.gz .
                    scp app.tar.gz $DEPLOY_USER@$DEPLOY_HOST:/tmp/

                    ssh $DEPLOY_USER@$DEPLOY_HOST "
                       rm -rf /var/www/ecomm
                       mkdir -p /var/www/ecomm
                       tar -xzf /tmp/app.tar.gz -C /var/www/ecomm
                       cd /var/www/ecomm
                       docker-compose down
                       docker-compose up -d --build
                    "
                    '''
                }
            }
        }
      }
   }
}

