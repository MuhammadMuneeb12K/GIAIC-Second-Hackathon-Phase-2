# Security Policy

## 🔒 Security Best Practices for TaskFlow

This document outlines security best practices for developers and users of TaskFlow.

---

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, please **DO NOT** open a public issue. Instead:

1. **Email us directly**: security@taskflow.com
2. **Include details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within **48 hours** and work with you to resolve the issue.

---

## 🛡️ Security Measures Implemented

### Authentication & Authorization
- ✅ **JWT-based authentication** with access and refresh tokens
- ✅ **Password hashing** using bcrypt (12 rounds)
- ✅ **Token expiration** (15 minutes for access, 7 days for refresh)
- ✅ **Secure password requirements** (minimum 8 characters)
- ✅ **Protected routes** with automatic token validation

### API Security
- ✅ **CORS configuration** with allowed origins
- ✅ **Input validation** using Pydantic schemas
- ✅ **SQL injection prevention** via SQLAlchemy ORM
- ✅ **Rate limiting** (recommended for production)
- ✅ **HTTPS enforcement** (recommended for production)

### Data Protection
- ✅ **User isolation** - users can only access their own data
- ✅ **Environment variables** for sensitive configuration
- ✅ **No sensitive data in logs**
- ✅ **Secure database connections**

---

## 🔐 Environment Variables Security

### Critical Rules

1. **NEVER commit `.env` files to Git**
   ```bash
   # Always in .gitignore
   .env
   .env.local
   .env.*
   ```

2. **Use strong, random secret keys**
   ```bash
   # Generate secure keys
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Different secrets for each environment**
   - Development: Use test secrets
   - Staging: Use staging-specific secrets
   - Production: Use strong, unique secrets

4. **Rotate secrets regularly**
   - Change `SECRET_KEY` every 90 days
   - Update database passwords quarterly
   - Rotate API keys when team members leave

### Environment Variable Checklist

- [ ] All `.env` files are in `.gitignore`
- [ ] `.env.example` files contain no real secrets
- [ ] Production secrets are stored securely (e.g., AWS Secrets Manager, Vercel Environment Variables)
- [ ] Secrets are not hardcoded in source code
- [ ] Secrets are not logged or exposed in error messages

---

## 🔒 Password Security

### Requirements
- Minimum 8 characters
- Maximum 72 bytes (bcrypt limitation)
- No common passwords (implement password strength checker)

### Best Practices
- ✅ Use bcrypt for hashing (already implemented)
- ✅ Use 12+ rounds for bcrypt (configurable via `BCRYPT_ROUNDS`)
- ✅ Never store passwords in plain text
- ✅ Never log passwords
- ✅ Implement password reset functionality securely

### User Recommendations
- Use unique passwords for each service
- Use a password manager
- Enable 2FA when available (future feature)

---

## 🌐 HTTPS & Network Security

### Production Requirements

1. **Always use HTTPS**
   ```nginx
   # Nginx example
   server {
       listen 443 ssl http2;
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
   }
   ```

2. **Redirect HTTP to HTTPS**
   ```nginx
   server {
       listen 80;
       return 301 https://$host$request_uri;
   }
   ```

3. **Use secure headers**
   ```python
   # FastAPI middleware
   app.add_middleware(
       SecureHeadersMiddleware,
       hsts=True,
       csp="default-src 'self'"
   )
   ```

---

## 🔑 JWT Token Security

### Current Implementation
- Access tokens expire in 15 minutes
- Refresh tokens expire in 7 days
- Tokens are signed with HS256 algorithm

### Best Practices
- ✅ Store tokens in memory or httpOnly cookies (not localStorage for sensitive apps)
- ✅ Implement token refresh mechanism
- ✅ Invalidate tokens on logout
- ✅ Use short expiration times for access tokens
- ⚠️ Consider implementing token blacklist for logout

### Token Storage Recommendations

**Current (localStorage)**:
```typescript
// Acceptable for this application
localStorage.setItem('access_token', token);
```

**More Secure (httpOnly cookies)**:
```python
# Backend sets httpOnly cookie
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,
    samesite="strict"
)
```

---

## 🗄️ Database Security

### Connection Security
- ✅ Use connection pooling
- ✅ Use parameterized queries (SQLAlchemy handles this)
- ✅ Encrypt database connections in production
- ✅ Use strong database passwords

### Data Protection
- ✅ Implement user isolation (users can only access their data)
- ✅ Regular backups
- ✅ Encrypt sensitive data at rest (for production)
- ✅ Audit database access logs

### PostgreSQL Security Checklist
- [ ] Use SSL/TLS for database connections
- [ ] Restrict database user permissions
- [ ] Enable query logging for auditing
- [ ] Regular security updates
- [ ] Implement backup strategy

---

## 🚦 Rate Limiting

### Recommended Implementation

```python
# FastAPI rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/signin")
@limiter.limit("5/minute")  # 5 attempts per minute
async def signin(request: Request):
    pass
