"""
SQLite Database Verification Script
Tests: connection, table creation, CRUD operations, relationships
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("=" * 60)
    print("  SQLite Database Verification")
    print("=" * 60)
    
    test_db_path = "sqlite:///./test_verify.db"
    passed = 0
    failed = 0
    
    # ── Test 1: Import models ──────────────────────────────────────
    print("\n[1/7] Importing SQLite models...", end=" ")
    try:
        from models.database import (
            DatabaseManager, Base,
            User, Business, Campaign, Content, Analytics, Message, AILog,
            UserRepository, BusinessRepository, CampaignRepository,
            ContentRepository, AnalyticsRepository, MessageRepository, AILogRepository,
        )
        print("OK ✓")
        passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1
        print("\nCannot continue without models. Aborting.")
        return
    
    # ── Test 2: Connect & create tables ────────────────────────────
    print("[2/7] Connecting to SQLite & creating tables...", end=" ")
    try:
        db = DatabaseManager(test_db_path)
        db.connect()
        print("OK ✓")
        passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1
        print("\nCannot continue without connection. Aborting.")
        return
    
    # ── Test 3: Verify tables exist ────────────────────────────────
    print("[3/7] Verifying tables...", end=" ")
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        expected = {"users", "businesses", "campaigns", "contents", "analytics", "messages", "ai_logs"}
        found = expected & set(tables)
        missing = expected - set(tables)
        if missing:
            print(f"WARN ⚠  → missing tables: {missing}")
            failed += 1
        else:
            print(f"OK ✓  → found {len(found)} tables: {sorted(found)}")
            passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1

    # ── Test 4: CRUD – Create a User ───────────────────────────────
    print("[4/7] CRUD: Creating user...", end=" ")
    user_id = None
    try:
        with db.get_session() as session:
            repo = UserRepository(session)
            user = repo.create({
                "email": "test@example.com",
                "full_name": "Test User",
                "first_name": "Test",
                "last_name": "User",
                "password_hash": "fakehash123",
                "provider": "email",
                "is_active": True,
            })
            user_id = user.id
        print(f"OK ✓  → id={user_id}")
        passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1

    # ── Test 5: CRUD – Read user back ──────────────────────────────
    print("[5/7] CRUD: Reading user...", end=" ")
    try:
        with db.get_session() as session:
            repo = UserRepository(session)
            user = repo.get_by_email("test@example.com")
            assert user is not None, "User not found by email"
            assert user.full_name == "Test User"
            user2 = repo.get_by_id(user_id)
            assert user2 is not None, "User not found by id"
        print("OK ✓")
        passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1

    # ── Test 6: CRUD – Create Business + Campaign + Content ────────
    print("[6/7] CRUD: Business → Campaign → Content chain...", end=" ")
    try:
        with db.get_session() as session:
            biz_repo = BusinessRepository(session)
            biz = biz_repo.create({
                "owner_id": user_id,
                "name": "Test Biz",
                "industry": "Technology",
            })
            
            camp_repo = CampaignRepository(session)
            camp = camp_repo.create({
                "business_id": biz.id,
                "name": "Launch Campaign",
                "objective": "Brand Awareness",
            })
            
            cont_repo = ContentRepository(session)
            content = cont_repo.create({
                "business_id": biz.id,
                "campaign_id": camp.id,
                "title": "Welcome Post",
                "content_type": "post",
                "platform": "instagram",
            })
            
            # Save IDs before session closes
            biz_id = biz.id
            biz_owner = biz.owner_id
            camp_id = camp.id
            camp_biz = camp.business_id
            cont_id = content.id
            cont_camp = content.campaign_id

        # Verify relationships (using saved IDs)
        assert biz_owner == user_id
        assert camp_biz == biz_id
        assert cont_camp == camp_id
        print(f"OK ✓  → biz={biz_id[:8]}… camp={camp_id[:8]}… content={cont_id[:8]}…")
        passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1

    # ── Test 7: CRUD – Update & Delete ─────────────────────────────
    print("[7/7] CRUD: Update & delete...", end=" ")
    try:
        with db.get_session() as session:
            repo = UserRepository(session)
            updated = repo.update(user_id, {"full_name": "Updated User"})
            assert updated is not None
            assert updated.full_name == "Updated User"
        print("OK ✓")
        passed += 1
    except Exception as e:
        print(f"FAIL ✗  → {e}")
        failed += 1

    # ── Cleanup ────────────────────────────────────────────────────
    db.disconnect()
    try:
        os.remove("test_verify.db")
    except:
        pass

    # ── Summary ────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    total = passed + failed
    print(f"  Results: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print("  ✅ SQLite database is fully working!")
    else:
        print("  ⚠️  Some tests failed – review output above")
    print("=" * 60)
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
