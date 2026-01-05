# Installation Guide

## Prerequisites

- Frappe Framework (v14.0.0 or higher)
- Bench CLI installed

## Installation Steps

1. **Navigate to your bench directory:**
```bash
cd /path/to/your/bench
```

2. **Get the app:**
```bash
bench get-app external_approval_digital_sign /path/to/external_approval_digital_sign --skip-assets
```

Or if you're installing from a git repository:
```bash
bench get-app external_approval_digital_sign https://github.com/VijaySatavSolux/External_approval_frappe.git --skip-assets
```

**Note:** Use the `--skip-assets` flag to avoid build errors since this app doesn't require frontend asset compilation.

3. **Install the app:**
```bash
bench install-app external_approval_digital_sign --skip-assets
```

4. **Migrate the database:**
```bash
bench migrate
```

5. **Restart bench:**
```bash
bench restart
```

## Configuration

### Step 1: Add Signature Field to Your DocType

Before configuring external approval, you need to add a signature field to your doctype:

1. Go to **Customize Form** → Select your DocType
2. Add a new field:
   - **Field Name**: `client_signature` (or any name you prefer)
   - **Field Type**: `Data` or `Small Text`
   - **Label**: `Client Signature`
3. Save

### Step 2: Configure External Approval

1. Go to **External Approval Configuration**
2. Create a new record:
   - **DocType Name**: Select the doctype you want to enable (e.g., "Quotation", "Sales Order")
   - **Is Active**: Check this box
   - **Workflow State for External Approval**: Enter the workflow state that should trigger external approval (e.g., "Pending Client Approval")
   - **Workflow State After Approval**: Enter the workflow state after client approves (e.g., "Client Approved")
   - **Signature Field Name**: Enter the field name you created (e.g., "client_signature")
   - **Signature Format**: Choose the format (Name - Date, Date - Name, or Name on Date)
3. Save

### Step 3: Set Up Workflow (if not already done)

1. Go to **Workflow** → Create a new workflow
2. Configure states and transitions:
   - Create state: "Pending Client Approval" (or your chosen state)
   - Create state: "Client Approved" (or your chosen state)
   - Add transition from "Pending Client Approval" to "Client Approved"
3. Assign the workflow to your doctype

### Step 4: Ensure Your DocType Has Client Email Field

The app looks for client email in these fields (in order):
- `customer_email`
- `client_email`
- `email`
- `contact_email`

Make sure your doctype has at least one of these fields, or modify the workflow.py file to use your custom field name.

## Usage

1. When a document reaches the configured workflow state, the system will:
   - Automatically create an External Approval record
   - Generate a unique approval link
   - Send an email to the client with the approval link

2. Client clicks the link and sees:
   - Document details
   - Approval form with signature fields

3. Client approves/rejects:
   - On approval: Signature is captured and document workflow state changes
   - On rejection: Document owner is notified

## Troubleshooting

### Email Not Sending
- Check Email Queue in Frappe
- Verify email settings in System Settings
- Check spam folder

### Workflow State Not Changing
- Verify workflow is assigned to the doctype
- Check that workflow states match exactly (case-sensitive)
- Ensure document is submitted (docstatus = 1)

### Signature Not Saving
- Verify signature field exists in doctype
- Check field name matches configuration exactly
- Ensure field is not read-only

## Support

For issues or questions, please contact support or create an issue in the repository.

