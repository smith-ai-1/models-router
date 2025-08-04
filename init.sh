#!/usr/bin/env zsh

source .venv/bin/activate
export $(grep -v '^#' .env.local)

