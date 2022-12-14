#!/bin/bash

function usage() {
    echo "Usage: $0 {start|stop|clean|stats|publish|unit-test|mongo-dump|mongo-restore}"
    echo "       start [-d: dev mode]: start the server"
    echo "       stop: stop the server"
    echo "       clean: stop the server and remove all docker data"
    echo "       stats: print stats from all services"
    echo "       publish: publish the images to a registry"
    echo "       unit-test SERVICE: run the unit-test suite for the given service"
    echo "       mongo-dump CONTAINER HOST_DESTINATION: dump the mongo database"
    echo "       mongo-restore CONTAINER HOST_SOURCE: restore the mongo database"
    exit 1
}

function start() {
    DEV=0
    PUBLISH=0
    while getopts dp opt; do
        case $opt in
            d) DEV=1 ;;
            *) usage ;;
        esac
    done

    if [ "$DEV" -eq "1" ]; then
        COMPOSE_FILE=docker-compose.dev.yml
    else
        COMPOSE_FILE=docker-compose.yml
    fi

    source .version
    if env VERSION="${VERSION}" docker-compose -f ./"$COMPOSE_FILE" up --build; then
        echo "Version: ${VERSION}"
        echo "OK"
    else
        echo ""
        echo "failed to start the server"
    fi
}

function stop() {
    docker stack rm sre
}

function clean() {
    stop
    docker swarm leave --force
    docker system prune --all --volumes
}

function stats() {
    docker stats
}

function publish() {
    local OPTIND

    source .version
    read -p "Publish version ${VERSION} to registry? [y/n] " -r VERSION_ANSWER
    read -p "Publish version latest to registry? [y/n] " -r LATEST_ANSWER

    if [ "$VERSION_ANSWER" != "y" ] && [ "$LATEST_ANSWER" != "y" ]; then
        echo "aborting"
        exit 1
    fi

    if [ "$VERSION_ANSWER" == "y" ]; then
        env VERSION="${VERSION}" docker-compose -f docker-compose.yml build --parallel && \
        env VERSION="${VERSION}" docker-compose -f docker-compose.yml push && \
        echo "published version ${VERSION}"
    fi

    if [ "$LATEST_ANSWER" == "y" ]; then
        env VERSION=latest docker-compose -f docker-compose.yml build --parallel && \
        env VERSION=latest docker-compose -f docker-compose.yml push && \
        echo "published version latest"
    fi
}

function unit-test() {
    if [ -z "${1}" ]; then
        echo "missing service name"
        usage
    fi
    docker-compose -f docker-compose.test.yml up "$1" --build
}

function mongo-dump() {
    if [ -z "$1" ]; then
        echo "missing container name"
        usage
    elif [ -z "$2" ]; then
        echo "missing host destination"
        usage
    fi
    ID=$RANDOM
    docker exec -it "${1}" mongodump --username root --password root --authenticationDatabase admin --db simulations --out /opt/bitnami/mongodb/dump_"$ID" && \
    docker cp "${1}":/opt/bitnami/mongodb/dump_"$ID"/simulations "${2}" && \
    docker exec -it "${1}" rm -rf /opt/bitnami/mongodb/dump_"$ID"
}

function mongo-restore() {
    if [ -z "$1" ]; then
        echo "missing container name"
        usage
    elif [ -z "$2" ]; then
        echo "missing host source"
        usage
    fi
    ID=$RANDOM
    docker exec -it "${1}" mkdir -p /opt/bitnami/mongodb/dump_"$ID" && \
    docker cp "${2}" "${1}":/opt/bitnami/mongodb/dump_"$ID" && \
    docker exec -it "${1}" mongorestore --username root --password root --authenticationDatabase admin --db simulations --drop /opt/bitnami/mongodb/dump_"$ID"/simulations
}

case "${1}" in
    start) start "${@:2}" ;;

    stop) stop ;;

    clean) clean ;;

    stats) stats ;;

    publish) publish "${@:2}" ;;

    unit-test) unit-test "${2}" ;;

    mongo-dump) mongo-dump "${2}" "${3}" ;;

    mongo-restore) mongo-restore "${2}" "${3}" ;;

    *) usage ;;
esac
