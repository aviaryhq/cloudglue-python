# CloudGlue Python SDK

Official Python SDK for the CloudGlue API.

## 📖 Resources

- [CloudGlue API Docs](https://docs.cloudglue.dev)
- [Terms of Service](https://cloudglue.dev/terms)
- [Privacy Policy](https://cloudglue.dev/privacy)
- [Pricing](https://cloudglue.dev/pricing)

> By using this SDK, you agree to the [CloudGlue Terms of Service](https://cloudglue.dev/terms) and acknowledge our [Privacy Policy](https://cloudglue.dev/privacy).


## Installation

You can install the CloudGlue Python SDK using pip:

```bash
pip install cloudglue
```

## Quick Start

```python
from cloudglue import CloudGlue

# Initialize the client
client = CloudGlue(api_key="your_api_key")  # Or use CLOUDGLUE_API_KEY env variable

# Define your messages
messages = [
    {"role": "user", "content": "What are aligned video captions?"}
]

# Make an API request
response = client.chat.completions.create(
    messages=messages,
    model="nimbus-001",
    collections=["abc123"], # Assumes collection already exists, otherwise create one first then reference here by collection id    
)

# Get the generated text
generated_text = response.choices[0].message.content
print(generated_text)
```

## Development

### Prerequisites

- Python 3.10+
- Make (for build tasks)
- Git

### Setup

Clone the repository and set up the development environment:

```bash
git clone https://github.com/aviaryhq/cloudglue-python.git
cd cloudglue-python

brew install openapi-generator
make setup  # This will set up the virtual environment

# Initialize the API spec Git submodule
make submodule-init
```

### API Specification

The OpenAPI specification is maintained in a separate [repository](https://github.com/aviaryhq/cloudglue-api-spec) and included as a Git submodule:

```bash
# Update the API spec to the latest version
make submodule-update

# After updating the spec, regenerate the SDK
make generate
```

### Building

```bash
make generate  # Generate SDK from OpenAPI spec
make build     # Build the package
```

### Project Structure

Project directory structure describe below:

```
cloudglue/
├── __init__.py       # Main package initialization
├── client/           # Custom client wrapper code
│   └── main.py       # CloudGlue class implementation  
└── sdk/              # Auto-generated API code
dist/                 # Pre-built package dist
spec/                 # Git submodule with OpenAPI specification
└── spec/             # Nested spec directory
    └── openapi.json  # OpenAPI spec file
```
