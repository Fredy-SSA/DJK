# Build the CI/CD pipeline:
Git address: https://github.com/fredy-ssa/jenkins-pipeline.git

- The next thing is to go back to Jenkins (localhost:8080) and modify the configuration of the project. Log in to Jenkins if needed and select your project, sample-pipeline.

-  Then, select Configure in the main menu. Select the Pipeline tab and modify the settings so that they look similar to this:
    - Add : https://github.com/fredy-ssa/jenkins-pipeline.git

![Jenkins](./img/l6-git-ci-02.png)

Configuring Jenkins to pull source from GitHub
With this, we configure Jenkins to pull code from GitHub and use a Jenkinsfile to define the pipeline. Jenkinsfile is expected to be found in the root of the project. 


7. Hit the green Save button to accept the changes.

8. We have defined that Jenkinsfile needs to be in the project root folder. This is the foundation of **Pipeline-as-Code** , since the pipeline definition file will be committed to the GitHub repository along with the rest of the code. Hence, add a file called Jenkinsfile to the jenkins-pipeline folder and add this code to it:

```nodejs
pipeline {
    agent {
        docker {
            image 'node:latest'
            args '--rm -it --name myapp -p 3000:3000'

        }
    }
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                
            }
        }
        stage('Test') {
            steps {
                sh './jenkins/scripts/test.sh'
            }
        }
        stage('Deliver') {
            steps {
                sh './jenkins/scripts/deliver.sh'
                input message: 'Finished using the web site? (Click "Proceed" to continue)'
                sh './jenkins/scripts/kill.sh'
            }
        }
    }
}
```
Now, we are ready to roll. Use git to commit your changes and push them to your repository:



 