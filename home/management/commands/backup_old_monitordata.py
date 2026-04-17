import os
import shutil
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from home.models import MonitorData
from django.utils import timezone


class Command(BaseCommand):
    help = "Backup DB, keep only MonitorData older than 30 days in backup, then delete them from main DB"

    def handle(self, *args, **kwargs):

        cutoff_date = datetime.now() - timedelta(days=15)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')

        today = datetime.now().strftime('%d-%m-%Y')

        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'db_backups')
        os.makedirs(backup_dir, exist_ok=True)

        backup_db_path = os.path.join(
            backup_dir, f"{today}_db.sqlite3"
        )

        # --------------------------------------------------
        # 1️⃣ FULL DATABASE BACKUP (SQLite file copy)
        # --------------------------------------------------
        shutil.copy2(db_path, backup_db_path)
        self.stdout.write(self.style.SUCCESS(
            f"✅ Database backup created: {backup_db_path}"
        ))

        # --------------------------------------------------
        # 2️⃣ REMOVE RECENT DATA FROM BACKUP DB
        #     (Keep ONLY PunchDate < 90 days)
        # --------------------------------------------------
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{backup_db_path}' AS backupdb;")

            cursor.execute(f"""
                DELETE FROM backupdb.home_monitordata
                WHERE PunchDate >= '{cutoff_str}';
            """)

            cursor.execute("DETACH DATABASE backupdb;")

        self.stdout.write(self.style.SUCCESS(
            "✂️ Backup DB cleaned (only data older than 90 days kept)"
        ))

        # --------------------------------------------------
        # 3️⃣ DELETE OLD DATA FROM MAIN DB
        # --------------------------------------------------
        deleted, _ = MonitorData.objects.filter(
            PunchDate__lt=cutoff_date
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"🗑️ Deleted {deleted} old MonitorData records from main DB"
        ))

        # --------------------------------------------------
        # 4️⃣ RESET SQLITE AUTO-INCREMENT (SAFE)
        # --------------------------------------------------
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='home_monitordata';"
            )

        self.stdout.write(self.style.SUCCESS(
            "🔁 Auto-increment reset completed"
        ))
