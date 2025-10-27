import os
from typing import Dict

import git
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


def git_commit_and_push(festival: str, user_email: str, user_name: str):
    """Commit changes to git and optionally push to origin"""
    try:
        repo = git.Repo(settings.ROOT_DIR)
        filename = FESTIVAL_FILES.get(festival)
        file_path = os.path.join('config', 'snippets', filename)

        # Configure git user for this commit
        with repo.config_writer() as config:
            config.set_value('user', 'email', user_email)
            config.set_value('user', 'name', user_name)

        # Stage the file
        repo.index.add([file_path])

        # Commit
        commit_message = f"Update {festival} content via web editor\n\nEdited by: {user_name} ({user_email})"
        repo.index.commit(commit_message)

        # Push to origin (GitHub)
        # Note: This requires SSH keys to be configured
        # If not configured, it will fail silently
        try:
            origin = repo.remote(name='origin')
            origin.push()
            return True, "Changes committed and pushed to GitHub"
        except Exception as push_error:
            # Commit succeeded but push failed
            return True, f"Changes committed locally. Push failed: {str(push_error)}"

    except Exception as e:
        return False, f"Git operation failed: {str(e)}"


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

        # Save YAML file
        if save_yaml_file(festival, content):
            # Reload snippets in memory
            ContentSnippets().reload()

            # Get user info for git commit
            user_email = request.user.email or 'noreply@acrofestival.com'
            user_name = request.user.get_full_name() or request.user.username

            # Commit to git
            success, message = git_commit_and_push(festival, user_email, user_name)

            if success:
                messages.success(request, f"{message}")
            else:
                messages.warning(request, f"Content saved but git failed: {message}")

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
