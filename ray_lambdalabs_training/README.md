# Motivation

The idea of this PoC was to play with [Ray Train](https://docs.ray.io/en/latest/train/train.html) on a GPU cluster running on [Lambdalabs](https://lambdalabs.com/). From a practical point of view, this repo provides automation for:

* Setting up one or two Cloud GPU instances in Lambdalabs 
* Setting an [on-prem Ray cluster](https://docs.ray.io/en/latest/cluster/vms/user-guides/launching-clusters/on-premises.html) with GPUs
* Launching a Ray Job to Train Alexnet on Cifar10

NOTE: The Alexnet-cifar10 code is an adaptation of the Sebastian Raschka's [deeplearning-models notebook](https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb)

Apart from playing with Ray Train, the idea was to make the workflow consistent and repeatable by automating each step. You can easily adjust most of the scripts to fit your own needs and do further experimentation.

# Pre-requisites

Configure your Lambdalabs API key using

```bash
export LAMBDALABS_API_KEY=....
```

Use your preferred python package manager of choice and create a environment. For example, using conda you can do:

```bash
conda create -n test_ray_train_lamblbs python=3.8
conda activate test_ray_train_lamblbs
```

Install python dependencies (ex: Pytorch, Ray[Train], [lamblbs CLI](https://pypi.org/project/lambda-cli/))

```
pip install -r requirements.txt
```

NOTE: The end to end testing was done using Python 3.8.

# Setting up the infra

## Setup SSH key

If you already have an ssh key configured in your Lambdalabs account, **you can skip this step**, but if you need a new ssh key you need to run:

```bash
./infra/setup_ssh.sh --ssh_key_name=test-ssh-010
```

```bash
# successful output
Adding key name test-ssh-010
```

This command takes care of:

* Creating a new ssh key via [API on Lambdalabs](https://cloud.lambdalabs.com/api/v1/docs#operation/addSSHKey)
* Saves the pem file in your `~/.ssh` directory

## Setup GPU instances

This command takes care launching one instance as the Ray Cluster head node, and does basic configuration on it. You can change the parameters of the type of instance in the script.

```bash
./infra/setup_infra.sh \
--ssh_key_name=test-ssh-010 \
--head_node_name=ray_head_node
```

```bash
# successful output
Launching instance using key name test-ssh-010 and name ray_head_node

Launch instance with parameters {'region_name': 'us-east-1', 'instance_type_name': 'gpu_1x_a10', 'ssh_key_names': ['test-ssh-010'], 'quantity': 1, 'name': 'ray_head_node'}
{"data": {"instance_ids": ["02c82f26ce3c426ba34c8f6d78afd63b"]}}

Launching instance using key name test-ssh-010 and name ray_head_node
Instance 02c82f26ce3c426ba34c8f6d78afd63b in booting status
...
Saving instances metadata in infra_state.json
List running instances
...
Adding ubuntu to the docker group on all instances
OpenSSH_8.6p1, LibreSSL 3.3.6
...
debug1: channel 0: free: client-session, nchannels 1
Transferred: sent 4340, received 2692 bytes, in 0.7 seconds
Bytes per second: sent 6218.0, received 3856.9
debug1: Exit status 0
```

If the script fails with `Not enough capacity to fulfill launch request` run this command `lamblbs instance --json_output types  | jq .` and find an instance type with non empty `regions_with_capacity_available` that works for you.

# Setting up the Ray Cluster

## Generate Ray Config

At this point we have one or more GPU instances running. Now we need to generate a Ray cluster configuration which refers to the given instance IPs and ssh key.

The next script generates a pretty fixed cluster configuration which works for my testing, but it might not work for your purposes. You can easly enhance the script or just manage your own cluster configuration. Just keep in mind that it needs to refer to the instance IPs and ssh key provisioned in previous steps.

```bash
./infra/generate_ray_config.sh \
--ssh_key_file=~/.ssh/test-ssh-010.pem \
--head_node_name=ray_head_node \
--output_file=ray_cluster_config.yaml
```

```bash
# successful output
Generating ray config file ray_cluster_config.yaml using IP from ray_head_node instance
```

Check the generated Ray config file `ray_cluster_config.yaml` to get yourself familiar with the basic configuration options.

## Launch Ray Cluster

There are different ways to launch and manage Ray Clusters. This particular PoC uses an [on-prem cluster](https://docs.ray.io/en/latest/cluster/vms/user-guides/launching-clusters/on-premises.html) setup, which does not require Kubernetes or VMs. It also relies on the [Cluster Launcher](https://docs.ray.io/en/latest/cluster/vms/references/ray-cluster-configuration.html#cluster-yaml-configuration-options) and the [Ray CLI](https://docs.ray.io/en/latest/cluster/cli.html#ray-cluster-cli) to set it up.

```bash
ray up ray_cluster_config.yaml
```

```bash
Usage stats collection is enabled. To disable this, add `--disable-usage-stats` to the command that starts the cluster, or run the following command: `ray disable-usage-stats` before starting the cluster. See https://docs.ray.io/en/master/cluster/usage-stats.html for more details.

Acquiring an up-to-date head node
2024-03-03 10:19:37,946	INFO node_provider.py:114 -- ...
  Launched a new head node
  Fetching the new head node

<1/1> Setting up head node
  Prepared bootstrap config
2024-03-03 10:19:37,950	INFO node_provider.py:114 -- ...
...
--------------------
Ray runtime started.
--------------------

Next steps
...
```

This will take a few minutes while the Ray Docker images are downloaded, etc.

# Running the training job

## Port forwarding

This command port-forwards a Ray cluster's dashboard to the local machine, making it possible for us to submit jobs from our local machine. Run this command on a different terminal.

```bash
ray dashboard ray_cluster_config.yaml
```

## Submit the Ray Job

At this point we have GPU instances running, a Ray cluster up an running, port-forwarding established and the next step is to submit our Ray job using the Ray CLI.

Change to the train directory `cd train`

```bash
RAY_ADDRESS='http://localhost:8265' ray job submit \
--runtime-env-json='{"pip": ["numpy","torch","torchvision","torchaudio","matplotlib","pandas","ray[train]"]}' \
--working-dir . \
-- python alexnet_cifar10_ray.py
```

```bash
# successful output 
Job submission server address: http://localhost:8265
2024-03-03 10:25:36,944	INFO dashboard_sdk.py:338 -- Uploading package gcs://_ray_pkg_9f965c1a911ba9f2.zip.
2024-03-03 10:25:36,946	INFO packaging.py:530 -- Creating a file package for local directory '.'.

-------------------------------------------------------
Job 'raysubmit_d4jjY6ydDdFSQeNs' submitted successfully
-------------------------------------------------------
...
(RayTrainWorker pid=2694) {'loss': 1.5134904384613037, 'epoch': 0}
(RayTrainWorker pid=2694) Epoch: 001/001 | Train. Acc.: 30.842% | Loss: 1.8459
(RayTrainWorker pid=2694) Epoch: 001/001 | Valid. Acc.: 30.700% | Loss: 1.8269
(RayTrainWorker pid=2694) Time elapsed: 0.58
(RayTrainWorker pid=2694) Total Training Time: 0.58
(RayTrainWorker pid=2694) Train ACC: 30.93%
(RayTrainWorker pid=2694) Validation ACC: 30.72%
(RayTrainWorker pid=2694) Test ACC: 30.66%

Training completed after 1 iterations at 2024-03-03 10:26:45. Total running time: 58s

------------------------------------------
Job 'raysubmit_d4jjY6ydDdFSQeNs' succeeded
------------------------------------------
```

Comments on this command:

* Include your dependencies on the `runtime-env-json` as needed.
* Try to keep your local `working-dir` small as Ray will try to upload everything stored in there, and if it is tool large it might fail. In some cases, it might be better to download large artifacts directly from the cloud instance before that.
* This is running for one epoch just for illustration purposes.

# Clean up

Once you are done with your excercise, you can tear down both the Ray Cluster and the GPU instances. Please make sure you save any artifacts or data from your cloud instances.

From the repo root directory run:

```bash
./infra/tear_down.sh --config_file=ray_cluster_config.yaml
```

```bash
# successful output

Shutdown the cluster with config file ray_cluster_config.yaml
...
Fetched IP: 129.159.84.134
Stopped all 6 Ray processes.
...
No nodes remaining.
...
Terminating instances
Terminate instance 02c82f26ce3c426ba34c8f6d78afd63b
...
```

Just in case, check your [Lambdalabs console](https://cloud.lambdalabs.com/instances) to verify the instances are terminating.

# Future work

* Enhance scripts to handle multiple worker nodes, and different configuration options
    * instance types
    * attached volumes
    * regions
* Integrate Ray Train with MLFlow to manage model experiments and model versions
* Add Ray Serve to complete the train-serve workflow
