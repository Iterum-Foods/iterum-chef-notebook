# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously and appreciate your help in identifying and responsibly disclosing vulnerabilities.

### How to Report

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Email security details to: security@iterum-foods.com
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 7 days
- **Regular Updates**: We will keep you informed of our progress
- **Resolution**: We aim to resolve critical issues within 30 days

### Security Response Process

1. **Triage**: We will triage and assess the vulnerability
2. **Investigation**: Our security team will investigate the issue
3. **Fix Development**: We will develop and test a fix
4. **Release**: We will release the fix in the next security update
5. **Disclosure**: We will coordinate disclosure with the reporter

## Security Features

### Current Security Measures

- **XSS Protection**: Safe HTML injection with input sanitization
- **Data Encryption**: AES-GCM encryption for sensitive localStorage data
- **Content Security Policy (CSP)**: Comprehensive security headers
- **Input Validation**: Robust validation for all user inputs
- **API Security**: Secure fetch wrapper with request sanitization
- **Security Monitoring**: Real-time violation logging and reporting

### Security Scanning

We regularly perform security scans:

- **Automated Scans**: Weekly security scans via GitHub Actions
- **Dependency Audits**: Regular npm audit and Snyk scans
- **Code Analysis**: CodeQL and Semgrep analysis
- **Secrets Detection**: Gitleaks for secret detection

### Security Best Practices

#### For Users

1. **Keep Updated**: Always use the latest version of the application
2. **Secure Environment**: Run the application in a secure environment
3. **Data Backup**: Regularly backup your data
4. **Access Control**: Use strong authentication and access controls

#### For Developers

1. **Secure Coding**: Follow secure coding practices
2. **Input Validation**: Always validate and sanitize user inputs
3. **Dependency Management**: Keep dependencies updated
4. **Security Testing**: Include security testing in development process

## Vulnerability Disclosure

### Responsible Disclosure

We follow responsible disclosure practices:

- **Private Disclosure**: Vulnerabilities are disclosed privately first
- **Coordinated Release**: We coordinate with researchers on disclosure timing
- **Credit**: We give credit to security researchers (unless they prefer anonymity)
- **No Legal Action**: We will not take legal action against researchers who follow this policy

### Disclosure Timeline

- **Critical**: 7 days for initial response, 30 days for fix
- **High**: 14 days for initial response, 60 days for fix
- **Medium**: 30 days for initial response, 90 days for fix
- **Low**: 60 days for initial response, 120 days for fix

## Security Updates

### Release Schedule

- **Critical**: Immediate release
- **High**: Within 7 days
- **Medium**: Within 30 days
- **Low**: Within 90 days

### Update Notifications

- **GitHub Releases**: All security updates are tagged and released
- **Security Advisories**: Critical issues are published as security advisories
- **Email Notifications**: Subscribers receive email notifications for critical updates

## Security Contact

- **Email**: security@iterum-foods.com
- **Response Time**: 48 hours for acknowledgment
- **PGP Key**: Available upon request

## Security Resources

### Documentation

- [Security Implementation Summary](SECURITY_IMPLEMENTATION_SUMMARY.md)
- [GitHub Security Advisories](https://github.com/Iterum-Foods/iterum-chef-notebook/security/advisories)
- [Dependency Security](https://github.com/Iterum-Foods/iterum-chef-notebook/security/dependabot)

### Tools and Services

- **GitHub Security**: Code scanning and dependency alerts
- **Snyk**: Vulnerability scanning and monitoring
- **CodeQL**: Static analysis security testing
- **Semgrep**: Static analysis security testing
- **Gitleaks**: Secret detection and prevention

## Security Metrics

We track and report on security metrics:

- **Vulnerability Response Time**: Average time to respond to reports
- **Fix Deployment Time**: Average time to deploy fixes
- **Security Scan Coverage**: Percentage of code covered by security scans
- **Dependency Update Frequency**: How often dependencies are updated

## Compliance

### Standards and Frameworks

- **OWASP Top 10**: Protection against common web vulnerabilities
- **NIST Cybersecurity Framework**: Security best practices
- **ISO 27001**: Information security management
- **SOC 2**: Security, availability, and confidentiality controls

### Certifications

- **Security Audits**: Regular third-party security audits
- **Penetration Testing**: Annual penetration testing
- **Vulnerability Assessments**: Quarterly vulnerability assessments

## Incident Response

### Security Incident Process

1. **Detection**: Monitor for security incidents
2. **Assessment**: Assess the severity and impact
3. **Containment**: Contain the incident to prevent further damage
4. **Investigation**: Investigate the root cause
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Document and learn from the incident

### Incident Communication

- **Internal**: Immediate notification to security team
- **External**: Coordinated communication with affected parties
- **Public**: Transparent communication about incidents and fixes

## Security Training

### Team Training

- **Security Awareness**: Regular security awareness training
- **Secure Coding**: Secure coding practices training
- **Incident Response**: Incident response procedures training

### User Education

- **Security Guides**: User security guides and best practices
- **Training Materials**: Security training materials for users
- **Documentation**: Comprehensive security documentation

---

**Last Updated**: January 2025  
**Next Review**: July 2025

For questions about this security policy, please contact security@iterum-foods.com.
