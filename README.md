# Overview

This project is composed of the following components:

## API

A REST api implemented using FastAPI which loads a model from the database or downloads it from a S3 bucket.

The api is instrumented using `prometheus_fastapi_instrumentator`, which means it adds a GET `/metrics` route where prometheus can scrape the api's metrics.

`prometheus_fastapi_instrumentator` serves common metrics like request counts, cpu usage and etc.

However this api also adds a custom metric named `intrusion_prediction_results_total`. Which is a counter that increments with the result of every prediction. In other words it stores the number of times a prediction was true and false.

## Prometheus

Prometheus is an open-source application that can scrape metrics from multiple sources, in our case it targets the api container.

It extract common FastAPI metrics served by `prometheus_fastapi_instrumentator` and also the custom `intrusion_prediction_results_total` described before.

Every time it scrapes the metrics it stores on it's database.

## Grafana

Although Prometheus offer some options of data visualization, Grafana is far superior and allows us to setup custom dashboards.

On the container startup a new dashboard named `"DVC Intrusion Detection API Metrics"` is created. The dashboard is configured by the file `monitoring/dashboard.json`


# Running the api and monitoring containers

Create the `.env` file on the project's root with the AWS credentials. The file is ignored by git

```env
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2
export DEPLOYMENT_AWS_BUCKET=intrusion-detection-deployment
```

To start the api and see the metrics, execute:

```bash
docker-compose up
```

It will download the model from S3 and use it to execute predictions.

To avoid downloading the model file every time the container is created:

