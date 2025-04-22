pipeline {
    agent any

    environment {
        SONARQUBE_SCANNER = 'SonarScanner' 
        SONARQUBE_SERVER  = 'SonarQube'
        DEPLOY_USER = 'ubuntu'          
        DEPLOY_HOST = '103.173.15.147'   
        DEPLOY_PATH = '/var/www/ecomm'    
        SSH_CRED_ID = 'nginx-ssh'
        TAG= 'test'
        HARBOR_REGISTRY_URL = '103.174.130.22'
        HARBOR_REPO = 'ecomm'
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

        stage('Build Docker Image'){
            steps {
               script{
                   sh """
                   docker build -t ${HARBOR_REGISTRY_URL}/${HARBOR_REPO}/${TAG}:latest .
                   """
                }
            }
        }

         stage('Login to Harbor') {
            steps {
                    withCredentials([usernamePassword(credentialsId: 'harbor-cred', usernameVariable: 'HARBOR_USERNAME', passwordVariable: 'HARBOR_PASSWORD')]) {
                        sh '''
                        set +x
                        echo ${HARBOR_PASSWORD} | docker login ${HARBOR_REGISTRY_URL} -u ${HARBOR_USERNAME} --password-stdin
                        set -x
                        '''
                }
            }
        }

        stage('Push Docker Image to Harbor') {
            steps {
                script {
                    sh """
                    docker push ${HARBOR_REGISTRY_URL}/${HARBOR_REPO}/${TAG}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent (credentials: ["${SSH_CRED_ID}"]) {
                    sh '''
                    set -x

                    echo "Creating deployment archive..."
                    tar --exclude=venv --exclude=app.tar.gz -czf app.tar.gz .

                    echo "Transferring archive to server..."
                    scp app.tar.gz $DEPLOY_USER@$DEPLOY_HOST:/tmp/

                    ssh $DEPLOY_USER@$DEPLOY_HOST "
                       rm -rf /var/www/ecomm/*
                       mkdir -p /var/www/ecomm
                       tar -xzf /tmp/app.tar.gz -C /var/www/ecomm
                       cd /var/www/ecomm
                       docker-compose down || true
                       docker-compose up -d --build

                       echo "Running Django migrations..."
                       docker-compose run --rm web python manage.py migrate

                       echo "Collecting static files..."
                       docker-compose run --rm web python manage.py collectstatic --noinput
                    "
                    '''
                }
            }
        }
        stage('Wait for App') {
           steps {
              sh 'sleep 10'
           }
        }         

        stage('Security Scan with ZAP') {
            steps {
             sh '''
             docker run --rm \
               -v $(pwd):/zap/wrk \
               zaproxy/zap-stable zap-baseline.py \
               -t http://103.174.130.22 \
              -r zap_report.html || true
             '''
       }
    }

    stage('Archive Report') {
      steps {
        archiveArtifacts artifacts: 'zap_report.html', fingerprint: true
      }
    }

  }
}

