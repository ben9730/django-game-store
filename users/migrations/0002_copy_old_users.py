from django.db import migrations


def copy_users(apps, schema_editor):
    AuthUser = apps.get_model('auth', 'User')
    CustomUser = apps.get_model('users', 'CustomUser')

    for old in AuthUser.objects.all():
        # Skip if already exists (in case of reruns)
        if CustomUser.objects.filter(id=old.id).exists():
            continue
        CustomUser.objects.create(
            id=old.id,
            password=old.password,
            last_login=old.last_login,
            is_superuser=old.is_superuser,
            username=old.username,
            first_name=old.first_name,
            last_name=old.last_name,
            email=old.email,
            is_staff=old.is_staff,
            is_active=old.is_active,
            date_joined=old.date_joined,
        )


def noop(apps, schema_editor):
    """No-op reverse migration."""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(copy_users, noop),
    ]
