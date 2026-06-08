# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in this repository or any of the agent implementations, please report it responsibly:

1. **Email**: ashishpatel.ce.2011@gmail.com with subject `[SECURITY] 500-AI-Agents-Projects`
2. **GitHub**: Use [GitHub's private security advisory](https://github.com/ashishpatel26/500-AI-Agents-Projects/security/advisories/new)

### What to include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response timeline

- Acknowledgement within **48 hours**
- Status update within **7 days**
- Fix or mitigation within **30 days** (depending on severity)

## Security Best Practices for Agent Implementations

When using or contributing agent code from this repo:

- **Never hardcode API keys** — always use `.env` files or environment variables
- **Never commit `.env` files** — they are gitignored by default
- **Validate external inputs** before passing to LLM agents
- **Review tool permissions** — agents with code execution can be dangerous if misconfigured
- **Use least-privilege API keys** — restrict API key scopes to what the agent actually needs
