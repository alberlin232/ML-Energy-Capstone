<h1>ERCOT</h1>
<h4> Useful documentation and resources: </h4>
<p>
ARPA-E PERFORM AWS:
https://registry.opendata.aws/arpa-e-perform/ <br>
Github Documentaiton: https://github.com/PERFORM-Forecasts/documentation <br>

ARPA-E perform .h5 files found at: s3://arpa-e-perform/

To access files, AWS CLI is required. <br>
Documentation: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install. <br>

AWS CLI can be installed on Mac OS by using the following commands:
</p>


```
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg ./AWSCLIV2.pkg -target /
```
Using the AWS CLI, ARPA-E data can be downloaded directly using the AWS command:

```
aws s3 cp s3://arpa-e-perform/ ./
```
