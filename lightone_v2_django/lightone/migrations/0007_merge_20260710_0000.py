from django.db import migrations


class Migration(migrations.Migration):
    """Merge the independently created LightOne MVP migration branches."""

    dependencies = [
        ('lightone', '0005_alter_indicator_jatc_score_and_more'),
        ('lightone', '0005_membersession_indicator_link'),
        ('lightone', '0006_alter_membersession_safety_notice'),
        ('lightone', '0006_membersession_updated_at_and_more'),
    ]

    operations = []
