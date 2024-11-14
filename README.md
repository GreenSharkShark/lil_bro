# Lil Bro
Share confidential information securely and anonymously without using instant messengers.
All information is stored in the database in encrypted form and is deleted as soon as the data on the link you generated
has been viewed or if the specified secret lifetime has expired.

## Installation

To start app at your local machine:
1. clone repo:
    ```bash
    git clone https://github.com/GreenSharkShark/Safe_secret.git
   ```
2. Navigate to work directory:
    ```bash
    cd Safe_secret
   ```
3. Create .env file using .env_example.
4. Make sure Docker is installed on your local machine and start app with:
    ```bash
    docker-compose up --build
   ```

### Note:
To enhance security and avoid storing user data in plain text within the database, 
this project leverages the Amazon Web Services Key Management Service in conjunction 
with the aws_encryption_sdk library. This service enables the generation and secure 
storage of an encryption key, which is then employed by the library to encrypt 
data in a secure manner.

Integrating a trusted third-party service into the project bolsters the 
application's reliability. Please note that this service may involve associated 
costs. To utilize this project, you will need to create an account on the website: 
https://aws.amazon.com/, and generate your own encryption key or configure the 
project to utilize alternative data encryption methods according to your requirements.

## Contribution
If you would like to contribute to the Atomic Habits project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch from the main branch.
3. Make your desired changes and improvements.
4. Commit and push your changes to your forked repository.
5. Create a pull request to merge your changes into the main repository.

## Contact
For any questions or inquiries, feel free to reach out via email at zhorikzeniuk@gmail.com.