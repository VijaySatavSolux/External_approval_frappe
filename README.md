# External Approval and Digital Sign

A plug-and-play Frappe app that enables external client approval workflows with digital signature capture for any doctype.

> [!NOTE]
> **Compatibility:** Fully compatible with Frappe Framework v15 and v16.

## Features

- **Plug-and-Play**: Easily configure any doctype for external approval workflows
- **Client Portal**: Secure portal interface for clients to review and approve documents
- **Digital Signature**: Capture client name and date signed
- **Workflow Integration**: Seamlessly integrates with Frappe workflows
- **Email Notifications**: Automatic email notifications for approval requests

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

### Quick Start (Recommended)

**Important:** This app requires the `--skip-assets` flag due to its backend-only nature. The installation has been enhanced to automatically register the app even with `--skip-assets`.

```bash
# 1. Get the app
bench get-app external_approval_digital_sign https://github.com/VijaySatavSolux/External_approval_frappe.git --skip-assets

# 2. Install the app
bench install-app external_approval_digital_sign --skip-assets

# 3. Run the fix script (ensures everything is registered)
bench --site your-site-name execute external_approval_digital_sign.fix_installation.fix_installation

# 4. Migrate and restart
bench migrate
bench restart
```

**Note:** 
- The `--skip-assets` flag is required because this app doesn't have frontend assets that need building
- The enhanced installation hooks will automatically register the app in `apps.txt` and create modules
- The fix script is a safety measure to ensure everything is properly registered
- If you encounter issues, see [COMPLETE_INSTALLATION_FIX.md](COMPLETE_INSTALLATION_FIX.md) for detailed troubleshooting

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

