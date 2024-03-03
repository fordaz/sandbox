#!/bin/zsh
set -e

usage="Usage: ./setup_infra.sh --ssh_key_name=<your_ssh_key_name> --head_node_name=<your_head_node>\n"

if [ $# -eq 0 ]
  then
      printf $usage
      exit 1
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --ssh_key_name=*)
      ssh_key_name="${1#*=}"
      ;;
    --head_node_name=*)
      head_node_name="${1#*=}"
      ;;
    *)
      printf "Invalid argument $1\n"
      printf $usage
      exit 1
  esac
  shift
done

echo "Launching instance using key name $ssh_key_name and name $head_node_name"

# Launching the Ray header node with with some pre-defined configuration
lamblbs instance launch --name "$head_node_name" \
--type gpu_1x_a10 \
--region us-east-1 \
--ssh_key "$ssh_key_name" \
--qty 1

# Uncomment this if you need Ray worker nodes.
# lamblbs instance launch --name ray-worker-node \
# --type gpu_1x_a10 \
# --region us-east-1 \
# --ssh_key lambdalabs-ssh-ray \
# --qty 1

# Waits until all the instances are active and fully operational
lamblbs instance check-status --status active

echo "Saving instances metadata in infra_state.json"

# Saves the instances metadata into the infra_state.json so later steps can refer to it 
lamblbs instance show-all --state_file infra_state.json

echo "Adding ubuntu to the docker group on all instances"

# adding ubuntu user to the docker group so the "ray up" can execute docker commands
for ip in `jq -r '.instances[].ip' infra_state.json`
do
    ssh -v -o "StrictHostKeyChecking no" -i ~/.ssh/"$ssh_key_name".pem ubuntu@$ip "sudo usermod -aG docker ubuntu"
done

