#!/bin/bash

# Repository Initialization Script
# Creates a new repository from boilerplate with customized naming and configuration

# shellcheck disable=SC2001

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Color codes for output formatting
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Global variables
# SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME=""
APP_DESCRIPTION=""
CUSTOMER_NAME=""
AZURE_USER_ID=""
AZURE_STORY_ID=""
REMOTE_URL=""
TARGET_DIR=""

AZURE_DOMAIN="DOMAIN"

# ---------------------------------------------------------------------------- #
#FUNCTION: print_message
#DESCRIPTION: Prints colored output messages to the terminal
# ---------------------------------------------------------------------------- #
print_message() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

# ---------------------------------------------------------------------------- #
#FUNCTION: error_exit
#DESCRIPTION: Prints error message and exits the script with status code 1
# ---------------------------------------------------------------------------- #
error_exit() {
    print_message "$RED" "ERROR: $1" >&2
    exit 1
}

# ---------------------------------------------------------------------------- #
#FUNCTION: validate_dependencies
#DESCRIPTION: Validates that required tools (git, find, sed, uv) are available
# ---------------------------------------------------------------------------- #
validate_dependencies() {
    local missing_tools=()

    command -v git >/dev/null 2>&1 || missing_tools+=("git")
    command -v find >/dev/null 2>&1 || missing_tools+=("find")
    command -v sed >/dev/null 2>&1 || missing_tools+=("sed")
    command -v uv >/dev/null 2>&1 || missing_tools+=("uv")

    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        error_exit "Missing required tools: ${missing_tools[*]}"
    fi
}

# ---------------------------------------------------------------------------- #
#FUNCTION: get_user_input
#DESCRIPTION: Collects user input for all required and optional configuration parameters
# ---------------------------------------------------------------------------- #
get_user_input() {
    print_message "$BLUE" "=== Repository Initialization Setup ==="
    echo

    # Application name (mandatory)
    while [[ -z "$APP_NAME" ]]; do
        read -r -p "Application name (mandatory): " APP_NAME
        APP_NAME="$(echo "$APP_NAME" | xargs)"  # Trim whitespace

        if [[ -z "$APP_NAME" ]]; then
            print_message "$RED" "Application name cannot be empty!"
        fi
    done

    # Application description (optional)
    read -r -p "Application description (optional): " APP_DESCRIPTION
    APP_DESCRIPTION="$(echo "$APP_DESCRIPTION" | xargs)"

    # Customer name (optional)
    read -r -p "Customer name (optional): " CUSTOMER_NAME
    CUSTOMER_NAME="$(echo "$CUSTOMER_NAME" | xargs)"

    # Azure DevOps User ID (optional)
    read -r -p "Azure DevOps User ID (optional): " AZURE_USER_ID
    AZURE_USER_ID="$(echo "$AZURE_USER_ID" | xargs)"

    # Azure DevOps User Story ID (optional)
    read -r -p "Azure DevOps User Story ID (optional): " AZURE_STORY_ID
    AZURE_STORY_ID="$(echo "$AZURE_STORY_ID" | xargs)"

    # Remote repository URL (optional)
    read -r -p "Remote repository URL (optional): " REMOTE_URL
    REMOTE_URL="$(echo "$REMOTE_URL" | xargs)"

    echo
}

# ---------------------------------------------------------------------------- #
# FUNCTION: sanitize_name
# DESCRIPTION: Convert app or customer name to different formats
# ---------------------------------------------------------------------------- #
sanitize_name() {
    local input="$1"
    local format="$2"

    if [[ -z "$input" ]]; then
        echo ""
        return
    fi

    case "$format" in
        "camel")
            echo "$input" | sed 's/[[:space:]_-]\+/ /g' | sed 's/\b\w/\U&/g' | sed 's/ //g' | sed 's/^\(.\)/\l\1/'
            ;;
        "kebab")
            echo "$input" | tr '[:upper:]' '[:lower:]' | sed 's/[[:space:]_]\+/-/g'
            ;;
        "pascal")
            echo "$input" | sed 's/[[:space:]_-]\+/ /g' | sed 's/\b\w/\U&/g' | sed 's/ //g'
            ;;
        "snake")
            echo "$input" | tr '[:upper:]' '[:lower:]' | sed 's/[[:space:]-]\+/_/g'
            ;;
        "title")
            echo "$input" | sed 's/[[:space:]_-]\+/ /g' | sed 's/\b\w/\U&/g'
            ;;
        *)
            echo "$input"
            ;;
    esac
}