1. Place the model file on this project using the path: `./model/model.joblib` (it's ignored by git)
2. Uncomment the volume configuration from the api container on `docker-compose.yaml`

# Invoking the prediction api

### Positive:

This example is predicted as an intrusion.

```bash
curl -H "Content-type: application/json" -d '{"duration":0,"src_bytes":0.00020094717776309186,"dst_bytes":0,"land":0,"wrong_fragment":0,"urgent":0,"hot":0,"num_failed_logins":0,"logged_in":0,"num_compromised":0,"root_shell":0,"su_attempted":0,"num_root":0,"num_file_creations":0,"num_shells":0,"num_access_files":0,"is_guest_login":0,"count":0.9980430528375733,"srv_count":0.9980430528375733,"serror_rate":0,"srv_serror_rate":0,"rerror_rate":0,"srv_rerror_rate":0,"same_srv_rate":1,"diff_srv_rate":0,"srv_diff_host_rate":0,"dst_host_count":1,"dst_host_srv_count":1,"dst_host_same_srv_rate":1,"dst_host_diff_srv_rate":0,"dst_host_same_src_port_rate":1,"dst_host_srv_diff_host_rate":0,"dst_host_serror_rate":0,"dst_host_srv_serror_rate":0,"dst_host_rerror_rate":0,"dst_host_srv_rerror_rate":0,"protocol_type_icmp":1,"protocol_type_tcp":0,"protocol_type_udp":0,"service_IRC":0,"service_X11":0,"service_Z39_50":0,"service_auth":0,"service_bgp":0,"service_courier":0,"service_csnet_ns":0,"service_ctf":0,"service_daytime":0,"service_discard":0,"service_domain":0,"service_domain_u":0,"service_echo":0,"service_eco_i":0,"service_ecr_i":1,"service_efs":0,"service_exec":0,"service_finger":0,"service_ftp":0,"service_ftp_data":0,"service_gopher":0,"service_hostnames":0,"service_http":0,"service_http_443":0,"service_imap4":0,"service_iso_tsap":0,"service_klogin":0,"service_kshell":0,"service_ldap":0,"service_link":0,"service_login":0,"service_mtp":0,"service_name":0,"service_netbios_dgm":0,"service_netbios_ns":0,"service_netbios_ssn":0,"service_netstat":0,"service_nnsp":0,"service_nntp":0,"service_ntp_u":0,"service_other":0,"service_pop_2":0,"service_pop_3":0,"service_printer":0,"service_private":0,"service_remote_job":0,"service_rje":0,"service_shell":0,"service_smtp":0,"service_sql_net":0,"service_ssh":0,"service_sunrpc":0,"service_supdup":0,"service_systat":0,"service_telnet":0,"service_tim_i":0,"service_time":0,"service_urh_i":0,"service_urp_i":0,"service_uucp":0,"service_uucp_path":0,"service_vmnet":0,"service_whois":0,"flag_OTH":0,"flag_REJ":0,"flag_RSTO":0,"flag_RSTOS0":0,"flag_RSTR":0,"flag_S0":0,"flag_S1":0,"flag_S2":0,"flag_S3":0,"flag_SF":1,"flag_SH":0}' \
   'http://localhost:8000/is_intrusion'
```

### Negative:

This example is not predicted as an intrusion.


```bash
curl -H "Content-type: application/json" -d '{"duration":0,"src_bytes":0.000029402154885878748,"dst_bytes":0,"land":0,"wrong_fragment":0,"urgent":0,"hot":0,"num_failed_logins":0,"logged_in":1,"num_compromised":0,"root_shell":0,"su_attempted":0,"num_root":0,"num_file_creations":0,"num_shells":0,"num_access_files":0,"is_guest_login":0,"count":0.019569471624266144,"srv_count":0.019569471624266144,"serror_rate":0,"srv_serror_rate":0,"rerror_rate":0,"srv_rerror_rate":0,"same_srv_rate":1,"diff_srv_rate":0,"srv_diff_host_rate":0,"dst_host_count":0.4627450980392157,"dst_host_srv_count":0.10980392156862745,"dst_host_same_srv_rate":0.24,"dst_host_diff_srv_rate":0.03,"dst_host_same_src_port_rate":0.24,"dst_host_srv_diff_host_rate":0,"dst_host_serror_rate":0,"dst_host_srv_serror_rate":0,"dst_host_rerror_rate":0,"dst_host_srv_rerror_rate":0,"protocol_type_icmp":0,"protocol_type_tcp":1,"protocol_type_udp":0,"service_IRC":0,"service_X11":0,"service_Z39_50":0,"service_auth":0,"service_bgp":0,"service_courier":0,"service_csnet_ns":0,"service_ctf":0,"service_daytime":0,"service_discard":0,"service_domain":0,"service_domain_u":0,"service_echo":0,"service_eco_i":0,"service_ecr_i":0,"service_efs":0,"service_exec":0,"service_finger":0,"service_ftp":0,"service_ftp_data":1,"service_gopher":0,"service_hostnames":0,"service_http":0,"service_http_443":0,"service_imap4":0,"service_iso_tsap":0,"service_klogin":0,"service_kshell":0,"service_ldap":0,"service_link":0,"service_login":0,"service_mtp":0,"service_name":0,"service_netbios_dgm":0,"service_netbios_ns":0,"service_netbios_ssn":0,"service_netstat":0,"service_nnsp":0,"service_nntp":0,"service_ntp_u":0,"service_other":0,"service_pop_2":0,"service_pop_3":0,"service_printer":0,"service_private":0,"service_remote_job":0,"service_rje":0,"service_shell":0,"service_smtp":0,"service_sql_net":0,"service_ssh":0,"service_sunrpc":0,"service_supdup":0,"service_systat":0,"service_telnet":0,"service_tim_i":0,"service_time":0,"service_urh_i":0,"service_urp_i":0,"service_uucp":0,"service_uucp_path":0,"service_vmnet":0,"service_whois":0,"flag_OTH":0,"flag_REJ":0,"flag_RSTO":0,"flag_RSTOS0":0,"flag_RSTR":0,"flag_S0":0,"flag_S1":0,"flag_S2":0,"flag_S3":0,"flag_SF":1,"flag_SH":0}' \
   'http://localhost:8000/is_intrusion'
```

# Visualizing metrics on grafana

1. Access the dashboard on http://localhost:3000/d/_dvc_intrusion_detection_api/dvc-intrusion-detection-api-metrics?refresh=5s
   - Credentials:
      - user: admin
      - password: admin

# Reference

The Prometheus and Grafana setups were based on the public repository: https://github.com/Kludex/fastapi-prometheus-grafana