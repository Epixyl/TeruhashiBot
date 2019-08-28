#! /bin/bash
until python3 login.py; do
    echo "'TeruhashiBot' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
