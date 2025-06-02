import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.auth.models import User
from app.auth.security import get_password_hash
from app.core.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession



async def create_superuser(email: str, password: str, full_name: str = ""):
    async with async_session_maker() as session:
        async with session.begin():
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                full_name=full_name,
                role="admin"
            )
            session.add(user)
        await session.commit()
        print(f"Superuser {email} created successfully.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python create_superuser.py email password [full_name]")
        sys.exit(1)
    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3] if len(sys.argv) > 3 else ""
    asyncio.run(create_superuser(email, password, full_name))
