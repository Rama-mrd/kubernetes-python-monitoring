# kubernetes-python-monitoring
Introduction:

This is an application in Python which is collecting external URL metrics and producing Prometheus metrics. 
The following URLS are queried
1.	https://httpstat.us/200
2.	https://httpstat.us/503

The metrics in response are:-
1.	URL response time in milliseconds
2.	URL status up or down using 1(200) or 0(503).
This Python application will be built into docker image and then deployed to Kubernetes.

Pre-requirements:
1.	Python3 environment
2.	Kubernetes env(minikube or cloud-based)
3.	Docker to be installed

Steps :

1.	Install necessary packages from requirements.txt

            cd pythonapp/
            pip install -r requirements.txt

2.	Run the application

            python pythonapp.py

3.	The application is designed to run on localhost. Endpoint /200 will hit https://httpstat.us/200 and give suitable response. Similarly , the endpoint /503 will hit https://httpstat.us/503 and give its response. Any other endpoints will throw error .

Example screenshots:

 ![image](https://user-images.githubusercontent.com/26178872/158742881-7ed486c7-1ae2-4691-a28b-822df0f639df.png)
 
 ![image](https://user-images.githubusercontent.com/26178872/158742940-903b3365-b573-4824-b215-99b7541bd60c.png)


 4.	Create test scripts and run them to verify the outputs if you get them as expected.
 
Building Docker Containers
1.	Build the Docker image

          docker build -t pyapp pythonapp/ .
          
2.	Run docker-compose file to check if app is working fine and if you are able to see Prometheus metrics on 9090 and Grafana on 3000.

          nohup docker-compose -f docker-compose.yaml up > $(date +%Y%m%d%H%M%S).txt 2>&1 &
 
      (App endpoint : http://localhost:5000 , Prometheus endpoint : http://localhost:9090 ,Grafana endpoint : http://localhost:3000 )


Deploying the Containers On K8s Cluster

The file kubernetesmain.yaml is used to create deployments, services on Kubernetes. Secret.yaml is used to store Grafana login credentials.
The file contains:-
a.	Deployment – It contains deployment of python application(local docker image), Prometheus and Grafana (public docker images)
b.	Service – Contains the service endpoints for python application, Prometheus and Grafana.

1.	Create a namespace

               kubectl create -n newdeploy
2.	Deploy secret first

               kubectl apply -f secret.yaml -n newdeploy

3.	Deploy the deployments and services.

                kubectl apply -f kubernetesmain.yaml -n newdeploy
                
4.	Display all the components deployed

                kubectl get all -n newdeploy

![image](https://user-images.githubusercontent.com/26178872/158742983-1be0c48b-5ea8-41c0-9bc4-6a49f761b7a5.png)

 
5.	Forward all service endpoints to listen to node ports

              kubectl port-forward service/grafana -n newdeploy 3000:3000
              kubectl port-forward service/prometheus -n newdeploy 5000:5000
              kubectl port-forward service/webapp1 -n newdeploy 9090:9090

6.	Login to Prometheus pod and copy contents of prometheus/prometheus.yaml
To listen to the webapp . instead of local host, change the ip to the clusterip.

              kubectl exec -it prometheus-7fcc6cb64d-cf658 -n newdeploy -- /bin/sh
              vi /etc/prometheus/prometheus.yml

7.	Open the endpoints again (App endpoint : http://localhost:5000 , Prometheus endpoint : http://localhost:9090 ,Grafana endpoint : http://localhost:3000 ) to check if they are loading as expected.

Data Observability in Prometheus

In prometheus(http://localhost:9090 ), go to “graph” section ,  and in table , choose 
request_count to see the number of requests for each url.

 ![image](https://user-images.githubusercontent.com/26178872/158743039-e44167b0-5736-48c8-85a8-f33f8e9a799a.png)


It can be represented as graph also
 
 ![image](https://user-images.githubusercontent.com/26178872/158743064-cd7bc210-a56e-4b83-a8e0-3006351ed883.png)


We can also check the total latency for each request over the time period in milliseconds.

![image](https://user-images.githubusercontent.com/26178872/158743107-6cc4904f-bb4e-4a71-b061-e66c9975e8f3.png)

 
![image](https://user-images.githubusercontent.com/26178872/158743126-7198c979-f3d3-4979-9c52-347c2fb3421f.png)


 

Adding Prometheus Data Source To Grafana

1.	Open Grafana
Open your browser and point to http://localhost:3000 you will see Grafana Login.
Enter the username and password to login.(default username is admin and password can be retrieved from secrets)
2.	Click on Configuration > Data Sources
3.	Click on Add data source
 ![image](https://user-images.githubusercontent.com/26178872/158743150-26c95e36-a5f4-417a-9bd4-f92d651a5331.png)

4.	Select Prometheus as the data source
 ![image](https://user-images.githubusercontent.com/26178872/158743162-e5726c50-2e60-4996-8aab-ed9302bbe5b7.png)


5.	Add the Prometheus Cluster IP in URL.
6.	Click Save & Test
Grafana Dashboard
1.	Click on Create > New Panel
2.	In metrics , add request_count . 
3.	set Panel name , legend , choose color palette , remove unwanted endpoints from transformation option.
4.	Repeat the same by choosing request_latency_seconds_sum as the metric.
5.	Apply and save to view the metrics in Grafana dashboard.

Request counts dashboard:
           
![image](https://user-images.githubusercontent.com/26178872/158743188-c8fd38c9-39aa-42b3-9be5-9bfced940b67.png)


Requests latency dashboard:
 
![image](https://user-images.githubusercontent.com/26178872/158743196-4a9c2031-ee23-490a-82dc-4b3afe6a4778.png)

