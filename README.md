# Overview
Secret-scanner is a Python-based tool designed to scan GitHub repositories or directories for exposed credentials and sensitive information. By integrating powerful secret scanning tools like **TruffleHog** and **Gitleaks**, alongside **custom regex rules**, this tool offers a robust solution for identifying security risks in Git repositories.

It’s designed to be flexible—allowing both **independent scanning** and integration into larger workflows, like **giturl-scanner**.
With this tool, you can scan for hardcoded credentials,  API keys, tokens, and other sensitive data that may be leaked in your codebase.
