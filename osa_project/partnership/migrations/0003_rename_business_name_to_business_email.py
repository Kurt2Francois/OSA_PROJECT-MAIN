from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partnership', '0002_rename_created_date_department_created_at_and_more'),
    ]

    operations = [
        # Rename business_name -> business_email on UserProfile
        migrations.RenameField(
            model_name='userprofile',
            old_name='business_name',
            new_name='business_email',
        ),
        # Rename business_name -> business_email on Department
        migrations.RenameField(
            model_name='department',
            old_name='business_name',
            new_name='business_email',
        ),
        # Ensure the field is an EmailField (sets validation at Django level)
        migrations.AlterField(
            model_name='userprofile',
            name='business_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='business_email',
            field=models.EmailField(max_length=255),
        ),
    ]
