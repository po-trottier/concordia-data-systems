# Project Setup
## 1 - Required Software
- Install [Docker](https://www.docker.com/products/docker-desktop). 
- Feel free to edit the password in the yml file, for security reasons.
- Launch Docker Desktop, run your terminal in the GitHub repository's directory, then run the following command:
```
docker-compose up -d
```

## 2 - Setting up the server
- Ensure that you have [Azure Data Studio](https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15) installed on your machine.
- Launch Azure Data Studio. 
- On the left navbar, choose Extensions, and install the Postgres extension.
- Next, add the Postgres server you started in Docker. Click on the server icon in the left tab and choose "New Connection".
```
Connection type: PostgreSQL
Server name: localhost
Authentication type: password
User name: postgres
Password: [what you chose in step #1]
Database name: [choose form dropdown]
Server group: <Default>
```

## 3 - Setting up your Phase 1 database
- Select the Postgres Docker server (top left) and right-click "New Query". 
- Type the following, then run:
```
CREATE DATABASE [database_name_here]
```
- Connect the Jupyter notebook to this database by double-clicking on the "project_notebook.ipynb" file in your project directory. It will open a new tab in Azure Data Studio.
- To connect, click on the dropdown for "Attach to" on the top of the tab window, and choose Postgres Docker.
