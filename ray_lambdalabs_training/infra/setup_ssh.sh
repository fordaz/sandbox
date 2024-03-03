#!/bin/zsh

usage="Usage: ./setup_ssh.sh --ssh_key_name=<your_ssh_key_name>\n"

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
    *)
      printf "Invalid argument $1\n"
      printf $usage
      exit 1
  esac
  shift
done

echo "Adding key name $ssh_key_name"

lamblbs ssh --json_output add \
--name $ssh_key_name | jq -r .data.private_key > "$ssh_key_name".pem

chmod 400 "$ssh_key_name".pem
mv "$ssh_key_name".pem ~/.ssh
