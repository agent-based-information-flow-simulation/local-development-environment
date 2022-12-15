#!/bin/bash

function usage() {
    echo "Usage: $0 {start|stop|clean|stats|publish|unit-test|mongo-dump|mongo-restore}"
    echo "       start [-d: dev mode, -k: do not detach]: start the server"
    echo "       stop: stop the server"
    echo "       clean: stop the server and remove all docker data"
    echo "       stats: print stats from all services"
    echo "       publish: publish the images to the registry"
    echo "       unit-test SERVICE: run the unit-test suite for the given service"
    echo "       mongo-dump CONTAINER HOST_DESTINATION: dump the mongo database"
    echo "       mongo-restore CONTAINER HOST_SOURCE: restore the mongo database"
    exit 1
}

function start() {
    DEV=0
    DETACH=1
    while getopts dk opt; do
        case $opt in
            d) DEV=1 ;;
            k) DETACH=0 ;;
            *) usage ;;
        esac
    done

    if [ "$DEV" -eq "1" ]; then
        COMPOSE_FILE=docker-compose.dev.yml
    else
        COMPOSE_FILE=docker-compose.yml
    fi

    if [ "$DETACH" -eq "0" ]; then
        DETACH_FLAG="--"
    else
        DETACH_FLAG="--detach"
    fi

    source .version
    if env VERSION="${VERSION}" docker compose --file ./"$COMPOSE_FILE" up --build "$DETACH_FLAG"; then
        echo "Version: ${VERSION}"
        echo "OK"
    else
        echo ""
        echo "failed to start the server"
    fi
}

function stop() {
    docker compose --file ./docker-compose.dev.yml stop --timeout 5
    docker compose --file ./docker-compose.test.yml stop --timeout 5
    docker compose --file ./docker-compose.yml stop --timeout 5
}

function clean() {
    stop
    docker compose --file ./docker-compose.dev.yml down --timeout 5
    docker compose --file ./docker-compose.test.yml down --timeout 5 
    docker compose --file ./docker-compose.yml down --timeout 5
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

    SUCCESS=1

    if [ "$SUCCESS" -eq "1" ] && [ "$VERSION_ANSWER" == "y" ]; then
        SUCCESS=0
        env VERSION="${VERSION}" docker compose --file docker-compose.yml build --parallel && \
        env VERSION="${VERSION}" docker compose --file docker-compose.yml push && \
        echo "published version ${VERSION}" && \
        SUCCESS=1
    fi

    if [ "$SUCCESS" -eq "1" ] && [ "$LATEST_ANSWER" == "y" ]; then
        SUCCESS=0
        env VERSION=latest docker compose --file docker-compose.yml build --parallel && \
        env VERSION=latest docker compose --file docker-compose.yml push && \
        echo "published version latest" && \
        SUCCESS=1
    fi
}

function unit-test() {
    if [ -z "${1}" ]; then
        echo "missing service name"
        usage
    fi
    docker compose --file docker-compose.test.yml up "$1" --build
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
