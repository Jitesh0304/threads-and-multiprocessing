import boto3
from botocore.exceptions import ClientError, NoCredentialsError, CredentialRetrievalError

def check_aws_credentials():
    """
    Checks if the current boto3 session has valid AWS credentials.
    """
    # Create an STS client. STS (Security Token Service) is a good choice 
    # because the get_caller_identity call is simple and doesn't require 
    # permissions to specific resources like S3 or EC2.
    try:
        sts = boto3.client(
                'sts',
                aws_access_key_id='KSBOECNALJAPSOAJFMA0QP',
                aws_secret_access_key='iosdw943=aose23kenwfw-34nws;odsai',
                region_name='ap-south-1'
        )
        # Attempt to call get_caller_identity
        response = sts.get_caller_identity()
        print("Credentials are valid.")
        print(f"User Arn: {response['Arn']}")
        return True
    except NoCredentialsError:
        print("Error: Credentials not found or not configured.")
        return False
    except CredentialRetrievalError:
        print("Error: Unable to retrieve credentials from the environment.")
        return False
    except ClientError as e:
        # Catch specific AWS errors
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == 'InvalidClientTokenId':
            print("Error: The security token (access key/secret key) included in the request is invalid.")
        elif error_code == 'ExpiredToken':
            print("Error: The security token included in the request is expired.")
        elif error_code == 'UnauthorizedSSOTokenError':
            print("Error: The SSO token is unauthorized or invalid.")
        else:
            print(f"Error: An AWS client error occurred: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return False

# Run the check
if __name__ == "__main__":
    check_aws_credentials()
