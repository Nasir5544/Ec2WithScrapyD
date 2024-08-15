Running Scrapy Spiders on AWS EC2 with Scrapyd
Overview
This guide explains how to deploy and run Scrapy spiders on an AWS EC2 instance using Scrapyd.

Prerequisites
A working Scrapy project with spiders.
An AWS account.
Step 1: Create and Configure an EC2 Instance
Launch an EC2 Instance:

Go to AWS Console > Services > EC2.
Click "Launch Instance."
Select "Ubuntu Server 18.04 LTS (HVM)".
Choose an instance type.
Click "Review and Launch."
Create a new key pair, name it, and download it. Click "Launch Instance."
Configure Security Groups:

Select your instance in AWS Console and go to the "Security Groups" tab.
Edit inbound rules:
Add a rule for TCP port 6800 (Scrapyd) allowing traffic from your IP address or 0.0.0.0/0 for testing.
Save the rules.
Step 2: Install and Configure Scrapyd
Connect to Your EC2 Instance:

In your terminal, navigate to the directory with your key pair file.
Run: chmod 400 your_keyPair.pem
Connect using SSH with the command from AWS Console.
Install Python and Scrapyd:

Update packages: sudo apt update
Install pip: sudo apt install python3-pip
Install virtualenv: sudo pip3 install virtualenv
Create and activate a virtual environment:
bash
Copy code
virtualenv venv
source venv/bin/activate
Install Scrapyd: pip install scrapyd
Configure Scrapyd:

Create and edit scrapyd.conf:
bash
Copy code
touch scrapyd.conf
vim scrapyd.conf
Add the configuration:
ini
Copy code
[scrapyd]
eggs_dir    = eggs
logs_dir    = logs
items_dir   =
jobs_to_keep = 5
dbs_dir     = dbs
max_proc    = 0
max_proc_per_cpu = 4
finished_to_keep = 100
poll_interval = 5.0
bind_address = 0.0.0.0
http_port   = 6800
debug       = off
runner      = scrapyd.runner
application = scrapyd.app.application
launcher    = scrapyd.launcher.Launcher
webroot     = scrapyd.website.Root

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
daemonstatus.json = scrapyd.webservice.DaemonStatus
Save and exit Vim (:wq).
Start Scrapyd:

Run Scrapyd in the background:
bash
Copy code
nohup scrapyd &
Verify it's running by visiting http://34.228.37.54:6800 in your browser.
Step 3: Deploy Your Scrapy Project
Configure Deployment:

In your Scrapy project environment, install Scrapyd client:
bash
Copy code
pip install scrapyd-client
Open scrapy.cfg in your project root and configure:
ini
Copy code
# Automatically created by: scrapy startproject
#
# For more information about the [deploy] section see:
# https://scrapyd.readthedocs.io/en/latest/deploy.html

[settings]
default = MyScrapyDTest.settings

[deploy:default]
url = http://34.228.37.54:6800/
project = MyScrapyDTest
Deploy the Project:

Navigate to the directory with scrapy.cfg and deploy:
bash
Copy code
scrapyd-deploy default -p MyScrapyDTest
Run a Spider:

Use PowerShell to send a request to Scrapyd:
powershell
Copy code
Invoke-WebRequest -Uri http://34.228.37.54:6800/schedule.json -Method POST -Body @{
    project='MyScrapyDTest'
    spider='product_scraper'
    city='Islamabad'
}
Summary
Launched and configured an EC2 instance.
Installed and configured Scrapyd.
Deployed a Scrapy project and managed spiders on Scrapyd.
