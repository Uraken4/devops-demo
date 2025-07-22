pipeline {
    agent any
    environment {
        PATH = "/home/jenkins/bin:$PATH"
        CONFIG_FILE = "/var/jenkins_home/pipeline-config.yaml"
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Uraken4/devops-demo.git', branch: 'main', credentialsId: 'github-cred'
            }
        }
        stage('Install Docker Compose') {
            steps {
                sh '''
                    mkdir -p /home/jenkins/bin
                    curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /home/jenkins/bin/docker-compose
                    chmod +x /home/jenkins/bin/docker-compose
                '''
            }
        }
        stage('Build') {
            steps {
                script {
                    def config = readYaml file: env.CONFIG_FILE
                    sh "docker-compose -f ${config.compose.file} build"
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    def config = readYaml file: env.CONFIG_FILE
                    sh "docker-compose -f ${config.compose.file} up -d"
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed'
        }
        failure {
            script {
                def config = readYaml file: env.CONFIG_FILE
                sh "docker-compose -f ${config.compose.file} down"
            }
        }
    }
}
