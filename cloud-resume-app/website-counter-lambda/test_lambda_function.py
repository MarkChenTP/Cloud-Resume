import random
import sys
import boto3
import unittest
from moto import mock_dynamodb2
import lambda_function


class TestWebsiteCounter(unittest.TestCase):
    def setUp(self):
        pass

    @mock_dynamodb2
    def test_set_default_totalVisit(self):
        # Get the service resource
        dynamodb = boto3.resource('dynamodb')
        
        # Setup a test dynamoDB table
        tablename = 'unittest'
        table = dynamodb.create_table(
            TableName=tablename,
            KeySchema=[
                {
                    'AttributeName': 'webVisit_count_type',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'webVisit_count_type',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=tablename)        

        '''
        Start of testing DynamoDB interaction

        '''
        # Confirm test table does not have totalVisit
        response = lambda_function.getItem(table, 'totalVisit')
        isTotalVisitExist = lambda_function.checkItemExist(response)
        self.assertEqual(False, isTotalVisitExist)

        # Put default totalVisit into the table
        lambda_function.putDefaultItem(table, 'totalVisit')
        response = lambda_function.getItem(table, 'totalVisit')
        
        count = response['Item']['visit_counts']
        self.assertEqual(0, count)

        '''
        End of testing DynamoDB interaction

        '''


    @mock_dynamodb2
    def test_get_updated_totalVisit(self):        
        # Get the service resource
        dynamodb = boto3.resource('dynamodb')
        
        # Setup a test dynamoDB table
        tablename = 'unittest'
        table = dynamodb.create_table(
            TableName=tablename,
            KeySchema=[
                {
                    'AttributeName': 'webVisit_count_type',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'webVisit_count_type',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=tablename)
        
        # Put a test totalVisit into the table
        testVisitCounts = random.randint(1, 100)
        table.put_item(
            Item={
                'webVisit_count_type': 'totalVisit',
                'visit_counts': testVisitCounts
            }
        )

        '''
        Start of testing DynamoDB interaction

        '''
        # Confirm test table does have totalVisit with visit_counts of testVisitCounts
        response = lambda_function.getItem(table, 'totalVisit')
        isTotalVisitExist = lambda_function.checkItemExist(response)
        self.assertEqual(True, isTotalVisitExist)

        count = response['Item']['visit_counts']
        self.assertEqual(testVisitCounts, count)

        # Increase the visit_counts of totalVisit by 1  
        response = lambda_function.incrementTotalVisit(table)

        count = response["Attributes"]["visit_counts"]
        self.assertEqual(testVisitCounts + 1, count)

        '''
        End of testing DynamoDB interaction
        
        '''

    def tearDown(self):
        pass


def checklambda():
    # Run unittest.TestCase: TestWebsiteCounter
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestWebsiteCounter)
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    test_result = test_runner.run(test_suite)

    # wasSuccessful() Return True if all tests run so far have passed, otherwise returns False.
    test_isSuccess = str(test_result.wasSuccessful())
    return test_isSuccess



if __name__ == "__main__":
    sys.stdout.write(checklambda())
