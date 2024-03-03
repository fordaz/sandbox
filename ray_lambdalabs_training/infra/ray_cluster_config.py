import yaml
import click
import json

config_template = {
    "cluster_name": "default",
    "docker": {
        "image": "rayproject/ray-ml:latest-gpu",
        "container_name": "ray_container",
        "pull_before_run": True,
        "run_options": ["--ulimit nofile=65536:65536", "--gpus all"],
    },
    "provider": {
        "type": "local",
        "head_ip": "YOUR_HEAD_NODE_HOSTNAME",
        "worker_ips": ["WORKER_NODE_1_HOSTNAME", "WORKER_NODE_2_HOSTNAME", "..."],
    },
    "auth": {"ssh_user": "YOUR_USERNAME"},
    "min_workers": "TYPICALLY_THE_NUMBER_OF_WORKER_IPS",
    "max_workers": "TYPICALLY_THE_NUMBER_OF_WORKER_IPS",
    "upscaling_speed": 1.0,
    "idle_timeout_minutes": 5,
    "file_mounts": {},
    "cluster_synced_files": [],
    "file_mounts_sync_continuously": False,
    "rsync_exclude": ["**/.git", "**/.git/**"],
    "rsync_filter": [".gitignore"],
    "initialization_commands": [],
    "setup_commands": [],
    "head_setup_commands": [],
    "worker_setup_commands": [],
    "head_start_ray_commands": [
        "ray stop",
        "ulimit -c unlimited && ray start --num-gpus 1 --head --port=6379 --autoscaling-config=~/ray_bootstrap_config.yaml",
    ],
    "worker_start_ray_commands": ["ray stop", "ray start --num-gpus 1 --address=$RAY_HEAD_IP:6379"],
}

def get_infra_ips(state_file, head_node_name):
    with open(state_file, "r") as f:
        try:
            state_payload = json.load(f)
            head_node_ip, worker_ips = "", []
            for instance in state_payload["instances"]:
                if instance["name"] == head_node_name:
                    head_node_ip = instance["ip"]
                    continue
                else:
                    worker_ips.append(instance["ip"])
            return head_node_ip, worker_ips
        except Exception as e:
            print(e)
        return None, []

def save_template(config_template, output_file):
    with open(output_file, "w") as stream:
        try:
            yaml.safe_dump(config_template, stream)
        except yaml.YAMLError as exc:
            print(exc)

@click.command()
@click.option("--ssh_key_file", required=True)
@click.option("--head_node_name", required=True)
@click.option("--output_file", required=True)
def generate(ssh_key_file, head_node_name, output_file):
    head_ip, worker_ips = get_infra_ips("infra_state.json", head_node_name)
    config_template["auth"]["ssh_user"] = "ubuntu"
    config_template["auth"]["ssh_private_key"] = ssh_key_file
    config_template["provider"]["head_ip"] = head_ip
    config_template["provider"]["worker_ips"] = worker_ips
    config_template["min_workers"] = max(1, len(worker_ips))
    config_template["max_workers"] = max(1, len(worker_ips))
    save_template(config_template, output_file)

generate()