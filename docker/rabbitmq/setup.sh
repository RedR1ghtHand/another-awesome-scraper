#!/bin/bash
set -eu

echo "RabbitMQ username: $RABBITMQ_USERNAME"
echo "RabbitMQ virtual host: $RABBITMQ_VIRTUAL_HOST"

(
# Sleep to allow RabbitMQ to initialize its files in the mounted directory
sleep 10

# Wait for RabbitMQ to fully start
echo "Waiting for RabbitMQ to start..."
rabbitmqctl await_startup
echo "RabbitMQ is fully started!"

# Check if the default "guest" user exists
if rabbitmqctl list_users | grep -q guest; then
    echo "Setting up new user..."

    # Create new user
    rabbitmqctl add_user "$RABBITMQ_USERNAME" "$RABBITMQ_PASSWORD"
    rabbitmqctl set_user_tags "$RABBITMQ_USERNAME" administrator

    # Create and configure virtual host
    rabbitmqctl add_vhost "$RABBITMQ_VIRTUAL_HOST"
    rabbitmqctl set_permissions -p / "$RABBITMQ_USERNAME" ".*" ".*" ".*"
    rabbitmqctl set_permissions -p "$RABBITMQ_VIRTUAL_HOST" "$RABBITMQ_USERNAME" ".*" ".*" ".*"

    echo "User setup completed!"
else
    echo "User already set up, skipping..."
fi
) &

# Call original RabbitMQ entrypoint
exec docker-entrypoint.sh rabbitmq-server "$@"
