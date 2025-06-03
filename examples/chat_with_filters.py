#!/usr/bin/env python3
"""
Example demonstrating how to use chat completion filters with CloudGlue.

This example shows different ways to create and use filters to constrain 
search results when using chat completions.
"""

import os
import cloudglue

def main():
    # Initialize the client
    client = cloudglue.CloudGlue(api_key=os.getenv("CLOUDGLUE_API_KEY"))
    
    # Example 1: Using the main filter creation method
    print("Example 1: Main filter creation method")
    chat_filter = client.chat.completions.create_filter(
        metadata_filters=[
            {'path': 'category', 'operator': 'Equal', 'value_text': 'tutorial'},
            {'path': 'tags', 'operator': 'ContainsAny', 'value_text_array': ['python', 'programming']}
        ],
        video_info_filters=[
            {'path': 'duration_seconds', 'operator': 'LessThan', 'value_text': '600'}  # Videos under 10 minutes
        ],
        file_filters=[
            {'path': 'filename', 'operator': 'ContainsAny', 'value_text_array': ['.mp4', '.avi']}
        ]
    )
    
    # Use the filter in a chat completion
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Explain Python basics"}],
        collections=["your-collection-id"],
        filter=chat_filter
    )
    print("Response with filter:", response.choices[0].message.content[:100] + "...")
    
    # Example 2: Using dictionary-based filter (passed directly)
    print("\\nExample 2: Dictionary-based filter")
    dict_filter = {
        'metadata': [
            {
                'path': 'topic',
                'operator': 'In',
                'valueText': None,  # Note: using API field names when passing dict directly
                'valueTextArray': ['machine-learning', 'data-science', 'ai']
            }
        ],
        'video_info': [
            {
                'path': 'duration_seconds', 
                'operator': 'GreaterThan',
                'valueText': '300',  # Videos longer than 5 minutes
                'valueTextArray': None
            }
        ]
    }
    
    response2 = client.chat.completions.create(
        messages=[{"role": "user", "content": "Tell me about AI topics"}],
        collections=["your-collection-id"],
        filter=dict_filter
    )
    print("Response with dict filter:", response2.choices[0].message.content[:100] + "...")
    
    # Example 3: Advanced usage with SDK classes (if more control needed)
    print("\\nExample 3: Using SDK classes directly")
    from cloudglue import ChatCompletionRequestFilter, ChatCompletionRequestFilterMetadataInner
    
    metadata_filter = ChatCompletionRequestFilterMetadataInner(
        path='difficulty_level',
        operator='Equal', 
        value_text='beginner'
    )
    
    advanced_filter = ChatCompletionRequestFilter(metadata=[metadata_filter])
    
    response3 = client.chat.completions.create(
        messages=[{"role": "user", "content": "Show me beginner content"}],
        collections=["your-collection-id"],
        filter=advanced_filter
    )
    print("Response with SDK classes:", response3.choices[0].message.content[:100] + "...")
    
    # Example 4: Common filter patterns
    print("\\nExample 4: Common filter patterns")
    
    # Filter by file upload date
    recent_files_filter = client.chat.completions.create_filter(
        file_filters=[
            {'path': 'created_at', 'operator': 'GreaterThan', 'value_text': '2024-01-01T00:00:00Z'}
        ]
    )
    
    # Filter by video duration range  
    medium_length_videos = client.chat.completions.create_filter(
        video_info_filters=[
            {'path': 'duration_seconds', 'operator': 'GreaterThan', 'value_text': '300'},  # > 5 min
            {'path': 'duration_seconds', 'operator': 'LessThan', 'value_text': '1800'}     # < 30 min
        ]
    )
    
    # Filter by multiple metadata categories
    specific_content_filter = client.chat.completions.create_filter(
        metadata_filters=[
            {'path': 'language', 'operator': 'Equal', 'value_text': 'english'},
            {'path': 'content_type', 'operator': 'In', 'value_text_array': ['lecture', 'tutorial', 'demo']},
            {'path': 'audience', 'operator': 'ContainsAny', 'value_text_array': ['beginner', 'intermediate']}
        ]
    )
    
    print("Created common filter patterns successfully!")


if __name__ == "__main__":
    main() 