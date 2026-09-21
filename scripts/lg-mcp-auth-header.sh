#!/bin/sh
set -eu

settings='/Users/dean/LibraryG/.obsidian/plugins/obsidian-local-rest-api/data.json'

test -r "$settings"
jq -e -cn --arg key "$(jq -er '.apiKey' "$settings")" \
  '{Authorization: ("Bearer " + $key)}'
