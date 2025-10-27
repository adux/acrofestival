import base64
import os
from typing import Dict, Tuple

import requests
import yaml
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from acrofestival.content.snippets import ContentSnippets


FESTIVAL_FILES = {
    'urbanacro': 'urbanacro.yml',
    'winteracro': 'winteracro.yml',
    'dap': 'dap.yml',
    'general': 'general.yml',
}

# GitHub repository configuration
GITHUB_OWNER = 'adux'
GITHUB_REPO = 'acrofestival'
GITHUB_BRANCH = 'master'


def get_snippets_dir():
    """Get the path to the snippets directory"""
    return os.path.join(settings.ROOT_DIR, 'config', 'snippets')


def load_yaml_file(festival: str) -> Dict:
    """Load YAML content for a specific festival"""
    filename = FESTIVAL_FILES.get(festival)
    if not filename:
        return {}

    file_path = os.path.join(get_snippets_dir(), filename)
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def save_yaml_file(festival: str, content: Dict) -> bool:
    """Save YAML content for a specific festival"""
    filename = FESTIVAL_FILES.get(festival)
    if not filename:
        return False

    file_path = os.path.join(get_snippets_dir(), filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(content, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return True


def commit_to_github(festival: str, content: Dict, user_email: str, user_name: str) -> Tuple[bool, str]:
    """
    Commit changes to GitHub using the GitHub API.
    Requires GITHUB_TOKEN environment variable to be set.
    """
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        return False, "GITHUB_TOKEN not configured. Changes saved locally only."

    filename = FESTIVAL_FILES.get(festival)
    if not filename:
        return False, "Invalid festival"

    file_path = f"config/snippets/{filename}"

    # Convert YAML content to string
    yaml_content = yaml.dump(content, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Encode content to base64
    content_encoded = base64.b64encode(yaml_content.encode('utf-8')).decode('utf-8')

    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{file_path}"

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    try:
        # Get the current file SHA (required for updates)
        response = requests.get(api_url, headers=headers, params={'ref': GITHUB_BRANCH})

        if response.status_code == 200:
            current_sha = response.json()['sha']
        elif response.status_code == 404:
            # File doesn't exist yet
            current_sha = None
        else:
            return False, f"GitHub API error: {response.status_code} - {response.text}"

        # Prepare commit data
        commit_message = f"Update {festival} content via web editor\n\nEdited by: {user_name} ({user_email})"

        commit_data = {
            'message': commit_message,
            'content': content_encoded,
            'branch': GITHUB_BRANCH,
            'committer': {
                'name': user_name,
                'email': user_email,
            },
        }

        if current_sha:
            commit_data['sha'] = current_sha

        # Create/update the file
        response = requests.put(api_url, headers=headers, json=commit_data)

        if response.status_code in [200, 201]:
            commit_url = response.json().get('commit', {}).get('html_url', '')
            return True, f"Changes committed to GitHub successfully! {commit_url}"
        else:
            return False, f"GitHub commit failed: {response.status_code} - {response.text}"

    except Exception as e:
        return False, f"GitHub API error: {str(e)}"


@staff_member_required
@require_http_methods(["GET"])
def content_editor_list(request):
    """List all available festivals for editing"""
    festivals = [
        {'key': 'urbanacro', 'name': 'Urban Acro Festival'},
        {'key': 'winteracro', 'name': 'Winter Acro Festival'},
        {'key': 'dap', 'name': 'Dynamic Acro Program'},
        {'key': 'general', 'name': 'General Content'},
    ]

    return render(request, 'content/editor_list.html', {
        'festivals': festivals,
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def content_editor_edit(request, festival):
    """Edit content for a specific festival"""
    if festival not in FESTIVAL_FILES:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect('content:editor_list')

    if request.method == 'POST':
        # Parse form data back into YAML structure
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                yaml_key = key[8:]  # Remove 'content_' prefix
                content[yaml_key] = value

        # Save YAML file locally
        if save_yaml_file(festival, content):
            # Reload snippets in memory
            ContentSnippets().reload()

            # Get user info for git commit
            user_email = request.user.email or 'noreply@acrofestival.com'
            user_name = request.user.get_full_name() or request.user.username

            # Commit to GitHub
            success, message = commit_to_github(festival, content, user_email, user_name)

            if success:
                messages.success(request, message)
            else:
                messages.warning(request, f"Content saved locally. GitHub sync: {message}")

            return redirect('content:editor_edit', festival=festival)
        else:
            messages.error(request, "Failed to save content")

    # Load current content
    content = load_yaml_file(festival)

    # Sort keys for consistent display
    sorted_content = sorted(content.items(), key=lambda x: x[0])

    festival_name = next(
        (f['name'] for f in [
            {'key': 'urbanacro', 'name': 'Urban Acro Festival'},
            {'key': 'winteracro', 'name': 'Winter Acro Festival'},
            {'key': 'dap', 'name': 'Dynamic Acro Program'},
            {'key': 'general', 'name': 'General Content'},
        ] if f['key'] == festival),
        festival.title()
    )

    return render(request, 'content/editor_edit.html', {
        'festival': festival,
        'festival_name': festival_name,
        'content': sorted_content,
    })
