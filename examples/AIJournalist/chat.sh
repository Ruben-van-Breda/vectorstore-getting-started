#!/bin/bash
QUERY="$1"
SYSTEM_MSG="You are a custom support agent for Siperb. Focused mainly on onboarding the client and making it an easy process."
python3 ../../ChatAgent.py -q "${QUERY}" -sys "${SYSTEM_MSG}"