# ---------------------------------------------------------------------------- #
# FUNCTION: create_target_directory
# DESCRIPTION: Creates the target directory for the new repository outside current directory
# ---------------------------------------------------------------------------- #
create_target_directory() {
    local app_kebab
    app_kebab=$(sanitize_name "$APP_NAME" "kebab")
    TARGET_DIR="../$app_kebab"

    if [[ -d "$TARGET_DIR" ]]; then
        print_message "$RED" "Directory '$TARGET_DIR' already exists"
        read -p "Do you want to remove it and continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error_exit "Aborted by user"
        fi
        rm -rf "$TARGET_DIR"
    fi

    print_message "$YELLOW" "Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR" || error_exit "Failed to create directory '$TARGET_DIR'"
}

# ---------------------------------------------------------------------------- #
#FUNCTION: copy_boilerplate
#DESCRIPTION: Copies all boilerplate files to the target directory excluding specified items
# ---------------------------------------------------------------------------- #
copy_boilerplate() {
    print_message "$YELLOW" "Copying boilerplate files..."

    # Use rsync if available for better performance, otherwise use cp
    if command -v rsync >/dev/null 2>&1; then
        rsync -a \
            --exclude='.git' \
            --exclude='.mypy_cache' \
            --exclude='.pytest_cache' \
            --exclude='.ruff_cache' \
            --exclude='.venv' \
            --exclude='.python-version' \
            --exclude='README.md' \
            --exclude='init.sh' \
            ./ "$TARGET_DIR/" || error_exit "Failed to copy files with rsync"
    else
        # Fallback to find and cp for dotfiles and directories
        find . -maxdepth 1 -not -name '.' \
            -not -name '.git' \
            -not -name '.mypy_cache' \
            -not -name '.pytest_cache' \
            -not -name '.ruff_cache' \
            -not -name '.venv' \
            -not -name '.python-version' \
            -not -name 'README.md' \
            -not -name 'init.sh' \
            -exec cp -r {} "$TARGET_DIR/" \; || error_exit "Failed to copy files"
    fi

    print_message "$GREEN" "Files copied successfully"
}

