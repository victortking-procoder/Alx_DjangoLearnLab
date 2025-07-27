# Advanced Features and Security (Django Project)

This project demonstrates custom user models, user managers, and granular permission/group management in Django.

## Custom User Model

-   **Location:** `myapp/models.py`
-   **Model:** `CustomUser` extends `django.contrib.auth.models.AbstractUser`.
    -   **Added Fields:** `date_of_birth` (DateField), `profile_photo` (ImageField).
-   **Custom Manager:** `CustomUserManager` extends `django.contrib.auth.models.BaseUserManager`.
    -   Provides `create_user` and `create_superuser` methods to handle the custom user model.
-   **Settings:** `AUTH_USER_MODEL = 'myapp.CustomUser'` is set in `advanced_features_and_security/settings.py` to use this custom model throughout the project.
-   **Admin Integration:** `myapp/admin.py` defines `CustomUserAdmin` to display and manage custom fields in the Django admin.

## Permissions and Groups Setup

This section outlines how custom permissions and Django's built-in group system are used to control access.

### 1. Custom Permissions

-   **Location:** `myapp/models.py` (within the `Post` model's `Meta` class)
-   **Defined Permissions (for the `Post` model):**
    -   `can_view`: Allows viewing of post instances.
    -   `can_create`: Allows creation of new post instances.
    -   `can_edit`: Allows editing of existing post instances.
    -   `can_delete`: Allows deletion of post instances.
-   **Activation:** These permissions are automatically registered with Django's content type system upon `makemigrations` and `migrate`.

### 2. User Groups

Groups are configured via the Django admin interface (`/admin/groups/`).

-   **Admins Group:**
    -   **Permissions:** `myapp.can_view`, `myapp.can_create`, `myapp.can_edit`, `myapp.can_delete` (and typically other general admin permissions).
    -   **Role:** Full control over posts.
-   **Editors Group:**
    -   **Permissions:** `myapp.can_create`, `myapp.can_edit`.
    -   **Role:** Can create and modify posts.
-   **Viewers Group:**
    -   **Permissions:** `myapp.can_view`.
    -   **Role:** Can only view posts.

### 3. Permission Enforcement in Views

-   **Location:** `myapp/views.py`
-   **Mechanism:** Django's `django.contrib.auth.decorators.permission_required` decorator is used.
    -   **Syntax:** `@permission_required('app_label.permission_codename', raise_exception=True)`
    -   `raise_exception=True` ensures that if a user lacks the permission, a `403 Forbidden` HTTP response is returned.
-   **Protected Views:**
    -   `post_list`: Requires `myapp.can_view`.
    -   `post_create`: Requires `myapp.can_create`.
    -   `post_edit`: Requires `myapp.can_edit`.
    -   `post_delete`: Requires `myapp.can_delete`.
-   **Template-level Checks:** `{% if perms.myapp.can_create %}` etc., are used in `myapp/templates/myapp/post_list.html` to conditionally render UI elements based on user permissions.

### 4. Testing

To test the permission system:

1.  Ensure you have a superuser.
2.  Log in to the Django admin (`/admin/`).
3.  Create test users (e.g., `viewer1`, `editor1`, `admin1`, `regular_user`).
4.  Assign `viewer1` to the `Viewers` group.
5.  Assign `editor1` to the `Editors` group.
6.  Assign `admin1` to the `Admins` group.
7.  `regular_user` should not be in any of these groups.
8.  Log in as each user and attempt to access different post-related URLs (`/posts/`, `/posts/new/`, `/posts/<id>/edit/`, `/posts/<id>/delete/`) to verify that permissions are correctly enforced.
    -   **Viewers:** Only `GET /posts/` should work.
    -   **Editors:** `GET /posts/`, `GET /posts/new/`, `POST /posts/new/`, `GET /posts/<id>/edit/`, `POST /posts/<id>/edit/` should work. Delete actions should be forbidden.
    -   **Admins:** All actions should work.
    -   **Regular User:** All post-related actions should be forbidden (unless they have global permissions assigned directly, which is not recommended for granular control).