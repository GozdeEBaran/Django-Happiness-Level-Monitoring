# Happiness Monitoring Service

Backend, REST API to monitor the happiness level of the users

</br>

# Setup Project

- Two options to setup;

    1. VS CODE
        - Install [Docker](https://www.docker.com/products/docker-desktop)
        - Ensure [Hyper-V is enabled](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) on your machine. May require enabling at BIOS level.
        - Install [VS Code](https://code.visualstudio.com/Download)
        - Install remote extensions in VSCode
        - [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
        - [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
        - Once you install all, open the project in VS Code and remote container will be started automatically
        
    
    2. Pycharm or Other Editors
    
        - Install [Docker](https://www.docker.com/products/docker-desktop)
        - Head to `.devcontainer` folder and fire up the container from command line with `docker-compose up`
        
- Project is running apply below section to start the server.
</br>
</br>

# Start Project
- After the setup (above step) completion
- Run the server with  `runserver` command from `bash`
- Now you should see the api documentation in your browser
- As starting point admin user will be created based on the
    - `name='admin', password='admin'` or ADMIN_PW environment variable
- As soon as project is started seed random data will be loaded to database

# Authorization
- App is utilizing JWT authentication
- User must hit `/api/v1/token/` endpoint with the credential then get the authorization with received token by passing it to
    swagger `authorize` part
- If Postman is used, your header must contain the `Authorization` key and `Bearer <token>` value
# Api Documentation
- App is utilizing Swagger
- Domain should return you to the swagger page by default

## Bash aliases

There are a few helpful aliases installed in the docker container.

| Alias     | Command | Notes |
| --------- | ------- | ------- |
| pmp       | python manage.py | |
| runserver | python manage.py runserver 0.0.0.0:8000 | runs server at http://localhost:8000/|
| lint      | flake8 | runs lint |
| covertest | coverage run manage.py test && coverage report | checks lines are covered with test |
| pmp shell_plus | python manage.py shell_plus | useful for debugging |
| pmp show_urls | python manage.py show_urls | useful for getting all urls in the app |
| pmp reset_db | python manage.py reset_db | destroys the database |
| kibosh    | pmp reset_db --noinput && pmp migrate &&  pmp create_admin_user && pmp seed_happiness | reset database, migrates, seeds |

# Contribution
- Coverage must be 100% and lint must pass. Pull request is not accepted otherwise.
- `covertest` command will give detail result.


## Extra Notes
- If `DEBUG_VS_CODE` option is set to true in .env, debug is ready for VS Code
- Set the loggings logger level to `DEBUG` in `common.py` to see all db queries
- `example.env` file is for reference usage of `env` file.
