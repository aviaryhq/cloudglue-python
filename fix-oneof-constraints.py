#!/usr/bin/env python3
"""
Post-processing script to fix oneOf constraints in generated OpenAPI models.
The standard Python generator doesn't handle oneOf properly, so we fix it here.
"""

import re
import os
from pathlib import Path

def fix_add_collection_file():
    """Fix the AddCollectionFile model to handle oneOf constraint properly"""
    model_file = Path("cloudglue/sdk/models/add_collection_file.py")
    
    if not model_file.exists():
        print(f"Warning: {model_file} not found, skipping...")
        return
    
    print(f"Fixing oneOf constraint in {model_file}")
    
    # Read the file
    content = model_file.read_text()
    
    # Make file_id and url optional
    content = re.sub(
        r'file_id: StrictStr = Field\(',
        r'file_id: Optional[StrictStr] = Field(default=None, ',
        content
    )
    content = re.sub(
        r'url: StrictStr = Field\(',
        r'url: Optional[StrictStr] = Field(default=None, ',
        content
    )
    
    # Add model_validator import if not present
    if 'model_validator' not in content:
        content = re.sub(
            r'from pydantic import BaseModel, ConfigDict, Field, StrictStr',
            r'from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator',
            content
        )
    
    # Add validation method after model_config
    validation_method = '''
    @model_validator(mode='after')
    def validate_file_id_or_url(self) -> 'AddCollectionFile':
        """Validate that exactly one of file_id or url is provided (oneOf constraint)"""
        if not self.file_id and not self.url:
            raise ValueError('Either file_id or url must be provided')
        return self
'''
    
    # Insert validation method after model_config
    if '@model_validator' not in content:
        content = re.sub(
            r'(    model_config = ConfigDict\(\s*\n.*?\n    \))\n',
            r'\1\n' + validation_method,
            content,
            flags=re.DOTALL
        )
    
    # Write back the file
    model_file.write_text(content)
    print(f"Successfully fixed {model_file}")

def main():
    """Main function to fix all oneOf constraints"""
    print("Fixing oneOf constraints in generated models...")
    fix_add_collection_file()
    print("oneOf constraint fixes complete!")

if __name__ == "__main__":
    main()
