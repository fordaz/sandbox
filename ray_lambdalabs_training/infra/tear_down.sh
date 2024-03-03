#!/bin/zsh

usage="Usage: ./tear_down.sh --config_file=<ray_config_file>\n"

if [ $# -eq 0 ]
  then
      printf $usage
      exit 1
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --config_file=*)
      config_file="${1#*=}"
      ;;
    *)
      printf "Invalid argument $1\n"
      printf $usage
      exit 1
  esac
  shift
done

echo "Shutdown the cluster with config file $config_file"
ray down $config_file

echo "Terminating instances"
for id in `jq -r '.instances[].id' infra_state.json`
do
    lamblbs instance terminate --instance_id $id
done