# ---------------------------------------------------------------------------- #
#FUNCTION: perform_replacements
#DESCRIPTION: Performs text replacements in all files using regex to maintain formatting
# ---------------------------------------------------------------------------- #
perform_replacements() {
    print_message "$YELLOW" "Performing text replacements..."

    local app_kebab app_pascal app_snake app_title
    local customer_kebab customer_pascal
    local combined_kebab combined_snake_kebab combined_pascal

    # Generate app name variants
    app_camel=$(sanitize_name "$APP_NAME" "camel")
    app_kebab=$(sanitize_name "$APP_NAME" "kebab")
    app_pascal=$(sanitize_name "$APP_NAME" "pascal")
    app_snake=$(sanitize_name "$APP_NAME" "snake")
    app_title=$(sanitize_name "$APP_NAME" "title")

    # Generate customer variants if provided
    if [[ -n "$CUSTOMER_NAME" ]]; then
        customer_kebab=$(sanitize_name "$CUSTOMER_NAME" "kebab")
        customer_pascal=$(sanitize_name "$CUSTOMER_NAME" "pascal")

        combined_kebab="${customer_kebab}-${app_kebab}"
        combined_snake_kebab="${customer_kebab}_${app_kebab}"
        combined_pascal="${customer_pascal}__${app_pascal}"
    else
        combined_kebab="$app_kebab"
        combined_snake_kebab="$app_kebab"
        combined_pascal="$app_pascal"
    fi

    # Use app description or fallback to app name
    local description="${APP_DESCRIPTION:-$APP_NAME}"

    # Find all text files (exclude binary files and common cache/build directories)
    local files_to_process
    mapfile -t files_to_process < <(
        find "$TARGET_DIR" -type f \
            -not -path "*/node_modules/*" \
            -not -path "*/venv/*" \
            -not -path "*/__pycache__/*" \
            -not -path "*/build/*" \
            -not -path "*/dist/*" \
            -exec file {} \; | \
        grep -E "(text|empty)" | \
        cut -d: -f1
    )

    if [[ ${#files_to_process[@]} -eq 0 ]]; then
        print_message "$YELLOW" "No text files found to process"
        return
    fi

    print_message "$BLUE" "Processing ${#files_to_process[@]} files..."

    # Perform replacements on each file
    for file in "${files_to_process[@]}"; do
        # Skip if file doesn't exist (race condition protection)
        [[ -f "$file" ]] || continue

        # Create a temporary file for atomic updates
        local temp_file="${file}.tmp"

        # Perform all replacements in one sed command for efficiency
        sed -E \
            -e "s/appName/${app_camel}/g" \
            -e "s/customer-app-name/${combined_kebab}/g" \
            -e "s/customer_app-name/${combined_snake_kebab}/g" \
            -e "s/Customer__AppName/${combined_pascal}/g" \
            -e "s/Application Name/${app_title}/g" \
            -e "s/app-name/${app_kebab}/g" \
            -e "s/app_name/${app_snake}/g" \
            -e "s/app-description/${description}/g" \
            "$file" > "$temp_file" || error_exit "Failed to process file: $file"

        # Atomically replace the original file
        mv "$temp_file" "$file" || error_exit "Failed to update file: $file"
    done

    print_message "$GREEN" "Text replacements completed"
}

# ---------------------------------------------------------------------------- #
#FUNCTION: rename_items
#DESCRIPTION: Renames directories and files containing app-name patterns to match the new application name
# ---------------------------------------------------------------------------- #
rename_items() {
    print_message "$YELLOW" "Renaming directories and files..."

    local app_snake app_kebab
    app_snake=$(sanitize_name "$APP_NAME" "snake")
    app_kebab=$(sanitize_name "$APP_NAME" "kebab")

    # Rename directories containing app_name (process from deepest first)
    find "$TARGET_DIR" -type d -name "*app_name*" | sort -r | while read -r dir; do
        local new_dir="${dir//app_name/$app_snake}"
        if [[ "$dir" != "$new_dir" ]]; then
            print_message "$BLUE" "Renaming directory: $(basename "$dir") -> $(basename "$new_dir")"
            mv "$dir" "$new_dir" || error_exit "Failed to rename directory: $dir"
        fi
    done

    # Rename files containing app-name
    find "$TARGET_DIR" -type f -name "*app-name*" | while read -r file; do
        local new_file="${file//app-name/$app_kebab}"
        if [[ "$file" != "$new_file" ]]; then
            print_message "$BLUE" "Renaming file: $(basename "$file") -> $(basename "$new_file")"
            mv "$file" "$new_file" || error_exit "Failed to rename file: $file"
        fi
    done

    # Rename README file
    print_message "$BLUE" "Renaming file: README_app.md -> README.md"
    mv "$TARGET_DIR/README_app.md" "$TARGET_DIR/README.md" || error_exit "Failed to rename README_app.md"
    sed -i "s/README_app/README/g" "$TARGET_DIR/.githooks/readme_update.py"

    print_message "$GREEN" "Renaming completed"
}

# ---------------------------------------------------------------------------- #
#FUNCTION: update_renovate_config
#DESCRIPTION: Updates renovate.json with Azure DevOps User ID and Work Item ID if provided
# ---------------------------------------------------------------------------- #
update_renovate_config() {
    local renovate_file="$TARGET_DIR/renovate.json"

    if [[ ! -f "$renovate_file" ]]; then
        print_message "$YELLOW" "renovate.json not found, skipping Azure DevOps configuration"
        return
    fi

    if [[ -n "$AZURE_STORY_ID" || -n "$AZURE_USER_ID" ]]; then
        print_message "$YELLOW" "Updating renovate.json..."

        local temp_file="${renovate_file}.tmp"

        # Read the current file
        cp "$renovate_file" "$temp_file" || error_exit "Failed to create temp file for renovate.json"

        # Update Azure Work Item ID if provided
        if [[ -n "$AZURE_STORY_ID" && "$AZURE_STORY_ID" =~ ^[0-9]+$ ]]; then
            sed -i -E "s/\"azureWorkItemId\":[[:space:]]*[0-9]+/\"azureWorkItemId\": $AZURE_STORY_ID/" "$temp_file"
        fi

        # Update reviewer if user ID provided
        if [[ -n "$AZURE_USER_ID" ]]; then
            sed -i -E "s/required:$AZURE_DOMAIN\\\\\\\\azure_user_id/required:$AZURE_DOMAIN\\\\\\\\$AZURE_USER_ID/" "$temp_file"
        fi

        # Atomically replace the original file
        mv "$temp_file" "$renovate_file" || error_exit "Failed to update renovate.json"

        print_message "$GREEN" "renovate.json updated successfully"
    fi
}

# ---------------------------------------------------------------------------- #
# FUNCTION: setup_virtual_environment
# DESCRIPTION: Create and initialize virtual environment using uv
# ---------------------------------------------------------------------------- #
setup_virtual_environment() {
    print_message "$YELLOW" "Setting up virtual environment with uv..."

    cd "$TARGET_DIR" || error_exit "Failed to change to target directory"

    if [[ -f "pyproject.toml" ]]; then
        unset VIRTUAL_ENV
        uv sync --frozen || error_exit "Failed to create virtual environment"
        print_message "$GREEN" "Virtual environment created successfully"
    else
        print_message "$YELLOW" "No pyproject.toml found, skipping virtual environment setup"
    fi

    cd - > /dev/null
}

# ---------------------------------------------------------------------------- #
#FUNCTION: initialize_git_repository
#DESCRIPTION: Initializes git repository and adds remote origin if URL is provided
# ---------------------------------------------------------------------------- #
initialize_git_repository() {
    print_message "$YELLOW" "Initializing git repository..."

    cd "$TARGET_DIR" || error_exit "Failed to change to target directory"

    # Initialize git repository
    git init --initial-branch main || error_exit "Failed to initialize git repository"

    # Add remote if URL provided
    if [[ -n "$REMOTE_URL" ]]; then
        print_message "$BLUE" "Adding remote origin: $REMOTE_URL"
        git remote add origin "$REMOTE_URL" || error_exit "Failed to add remote origin"
    fi

    print_message "$GREEN" "Git repository initialized successfully"
    cd - > /dev/null
}

# ---------------------------------------------------------------------------- #
# FUNCTION: stage_initial_commit
# DESCRIPTION: Stage all files for the initial commit
# ---------------------------------------------------------------------------- #
stage_initial_commit() {
    print_message "$YELLOW" "Staging files for initial commit..."

    cd "$TARGET_DIR" || error_exit "Failed to change to target directory"
    git add . || error_exit "Failed to stage files"

    print_message "$GREEN" "Files staged successfully"
    cd - > /dev/null
}

# ---------------------------------------------------------------------------- #
# FUNCTION: install_precommit_hooks
# DESCRIPTION: Install pre-commit hooks using uv
# ---------------------------------------------------------------------------- #
install_precommit_hooks() {
    print_message "$YELLOW" "Installing pre-commit hooks..."

    cd "$TARGET_DIR" || error_exit "Failed to change to target directory"

    if [[ -f ".pre-commit-config.yaml" ]]; then
        chmod +x -R .githooks
        git add .githooks || error_exit "Failed to stage local pre-commit hook files"
        uv run prek install --install-hooks || error_exit "Failed to install pre-commit hooks"
        print_message "$GREEN" "Pre-commit hooks installed successfully"
    else
        print_message "$YELLOW" "No .pre-commit-config.yaml found, skipping pre-commit setup"
    fi

    cd - > /dev/null
}

# ---------------------------------------------------------------------------- #
# FUNCTION: run_precommit_hooks
# DESCRIPTION: Run pre-commit hooks on all staged files
# ---------------------------------------------------------------------------- #
run_precommit_hooks() {
    print_message "$YELLOW" "Running pre-commit hooks..."

    cd "$TARGET_DIR" || error_exit "Failed to change to target directory"

    if [[ -f ".pre-commit-config.yaml" ]]; then
        uv run pre-commit run --all-files || error_exit "Failed to run pre-commit hooks"
        print_message "$GREEN" "Pre-commit hooks run successfully"
    else
        print_message "$YELLOW" "No .pre-commit-config.yaml found, skipping pre-commit run"
    fi

    cd - > /dev/null
}

# ---------------------------------------------------------------------------- #
#FUNCTION: display_summary
#DESCRIPTION: Displays a summary of the initialization process and next steps
# ---------------------------------------------------------------------------- #
display_summary() {
    echo
    print_message "$GREEN" "=== Repository Initialization Complete ==="
    echo "Application Name: $APP_NAME"
    [[ -n "$APP_DESCRIPTION" ]] && echo "Description: $APP_DESCRIPTION"
    [[ -n "$CUSTOMER_NAME" ]] && echo "Customer: $CUSTOMER_NAME"
    [[ -n "$AZURE_USER_ID" ]] && echo "Azure User ID: $AZURE_USER_ID"
    [[ -n "$AZURE_STORY_ID" ]] && echo "Azure Story ID: $AZURE_STORY_ID"
    [[ -n "$REMOTE_URL" ]] && echo "Remote URL: $REMOTE_URL"
    echo "Target Directory: $TARGET_DIR"
    echo
    print_message "$BLUE" "Next steps:"
    echo "1. cd $TARGET_DIR"
    echo "2. Open the project in Visual Studio Code: code $(sanitize_name "$APP_NAME" "kebab").code-workspace"
    echo "3. Review the generated files"
    echo "4. Make your initial commit: git commit -m 'Initial commit'"
    if [[ -n "$REMOTE_URL" ]]; then
        echo "5. Push to remote: git push --set-upstream origin main"
    else
        echo "5. Add remote: git remote add origin <URL>"
        echo "6. Push to remote: git push --set-upstream origin main"
    fi
    echo
}

# ---------------------------------------------------------------------------- #
#FUNCTION: main
#DESCRIPTION: Main execution function that orchestrates the entire repository initialization process
# ---------------------------------------------------------------------------- #
main() {
    print_message "$GREEN" "Repository Initialization Script"
    echo

    # Validate dependencies
    validate_dependencies

    # Get user input
    get_user_input

    # Create target directory and copy boilerplate files
    create_target_directory
    copy_boilerplate

    # Perform text replacements, rename directories and files
    perform_replacements
    rename_items

    # Update renovate configuration
    update_renovate_config

    # Setup development environment
    setup_virtual_environment
    initialize_git_repository
    stage_initial_commit

    # Install and run pre-commit hooks
    install_precommit_hooks
    run_precommit_hooks

    # Display summary
    display_summary
}

# Trap to cleanup on script interruption
trap 'print_message "$RED" "Script interrupted. Cleaning up..."; [[ -d "$TARGET_DIR" ]] && rm -rf "$TARGET_DIR"; exit 1' INT TERM

# Execute main function
main "$@"
