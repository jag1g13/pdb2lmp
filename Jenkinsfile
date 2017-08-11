pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh 'py.test --junitxml results.xml test/'
      }
    }
    stage('xUnit') {
      steps {
        junit 'results.xml'
      }
    }
  }
}