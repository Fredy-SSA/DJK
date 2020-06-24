# Prepare/ Install Jenkins
## The goal of this section is to build a CI/CD pipeline that looks like this:

![Jenkins](./img/l6-01.png)

We are going to use Jenkins (https://jenkins.io) as our automation server. Other automation servers such as TeamCity (https://www.jetbrains.com/teamcity) work equally well. When using Jenkins, the central document is the Jenkinsfile, which will contain the definition of the pipeline with its multiple stages.


Of course, the preceding pipeline just outputs a message during each stage and does nothing else. It is useful though as a starting point from which to build up our pipeline:

**1. Create a project folder named jenkins-pipeline and navigate to it:**

```
mkdir jenkins-pipeline 
cd jenkins-pipeline 

```


**2. Now, let's run Jenkins in a Docker container. Use the following command to do so:**

- wsl\bash
```
docker run --rm -d \
   --name jenkins \
   -u root \
   -p 8080:8080 \
   -v jenkins-data:/var/jenkins_home \
   -v /var/run/docker.sock:/var/run/docker.sock \
   -v $(Pwd)/:/home \
   jenkinsci/blueocean
```

- PS
```powershell

docker run --rm -d `
   --name jenkins `
   -u root `
   -p 8080:8080 `
   -v jenkins-data:/var/jenkins_home `
   -v /var/run/docker.sock:/var/run/docker.sock `
   -v $Pwd/:/home `
   jenkinsci/blueocean

```
Note that we are running as the root user inside the container and that we are mounting the Docker socket into the container (-v /var/run/docker.sock:/var/run/docker.sock) so that Jenkins can access Docker from within the container. Data produced and used by Jenkins will be stored in the Docker volume, **jenkins-data**.





3. In your browser, navigate to **http://localhost:8080** to access the graphical UI of Jenkins.

![Jenkins](./img/l6-Install-01.png)

5. Unlock Jenkins with the admin password that you retrieved with the command.

```
docker container exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

6. Next, choose Install suggested plugins to have Jenkins automatically install the most useful plugins. Plugins include the GitHub integration, an email extension, Maven and Gradle integration, and so on.

![Jenkins](./img/l6-Install-02.png)

![Jenkins](./img/l6-Install-02.1.png)


As soon as the plugins are installed, create your first admin account. When asked to restart Jenkins, do so.

![Jenkins](./img/l6-Install-03.png)

![Jenkins](./img/l6-Install-04.png)

![Jenkins](./img/l6-Install-05.png)

![Jenkins](./img/l6-Install-06.png)

Once you have configured your Jenkins server, start by creating a new project; you may need to click New Item in the main menu:


**7. Add a new project in Jenkins**

- Give the project the name sample-pipeline, select the Pipeline type, and click OK.
- In the configuration view, select the Pipeline tab and add the pipeline definition from the preceding into the Script textbox:

![Jenkins](./img/l6-pipline-01.png)

```json
pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
            }
        }
        stage('Deploy to Staging') {
            steps {
                echo 'Deploying to Staging'
            }
        }
        stage('Deploy to Production') {
            steps {
                echo 'Deploying to Production'
            }
        }
    }
}
```


![Jenkins](./img/l6-pipline-02.png)

8. Click Save and then, in the main menu of Jenkins, select Build Now. After a short moment, you should see this:


![Jenkins](./img/l6-pipline-03.png)


9. Now that we have prepared Jenkins, we can start to integrate our sample application. Let's start with the build step. First, we initialize the jenkins-pipeline project folder as a Git project:

```
mkdir jenkins-pipeline 
cd jenkins-pipeline 

git pull https://github.com/Fredy-SSA/jenkins-pipeline

git init
```

10. Add a package.json file to this folder with this content:

```json
{
  "name": "jenkins-pipeline",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "test": "jasmine"
  },
  "dependencies": {
    "express": "^4.17.1"
  },
  "devDependencies": {
    "jasmine": "^3.4.0"
  }
}
```

There is nothing exceptional in this file other the usual list of external dependencies, express and jasmine, in this case. Also, note the two scripts start and test that we define for use with npm.

11. Add a **hobbies.js** file to the project, which implements the logic to retrieve hobbies as a JavaScript module called hobbies:

```javascript
const hobbies = ["jogging","cooking","diving","swimming","reading"];

exports.getHobbies = () => {
    return hobbies;
}

exports.getHobby = id => {
    if(id<1 || id > hobbies.length)
        return null;
    return hobbies[id-1];
}
```
This code evidently is simulating a database by serving pre-canned data stored in the hobbies array. We do this for simplicity.

12. Next add a **server.js** file to the folder that defines a RESTful API with the three endpoints, GET /,  GET /hobbies, and GET /hobbies/:id. The code uses the logic defined in the hobbies module to retrieve data:


```nodejs
const hobbies = require('./hobbies');
const express = require('express');
const app = express();

app.listen(3000, '0.0.0.0', () => {
    console.log('Application listening at 0.0.0.0:3000');
})

app.get('/', (req, res) => {
    res.send('Sample API');
})

app.get('/hobbies', async (req, res) => {
    res.send(hobbies.getHobbies());
})

app.get('/hobbies/:id', async (req, res) => {
    const id = req.params.id;
    const hobby = hobbies.getHobby(id);
    if(!hobby){
        res.status(404).send("Hobby not found");
        return;
    }
    res.send();
})
```

13. Now we need to define some unit tests. Create a spec subfolder in the project and add the **hobbies-spec.js** file to it with the following code that tests the hobbies module:

```nodejs
const hobbies = require('../hobbies');
describe("API unit test suite", () => {
    describe("getHobbies", () => {
        const list = hobbies.getHobbies();
        it("returns 5 hobbies", () => {
            expect(list.length).toEqual(5);
        });
        it("returns 'jogging' as first hobby", () => {
            expect(list[0]).toBe("jogging");
        });
    })
})
```
14. The last step is to add a **support/jasmine.json** file to configure our test framework, Jasmine. Add the following code snippet:

```nodejs
{
    "spec_dir": "spec",
    "spec_files": [
      "**/*[sS]pec.js"
    ],
    "stopSpecOnExpectationFailure": false,
    "random": false
}
```


This is all the code that we need for the moment.

