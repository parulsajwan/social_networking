
# Social Networking

### Installation Steps

1. **Install Docker**
2. **Create Symbolic Link - Run this command to create symbolic link**- ln -s docker/compose/local.yml docker-compose.override.yml 
3. **Run command to docker build** - Docker compose build
4. **Run command to start docker container**- Docker compose up -d/ docker compose up


### To Check the API use postman collection shared:
social_networking.postman_environment.json
Social Networking.postman_collection.json


### API Details

- {{base_url}}/signup/ -  **API for Signup**
- {{base_url}}/login/ - **API for Login**
- {{base_url}}/search/?search_query=searching_element  - **API to search other users by email and name(paginate up to 10 records per page)**
- {{base_url}}/sent-request/ - **API to send Friend Request**
- {{base_url}}/accepted-requests/ - **API to list friends(list of users who have accepted friend request)**
- {{base_url}}/all-request/ - **List pending friend requests(received friend request)**
- {{base_url}}/action-request/id/?action=A -  **API to accept friend request with id=user request id which want to accept**
- {{base_url}}/action-request/id/?action=R - **API to reject friend request with id=user request id which want to reject**
