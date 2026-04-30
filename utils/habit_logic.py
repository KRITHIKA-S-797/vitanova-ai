from utils.db import get_connection

def add_points(points):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT total_points FROM user_stats WHERE id = 1")
    row = cursor.fetchone()

    if row:
        total = row[0] + points
        cursor.execute("UPDATE user_stats SET total_points = ? WHERE id = 1", (total,))
    else:
        cursor.execute("INSERT INTO user_stats (id, total_points) VALUES (1, ?)", (points,))

    conn.commit()
    conn.close()

def get_total_points():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT total_points FROM user_stats WHERE id = 1")
    row = cursor.fetchone()

    conn.close()
    return row[0] if row else 0