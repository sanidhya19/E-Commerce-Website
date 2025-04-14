pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
               withKubeConfig(credentialsId: 'kube-config') {
           sh "kubectl get ns"
        }
      }
    }
  }
}
