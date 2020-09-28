# Using a package manager
The easiest way to install software on a macOS or Windows laptop is to use a good package manager. On macOS, most people use Homebrew, and on Windows, Chocolatey is a good choice. If you're using a Debian-based Linux distribution such as Ubuntu, then the package manager of choice for most is **apt**, which is installed by default. 

# Installing Homebrew on macOS
Homebrew is the most popular package manager on macOS, and it is easy to use and very versatile. Installing Homebrew on macOS is simple; just follow the instructions at **https://brew.sh/**:

- In a nutshell, open a new Terminal window and execute the following command to install Homebrew:
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
- Once the installation is finished, test whether Homebrew is working by entering **brew --version** in the Terminal. You should see something like this:

```
$ brew --version
Homebrew 2.1.4
Homebrew/homebrew-core (git revision 77d1b; last commit 2019-06-07)
```

- Now, we are ready to use Homebrew to install tools and utilities. If we, for example, want to install the Vi text editor, we can do so like this:
```
$ brew install vim
```

This will then download and install the editor for you.

# Installing Chocolatey on Windows
Chocolatey is a popular package manager for Windows, built on PowerShell. To install the Chocolatey package manager, please follow the instructions at https://chocolatey.org/ or open a new PowerShell window in admin mode and execute the following command:

```
PS> Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```
#### If TLS is old - Fix  run in Powershell
```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
```

- **Tip** :It is important to run the preceding command as an administrator, otherwise, the installation will not succeed.

Once Chocolatey is installed, test it with the choco --version command. You should see output similar to the following:
```
PS> choco --version
0.10.15
```
To install an application such as the Vi editor, use the following command:
```
PS> choco install -y vim
```
The -y parameter makes sure that the installation happens without asking for reconfirmation.

- **Tip** : Please note that once Chocolatey has installed an application, you need to open a new PowerShell window to use that application.
