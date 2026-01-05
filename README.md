# External Approval and Digital Sign

A plug-and-play Frappe app that enables external client approval workflows with digital signature capture for any doctype.

## Features

- **Plug-and-Play**: Easily configure any doctype for external approval workflows
- **Client Portal**: Secure portal interface for clients to review and approve documents
- **Digital Signature**: Capture client name and date signed
- **Workflow Integration**: Seamlessly integrates with Frappe workflows
- **Email Notifications**: Automatic email notifications for approval requests

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

Quick start:
```bash
bench get-app external_approval_digital_sign /path/to/external_approval_digital_sign
bench install-app external_approval_digital_sign
bench migrate
bench restart
```

## Configuration

1. **Add Signature Field**: Add a signature field (Data/Small Text type) to your doctype
2. **Configure External Approval**: Go to **External Approval Configuration** and create a new record:
   - Select your doctype
   - Set workflow state that triggers external approval
   - Set workflow state after approval
   - Enter signature field name
   - Choose signature format
3. **Set Up Workflow**: Ensure your doctype has a workflow with the configured states

See [INSTALLATION.md](INSTALLATION.md) for detailed configuration steps.

## Usage

1. When a document reaches the configured workflow state, it will automatically:
   - Generate a unique approval link
   - Send email notification to the client
   - Create an External Approval record

2. Client receives email with approval link

3. Client clicks link, reviews document, and approves/rejects

4. Upon approval:
   - Client name and date are captured in the signature field
   - Document workflow state changes automatically
   - Email notification sent to document owner

## Customization

You can customize:
- Email templates
- Portal page design
- Signature field format
- Approval workflow states

## License

MIT