```

### Recommended Limits
- **Authentication endpoints**: 5 requests/minute
- **API endpoints**: 60 requests/minute
- **Public endpoints**: 100 requests/minute

---

## 🔍 Input Validation

### Current Implementation
- ✅ Pydantic schemas validate all inputs
- ✅ Email format validation
- ✅ Password length validation
- ✅ SQL injection prevention via ORM

### Additional Recommendations
- Sanitize HTML inputs (if accepting rich text)
- Validate file uploads (if implemented)
- Implement CSRF protection for state-changing operations
- Validate redirect URLs to prevent open redirects

---

## 🛠️ Dependency Security

### Regular Updates
```bash
# Frontend
npm audit
npm audit fix

# Backend
pip list --outdated
pip install --upgrade package-name
```

### Automated Security Scanning
- Use **Dependabot** (GitHub) for automatic dependency updates
- Use **Snyk** for vulnerability scanning
- Use **npm audit** / **pip-audit** in CI/CD pipeline

### Security Checklist
- [ ] Enable Dependabot alerts
- [ ] Review security advisories regularly
- [ ] Update dependencies monthly
- [ ] Test after updates

---

## 🔐 Secrets Management

### Development
- Use `.env` files (never commit)
- Use `.env.example` as template

### Production

**Option 1: Cloud Provider Secrets**
```bash
# Vercel
vercel env add SECRET_KEY

# Railway
railway variables set SECRET_KEY=xxx

# AWS
aws secretsmanager create-secret --name SECRET_KEY
```

**Option 2: Environment Variables**
- Set via hosting platform dashboard
- Use CI/CD secrets for deployment

**Option 3: Secrets Manager**
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault

---

## 🚨 Common Vulnerabilities to Avoid

### ❌ Don't Do This

1. **Hardcoded Secrets**
   ```python
   # BAD
   SECRET_KEY = "my-secret-key-123"
   ```

2. **Exposed API Keys**
   ```javascript
   // BAD
   const API_KEY = "sk_live_xxxxx";
   ```

3. **SQL Injection**
   ```python
   # BAD
   query = f"SELECT * FROM users WHERE email = '{email}'"
   ```

4. **Weak Passwords**
   ```python
   # BAD
   if len(password) < 4:  # Too short!
   ```

5. **Logging Sensitive Data**
   ```python
   # BAD
   logger.info(f"User password: {password}")
   ```

### ✅ Do This Instead

1. **Use Environment Variables**
   ```python
   # GOOD
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

2. **Use Backend Proxy**
   ```javascript
   // GOOD - API key stays on backend
   const response = await fetch('/api/proxy');
   ```

3. **Use ORM/Parameterized Queries**
   ```python
   # GOOD
   user = db.query(User).filter(User.email == email).first()
   ```

4. **Enforce Strong Passwords**
   ```python
   # GOOD
   if len(password) < 8:
       raise ValueError("Password too short")
   ```

5. **Never Log Secrets**
   ```python
   # GOOD
   logger.info(f"User authenticated: {user.email}")
   ```

---

## 📋 Security Checklist

### Before Deployment

- [ ] All `.env` files are in `.gitignore`
- [ ] Strong, unique `SECRET_KEY` is set
- [ ] Database uses strong password
- [ ] HTTPS is enabled
- [ ] CORS is properly configured
- [ ] Rate limiting is implemented
- [ ] Dependencies are up to date
- [ ] Security headers are set
- [ ] Error messages don't expose internals
- [ ] Logging doesn't include sensitive data

### Regular Maintenance

- [ ] Review security advisories monthly
- [ ] Update dependencies monthly
- [ ] Rotate secrets quarterly
- [ ] Review access logs weekly
- [ ] Backup database daily
- [ ] Test disaster recovery quarterly

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Next.js Security](https://nextjs.org/docs/app/building-your-application/configuring/security)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

---

## 🆘 Incident Response

If a security breach occurs:

1. **Immediately**:
   - Rotate all secrets and tokens
   - Notify affected users
   - Document the incident

2. **Within 24 hours**:
   - Identify the vulnerability
   - Deploy a fix
   - Review logs for impact

3. **Within 1 week**:
   - Conduct post-mortem
   - Update security practices
   - Implement additional safeguards

---

## 📞 Contact

For security concerns:
- **Email**: security@taskflow.com
- **Response Time**: Within 48 hours
- **PGP Key**: Available on request

---

**Last Updated**: January 25, 2026

**Remember**: Security is everyone's responsibility. When in doubt, ask!
