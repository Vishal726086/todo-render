from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='vishal').exists():
    User.objects.create_superuser('vishal', 'alphaz010101@gmail.com', 'todoapp11')
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")
