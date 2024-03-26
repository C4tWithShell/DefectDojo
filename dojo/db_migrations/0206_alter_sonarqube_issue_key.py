from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0201_populate_finding_sla_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sonarqube_issue',
            name='key',
            field=models.CharField(help_text='SonarQube issue key', max_length=60, unique=True),
        ),
    ]