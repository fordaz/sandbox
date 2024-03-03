#!/bin/zsh

usage="Usage: ./generate_ray_config.sh --head_node_name=<your_head_node> --output_file=<output_ray_config>\n"

if [ $# -eq 0 ]
  then
      printf $usage
      exit 1
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --ssh_key_file=*)
      ssh_key_file="${1#*=}"
      ;;
    --head_node_name=*)
      head_node_name="${1#*=}"
      ;;
    --output_file=*)
      output_file="${1#*=}"
      ;;
    *)
      printf "Invalid argument $1\n"
      printf "Usage: ./generate_ray_config.sh --head_node_name=<your_head_node> --output_file=<output_ray_config>\n"
      exit 1
  esac
  shift
done

echo "Generating ray config file $output_file using IP from $head_node_name instance"

python ./infra/ray_cluster_config.py --ssh_key_file=$ssh_key_file --head_node_name=$head_node_name --output_file=$output_file