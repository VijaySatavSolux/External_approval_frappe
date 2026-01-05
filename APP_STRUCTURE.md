# App Structure

This document describes the structure of the External Approval and Digital Sign Frappe app.

## Directory Structure

```
external_approval_digital_sign/
├── external_approval_digital_sign/          # Main app package
│   ├── __init__.py                          # Package initialization
│   ├── hooks.py                             # Frappe hooks configuration
│   ├── install.py                           # Installation hooks
│   ├── api/                                 # API endpoints
│   │   ├── __init__.py
│   │   └── approval.py                      # Approval API endpoints
│   ├── utils/                               # Utility functions
│   │   ├── __init__.py
│   │   └── workflow.py                      # Workflow handlers
│   └── external_approval_digital_sign/      # Module package
│       ├── __init__.py
│       ├── module.json                      # Module metadata
│       ├── modules.txt                      # Module list
│       ├── doctype/                         # Custom DocTypes
│       │   ├── external_approval/           # External Approval DocType
│       │   │   ├── external_approval.json
│       │   │   └── external_approval.py
│       │   └── external_approval_configuration/  # Configuration DocType
│       │       ├── external_approval_configuration.json
│       │       └── external_approval_configuration.py
│       ├── web_page/                        # Web pages
│       │   └── approval/                    # Approval page
│       │       ├── approval.json
│       │       ├── approval.py
│       │       └── approval.html
│       └── web_template/                    # Web templates
│           └── approval_page/
│               └── approval_page.json
├── setup.py                                 # Python package setup
├── requirements.txt                         # Python dependencies
├── README.md                                # Main documentation
├── INSTALLATION.md                          # Installation guide
├── CONTRIBUTING.md                          # Contribution guidelines
├── LICENSE                                  # MIT License
└── .gitignore                              # Git ignore rules
```

## Key Components

### 1. DocTypes

#### External Approval Configuration
- **Purpose**: Configure which doctypes should have external approval enabled
- **Key Fields**:
  - `doctype_name`: The doctype to enable
  - `workflow_state_for_external_approval`: State that triggers approval
  - `workflow_state_after_approval`: State after approval
  - `signature_field_name`: Field to store signature
  - `signature_format`: Format of signature (Name - Date, etc.)

#### External Approval
- **Purpose**: Track individual approval requests
- **Key Fields**:
  - `reference_doctype` & `reference_docname`: Link to document
  - `client_email`: Client email address
  - `approval_token`: Unique token for approval link
  - `status`: Pending/Approved/Rejected
  - `signature_name`, `signature_date`, `signature_value`: Signature data

### 2. API Endpoints (`api/approval.py`)

- `get_approval_page(token)`: Get approval page data
- `submit_approval(token, action, ...)`: Submit approval/rejection

### 3. Workflow Handler (`utils/workflow.py`)

- `handle_workflow_state_change()`: Triggered when document workflow state changes
- `send_approval_email()`: Send approval email to client
- `validate_signature_field()`: Validate signature field exists

### 4. Web Page (`web_page/approval/`)

- **Route**: `/approval?token=<token>`
- **Purpose**: Client-facing approval interface
- **Features**:
  - Display document details
  - Signature capture form
  - Approve/Reject buttons

### 5. Hooks (`hooks.py`)

- Document events: `on_update_after_submit` for workflow state changes
- Installation hooks: `after_install`

## Workflow

1. **Document State Change**: Document reaches configured workflow state
2. **Auto-Trigger**: `handle_workflow_state_change()` is called
3. **Create Approval**: External Approval record created with unique token
4. **Send Email**: Approval email sent to client with link
5. **Client Action**: Client clicks link, reviews, and approves/rejects
6. **Update Document**: On approval, signature saved and workflow state updated
7. **Notification**: Email sent to document owner

## Customization Points

1. **Email Templates**: Modify email content in `utils/workflow.py` and `api/approval.py`
2. **Client Email Field**: Modify field names in `utils/workflow.py` (line 52)
3. **Signature Format**: Add new formats in `api/approval.py` `format_signature()` function
4. **Portal Design**: Modify `web_page/approval/approval.html`
5. **Approval Logic**: Extend `api/approval.py` `submit_approval()` function

## Security Considerations

- Approval tokens are cryptographically secure (secrets.token_urlsafe)
- Tokens are unique and non-guessable
- Approval links expire when status changes from Pending
- Guest access is allowed only for approval endpoints with valid token

