# Build the CI/CD pipeline:

1. Commit the code just created locally with the following command:

```bash
git add -A 
git commit -m "First commit"
```

2. To avoid all of the node modules being saved to GitHub, add a .gitignore file to the project root folder with the following content:

```nodejs
node_modules
```

3. **Now, we need to define a repository on GitHub**. 

- Log in to your account on GitHub at **https://github.com**.
- Create a new repository there and call it : **jenkins-pipeline** 
 
![Jenkins](./img/l6-git-ci-01.png)

Create a new GitHub repository for the Jenkins pipeline sample application
! Note  that my GitHub account is **fredy-ssa**. In your case, it will be your own account.

4. After you have clicked the green button, Create repository, go back to you project and execute the following two commands from within the project root folder:

```
git remote add origin https://github.com/fredy-ssa/jenkins-pipeline.git
git push -u origin master
```

**Make sure you replace fredy-ssa** in the first line with your own GitHub account name. After this step, your code will be available on GitHub for further use. One of the users will be Jenkins, which will pull the code from this repository as we will show shortly.

5. The next thing is to go back to Jenkins (localhost:8080) and modify the configuration of the project. Log in to Jenkins if needed and select your project, sample-pipeline.

6. Then, select Configure in the main menu. Select the Pipeline tab and modify the settings so that they look similar to this:

![Jenkins](./img/l6-git-ci-02.png)

Configuring Jenkins to pull source from GitHub
With this, we configure Jenkins to pull code from GitHub and use a Jenkinsfile to define the pipeline. Jenkinsfile is expected to be found in the root of the project. 

Note that for the repository URL path, we need to give the **relative path** to the **/home** directory where our project is located. Remember that, when running the Jenkins container, we mapped our own home folder on the host to the **/home** folder inside the Jenkins container with this: **-v $pwd/:/home**.

7. Hit the green Save button to accept the changes.

8. We have defined that Jenkinsfile needs to be in the project root folder. This is the foundation of**Pipeline-as-Code**, since the pipeline definition file will be committed to the GitHub repository along with the rest of the code. Hence, add a file called Jenkinsfile to the jenkins-pipeline folder and add this code to it:

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

```
git add -A 
git commit -m "Defined code based Pipeline"
git push origin master
```

Select your sample-pipeline project and click Build now in the main menu. Jenkins will start to build the pipeline. 


 