#!/usr/bin/env python3
"""
Script to verify the Arabic courses in the database
"""

import pymysql

def get_db_connection():
    """Get database connection"""
    return pymysql.connect(
        host='mysql-31a284a2-s7304690-462f.i.aivencloud.com',
        user='avnadmin',
        password='AVNS_KUiCMFzJ3QHxBt_jkJW',
        database='defaultdb',
        port=27671,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def verify_courses():
    """Verify the courses in database"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            print("🔍 Verifying courses in database...")

            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM courses")
            result = cursor.fetchone()
            total_courses = result['total']
            print(f"📊 Total courses: {total_courses}")

            # Get courses by category
            cursor.execute("SELECT category, COUNT(*) as count FROM courses GROUP BY category ORDER BY category")
            categories = cursor.fetchall()
            print("\n📂 Courses by category:")
            for cat in categories:
                print(f"  {cat['category']}: {cat['count']} courses")

            # Show sample Arabic courses
            cursor.execute("""
                SELECT id, name, category, pricing_type, session_price, monthly_price
                FROM courses
                WHERE name LIKE '%ال%'
                LIMIT 10
            """)
            arabic_courses = cursor.fetchall()

            if arabic_courses:
                print("\n✅ Arabic courses found:")
                for course in arabic_courses:
                    price_info = ""
                    if course['pricing_type'] == 'session':
                        price_info = f"{course['session_price']} DA/session"
                    elif course['pricing_type'] == 'monthly':
                        price_info = f"{course['monthly_price']} DA/month"

                    print(f"  {course['id']}. {course['name']}")
                    print(f"     Category: {course['category']}, Price: {price_info}")
            else:
                print("\n❌ No Arabic courses found!")

            # Check pricing structure
            cursor.execute("""
                SELECT pricing_type, COUNT(*) as count,
                       MIN(COALESCE(session_price, monthly_price)) as min_price,
                       MAX(COALESCE(session_price, monthly_price)) as max_price
                FROM courses
                GROUP BY pricing_type
            """)
            pricing_stats = cursor.fetchall()

            print("\n💰 Pricing structure:")
            for stat in pricing_stats:
                print(f"  {stat['pricing_type']}: {stat['count']} courses")
                print(f"     Price range: {stat['min_price']} - {stat['max_price']} DA")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    verify_courses()
