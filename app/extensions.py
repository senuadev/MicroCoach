from supabase import create_client, Client

class Supabase:
    def __init__(self):
        self.client: Client | None = None

    def init_app(self, app):
        url = app.config['SUPABASE_URL']
        key = app.config['SUPABASE_KEY']
        self.client = create_client(url, key)

# Global extension instance
supabase = Supabase()
