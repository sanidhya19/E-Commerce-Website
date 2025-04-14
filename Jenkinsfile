pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
               withKubeConfig(caCertificate: '', clusterName: 'kubernetes', contextName: 'kubernetes', credentialsId: 'kube-token', namespace: '', restrictKubeConfigAccess: false, serverUrl: 'https://10.20.30.2:6443') {
    sh "kubectl get ns"
            }
          }
       }
    }
}