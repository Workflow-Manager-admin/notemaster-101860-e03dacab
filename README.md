# notemaster-101860-e03dacab

## Backend Environment Setup (Supabase Integration)

The backend (`notes_backend`) requires access to a Supabase project. Credentials are read securely from environment variables:

- `SUPABASE_URL` – The API URL for your Supabase project
- `SUPABASE_KEY` – The service role or anon API key for this project

**Setup:**
1. Create a `.env` file in `notes_backend` with:

    ```
    SUPABASE_URL=https://your-project.supabase.co
    SUPABASE_KEY=your-supabase-key
    ```

2. The backend will automatically load these values at runtime (see `assets/supabase.md` for further details).

**DO NOT** expose `SUPABASE_KEY` in frontend or public code. These secrets must remain strictly on the backend.

**See `notes_backend/assets/supabase.md`** for more on schema, security, and troubleshooting.